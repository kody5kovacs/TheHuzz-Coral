#Here is where the main MABfuzz class is defined. 
#This class will be responsible for running the fuzzing campaign using the multi-arm bandit algorithm
import subprocess, os, sys, re
import time, random, copy, datetime
import json, jsonlines
from string import Template
from tqdm import tqdm
import logging as lg # critical, error, warning, info, debug
import pandas as pd
import numpy as np

import config
from configManager import getCONFIG
import prog_gen, riscv_isa, prog_mut, prog_sim, parse_cov, feedback, detect_bugs, plot_graphs
from riscv_isa import nop_inst_bin_32
import thehuzz_utils as TU

from fuzz import *
from . import MAB_algos 


"""
Main function that runs the mabfuzzer
- Fuzzer stops when timelimit, testcase limit, or coverage % limit is reached

"""
def run_thehuzz(fuzz_time, CONFIG_PT, CONFIG_CORE_PT, CONFIG_EMU_PT, run_mode\
              , start_type_cov, input_cov_file\
              , core, emu, max_fuzz_time, max_fuzz_progs, target_cov, sim_batch_size\
              , seed_gen_interval\
              , detecting_bugs, no_threads, store_elf_file\
              , num_times_to_mut, val_muts, opc_muts\
              , feedback_cov_types, prog_gen_xargs, prog_mut_xargs, prog_sim_xargs\
              , mab_algo, mab_num_seed_arms, mab_n_picks_reset\
              , all_cov_types\
              , bug_detection_xargs, debug_print): 


    #######################################
    ########### set variables  ############
    #######################################
    input_database = TU.DATABASE(core, CONFIG_PT['all_progs_dir']\
                               , CONFIG_PT['hex_file_t'], CONFIG_PT['bin_file_t']\
                               , CONFIG_PT['riscv_file_t'], run_mode, mab_num_seed_arms) # database of input testcases
    tot_cov_points = None # total coverage points
    tot_cov_points_feedback = None # total coverage points of feedback cov type
    cov_per_ach    = 0 # percentage of coverage achieved so far 
    merged_cov_dict = None # merged coverage of all simulations
    inputs_log_file = CONFIG_PT['inputs_log_file']
    num_mutations_after_seed_gen = 0 # number of testcases generated since the
                                    # last time new seeds were added to database
    save_filetypes = ['riscv','hex'] if store_elf_file else ['hex']

    iteration_num = 0 # keeps track of how many iterations happened
    seed_mab = MAB_algos.create_mab_object(mab_algo, [mab_num_seed_arms, mab_n_picks_reset]) 

    #######################################
    ######### get user input progs ########
    #######################################
    TU.TIMELOG(fuzz_time, f" -- Loading input seeds (.hex format)", False, True) 
    if CONFIG_CORE_PT["input_format"] == 'riscv': # used for chipyard 1130
        CONFIG_PT['seed_input_file_re'] =  CONFIG_PT['seed_input_file_re'].replace("hex", "riscv")
    
    input_test_files = TU.get_files_in_dir(CONFIG_PT['input_seeds_dir'], CONFIG_PT['seed_input_file_re'])
    if run_mode == 'mabfuzz':  assert len(input_test_files) == 0, f"MABFuzz doesnt support input seed files, {input_test_files}"
    input_database.add_testcases(input_test_files, save_filetypes)
    TU.log(inputs_log_file, f"Loaded {len(input_test_files)} input seeds | Total testcases = {input_database.num_testcases()}\n", fuzz_time)
    TU.TIMELOG(fuzz_time, f" -- Loading input seeds", True, True)

    #######################################
    ############# load coverage ###########
    #######################################
    if start_type_cov == 'continue': 
        TU.TIMELOG(fuzz_time, f" -- Loading input coverage data from {input_cov_file} file", False, True)
        with open(input_cov_file, 'r') as fp: merged_cov_dict = json.load(fp)

        # update the log files
        cov_data_tot = parse_cov.full_cov_to_cov_num(merged_cov_dict)
        cov_data = { 'id': '', 'time': fuzz_time.get_time(False), 'incr': cov_data_tot, 'tot': cov_data_tot }
        with jsonlines.open(CONFIG.pt['cov_log_file'], 'a') as fp: fp.write(cov_data)
        TU.TIMELOG(fuzz_time, f" -- Loading input coverage data", True, True)

    #######################################
    ######### main loop of fuzzer #########
    #######################################
    while (fuzz_time.time_diff() < max_fuzz_time \
       and input_database.num_testcases_simulated() < max_fuzz_progs \
       and cov_per_ach < target_cov): # stopping condition of thehuzz 

        #######################################
        ############ seed generator ###########
        #######################################
        # find if there are enough testcases in database
        num_progs = sim_batch_size - input_database.num_new_testcases()
        save_filetypes = ['riscv'] if store_elf_file else [] 
        # only create new testcases for new arms
        seed_arm_ids = np.where(np.array([len(i) for i in input_database.seed_mab_new_testcases]) == 0)[0]
        num_progs = len(seed_arm_ids)
        
        # generate inputs if database doesnt have enough testcases
        if num_progs > 0:
            TU.TIMELOG(fuzz_time, f" -- Generating {num_progs} testcases")
            del_repo = 1 
            generated_test_files = prog_gen.gen_multi_prog(del_repo, run_mode, core\
                , no_threads, CONFIG_PT['gen_progs_dir'], CONFIG_PT['sw_run_dir']\
                , num_progs, prog_gen_xargs, CONFIG_PT['trash_run_dir'], debug_print)
            
            newly_added_testcases = input_database.add_testcases(generated_test_files\
                                    , save_filetypes, seed_arm_ids)

            #input_database.add_testcases(generated_test_files, save_filetypes)

            num_mutations_after_seed_gen = 0 # reset this as seeds are generated
            testcases_to_mut = []
            TU.log(inputs_log_file, f"Generated {num_progs} testcases | Total testcases = {input_database.num_testcases()}\n", fuzz_time)
            TU.TIMELOG(fuzz_time, f" -- Generating {num_progs} testcases", True)

            #need to mut to create sufficient testcases
            # mutate each seed sim_batch_size-1 times
            for testcase in newly_added_testcases: 
                seed_mab.arm_seed[testcase['seed_arm_id']] = testcase # arms need to remember seed testcase
                testcase.update({'mut_times':sim_batch_size-1})
            testcases_to_mut = input_database.allocate_testcases_to_mut(testcases_to_mut)
            num_mutations_after_seed_gen = run_muts(testcases_to_mut, prog_mut_xargs, run_mode)

        #######################################
        ############ prog simulator ###########
        #######################################
        TU.TIMELOG(fuzz_time, f" -- Running simulations")
        chosen_seed_arm = -1
        # pull arm to decide which testcase to sim
        chosen_seed_arm = int(seed_mab.select_arm())

        testcases_to_sim = input_database.get_testcases_to_sim(sim_batch_size, chosen_seed_arm)
        files_to_sim = [i['riscv_file'] for i in testcases_to_sim]
        save_ids = [i['id'] for i in testcases_to_sim]
        cov_data_dict = sim_testcases(files_to_sim, save_ids\
               , CONFIG_CORE_PT, CONFIG_EMU_PT, CONFIG_PT\
               , detecting_bugs, no_threads, core, *prog_sim_xargs)
        TU.TIMELOG(fuzz_time, f" -- Running simulations", True)
        
        #######################################
        ########## feedback analysis ##########
        #######################################
        TU.TIMELOG(fuzz_time, f" -- Analyzing coverage data")


        # merge coverage 
        merge_mode = get_merge_mode(run_mode)
        merged_cov_dict, cov_increment_dict\
          , arm_merged_cov_dict, arm_cov_increment_dict\
         = parse_cov.merge_cov_dicts(cov_data_dict, 'dict', merge_mode\
              , merged_cov_dict, fuzz_time.get_time(False)\
              , seed_mab.arm_merged_cov_dict[chosen_seed_arm])
        

        # update the cov log file
        with jsonlines.open(CONFIG_PT['cov_log_file'], 'a') as fp: 
            for cov_data in cov_increment_dict.values(): fp.write(cov_data)
        with jsonlines.open(CONFIG_PT['cov_log_file'], 'a') as fp: 
            fp.write({'itr_no': iteration_num, 'arm_id':int(chosen_seed_arm), 'num_tests': len(testcases_to_sim)})
            for i, cov_data in enumerate(arm_cov_increment_dict.values()): 
                fp.write(cov_data)

   
        testcases_to_mut, interesting_testcases, just_generated_testcases = \
            feedback.feedback_based_selection(input_database.num_new_testcases(chosen_seed_arm)\
                    , testcases_to_sim, arm_cov_increment_dict, num_times_to_mut\
                    , feedback_cov_types)
        tot_cov_incr_dict = list(cov_increment_dict.values())[-1] # cov incr dict is a dict of one dict
        tot_cov_incr = sum([tot_cov_incr_dict['incr'][cov_type] for cov_type in feedback_cov_types])
        arm_cov_incr_dict = {cov_type: sum(i['incr'][cov_type] for i in arm_cov_increment_dict.values()) for cov_type in merged_cov_dict.keys()}            
        arm_cov_incr = sum([arm_cov_incr_dict[cov_type] for cov_type in feedback_cov_types])
        if not tot_cov_points_feedback: 
            tot_cov_points_feedback = sum([len(merged_cov_dict[i]) for i in feedback_cov_types])
        seed_mab.update_arm(chosen_seed_arm, tot_cov_incr, arm_merged_cov_dict, arm_cov_incr, tot_cov_points_feedback)#, len(testcases_to_sim)==sim_batch_size)
        with jsonlines.open(CONFIG_PT['cov_log_file'], 'a') as fp: 
            fp.write({'itr_no': iteration_num, 'arm': chosen_seed_arm, 'interesting_to_mutate': interesting_testcases, 'just_gen_mutate': just_generated_testcases})
            fp.write({'itr_no': iteration_num, 'arm': chosen_seed_arm, 'counts': list(seed_mab.counts), 'values': list(seed_mab.values)})

        
        TU.TIMELOG(fuzz_time, f" -- Analyzing coverage data", True)

        print("\n\t\tMUTATION START\n")
        #######################################
        ############ prog mutation ############
        #######################################
        TU.TIMELOG(fuzz_time, f" -- Mutating testcases")
        testcases_to_mut = input_database.allocate_testcases_to_mut(testcases_to_mut)#Need help here, this function doesn't access allocate_testcases_to_mut properly 
        num_testcases_generated = run_muts(testcases_to_mut, prog_mut_xargs, run_mode)
        num_mutations_after_seed_gen += num_testcases_generated
        TU.log(inputs_log_file, f"Mutation done | Total testcases = {input_database.num_testcases()}\n", fuzz_time)
        TU.TIMELOG(fuzz_time, f" -- Mutating testcases", True)
        print("\n\t\tMUTATION END\n")

        #######################################
        ########## coverage achieved ##########
        #######################################
        if not tot_cov_points: 
            tot_cov_points = sum([len(cov_str) for cov_str in merged_cov_dict.values()]) 
        cov_points_ach = sum((parse_cov.full_cov_to_cov_num(merged_cov_dict)).values())
        cov_per_ach = round( (cov_points_ach / tot_cov_points)*100, 2 )
        TU.TIMELOG(fuzz_time, f" -- {input_database.num_testcases_simulated()} testcases, {cov_per_ach}% coverage achieved", False, True)


        # see if any arms need to be reset
        reset_arms = seed_mab.check_reset(chosen_seed_arm, input_database.num_new_testcases(chosen_seed_arm) > 0)
        for arm_info in reset_arms: input_database.seed_mab_new_testcases[arm_info[0]] = []
        if reset_arms != []:  
            with jsonlines.open(CONFIG_PT['cov_log_file'], 'a') as fp: 
                fp.write({'itr_no': iteration_num, 'arm': chosen_seed_arm, 'reset_arms': reset_arms})

        iteration_num += 1

    #######################################
    ############ log statistics ###########
    #######################################
    if merged_cov_dict: 
        tot_cov = {key: len(cov_str) for key, cov_str in merged_cov_dict.items()}
        tot_cov['total'] = sum(tot_cov.values())
        ach_cov = parse_cov.full_cov_to_cov_num(merged_cov_dict, True)
        cov_per = round( (ach_cov['total'] / tot_cov['total'])*100, 2 )
    else:  # need to run atleast one simulation to get these stats
        tot_cov = {}
        ach_cov = {}
        cov_per = 0
    stats_string  = f"\n{'-'*60}\n"
    stats_string += f"  Benchmark              : {core}\n"
    stats_string += f"  Run time               : {fuzz_time.get_time(False)} sec\n"
    stats_string += f"  No. of testcases       : {input_database.num_testcases_simulated()}\n"
    stats_string += f"  No. of coverage points : {tot_cov}\n"
    stats_string += f"  No. of points covered  : {ach_cov}\n"
    stats_string += f"  % coverage achieved    : {cov_per}%\n"
    stats_string += f"{'-'*60}\n"
    TU.TIMELOG(fuzz_time, stats_string, False, True)
    # save fuzzer real end time
    TU.TIMELOG(fuzz_time, f" EndTime: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", False, True)


    # save final coverage
    if merged_cov_dict: 
        with open(CONFIG_PT['merged_cov_file'], 'w') as fp: json.dump(merged_cov_dict, fp, indent=2)

    #######################################
    ############ bug detection ############
    #######################################
    if detecting_bugs: 
        TU.TIMELOG(fuzz_time, f" Comparing traces to detect mismatches", False, True)
        detect_bugs.detect_mismatches(*bug_detection_xargs)
        TU.TIMELOG(fuzz_time, f" Comparing traces to detect mismatches", True, True)

