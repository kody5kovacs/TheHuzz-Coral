import subprocess, os, sys, re
import numpy as np
from sklearn.preprocessing import normalize

reset_parameter = 3


"""
"""
def init_pso_variables(sim_batch_size, tot_num_muts, run_mode): 
    if run_mode == 'psofuzz': 
        num_particle = sim_batch_size # as many particles as simulations in a batch
        P, V, lbest, lbest_cov, particle_merged_cov, tot_particle_merged_cov, gbest, gbest_cov\
                = init_pos_v(num_particle, tot_num_muts) # len(val_muts)+len(opc_muts))
        saturate_cts = [0 for i in range(num_particle)] # if gbest doesnt change for 11 iteration, generate new seeds to mutate
        seeds_itr = [True for i in range(num_particle)] # skip the iteration of seed
        particle_seed_ids = [-1 for i in range(num_particle)] # maps seed ids to particles
    else: # set all variables to None or empty
        num_particle = None
        P = []
        V = None
        lbest = None
        lbest_cov = None
        particle_merged_cov = None
        tot_particle_merged_cov = None
        gbest = None
        gbest_cov = None
        saturate_cts = None
        seeds_itr = None
        particle_seed_ids = None

    return num_particle, P, V, lbest, lbest_cov, particle_merged_cov, tot_particle_merged_cov\
           , gbest, gbest_cov, saturate_cts, seeds_itr, particle_seed_ids


"""
Initialize the PSO model for mutation scheduling scheme optimization
"""
def init_pos_v(num_particle, num_mut_algo):
    # initialize particle positions and velocity
    P = np.random.randint(100, size = (num_particle, num_mut_algo))
    V = np.random.randint(low=-100, high=100, size = (num_particle, num_mut_algo))
    # normalize
    P = normalize(P, axis=1, norm='l1')
    V = normalize(V, axis=1, norm='l1')

    lbest = np.copy(P)
    lbest_cov = [{'line':0, 'branch':0, 'cond':0, 'fsm':0, 'tgl':0, 'total':0} for i in range(num_particle)]

    P_tot_cov_so_far = [None for i in range(num_particle)]
    P_tot_cov_bin = [None for i in range(num_particle)]
    
    gbest = np.copy(P[0])
    gbest_cov = {'line':0, 'branch':0, 'cond':0, 'fsm':0, 'tgl':0, 'total':0}

    return P, V, lbest, lbest_cov, P_tot_cov_so_far, P_tot_cov_bin, gbest, gbest_cov


def update_l_gbest(P_tot_cov_so_far, tar_covs:list, lbest, lbest_cov, \
                   gbest, gbest_cov, saturate_cts, P, particle_seed_ids, testcases_to_sim):
    
    particle_mut = [-1 for i in range(len(P))]

    # get index of testcase for each particle
    testcase_index_for_particle = [-1 for i in range(len(P))]
    for i, testcase in enumerate(testcases_to_sim): 
        testcase_index_for_particle[testcase['particle_id']] = i
        assert particle_seed_ids[testcase['particle_id']] == testcase['id'], f"got incorrect index for testcase {i}, {particle_seed_ids}, {testcase_index_for_particle}, {testcases_to_sim}"

    #glcov_incre = False
    for p, cov_p in enumerate(P_tot_cov_so_far):
        tar_tot_cov = 0
        lbest_tar_tot_cov = 0
        for tar_cov in tar_covs:
            tar_tot_cov += cov_p[tar_cov]
            lbest_tar_tot_cov += lbest_cov[p][tar_cov]
        if tar_tot_cov > lbest_tar_tot_cov:
            # update lbest of the particle
            lbest[p] = np.copy(P[p])
            lbest_cov[p]['line'] = cov_p['line']
            lbest_cov[p]['branch'] = cov_p['branch']
            lbest_cov[p]['cond'] = cov_p['cond']
            lbest_cov[p]['fsm'] = cov_p['fsm']
            lbest_cov[p]['tgl'] = cov_p['tgl']
            lbest_cov[p]['total'] = cov_p['total']
        else: # no local increment
            saturate_cts[p] += 1

        # get the testcase for the particle and set its mutation count
        
        if saturate_cts[p] > reset_parameter:
            particle_seed_ids[p] = -1 # removing seed id is same as reseting
            testcases_to_sim[testcase_index_for_particle[p]]['mut_times'] = 0
            particle_mut[p] = 0
        else:
            testcases_to_sim[testcase_index_for_particle[p]]['mut_times'] = 1
            particle_mut[p] = 1

    # update global best position
    for p in range(len(P)):
        lbest_tar_tot_cov = 0
        gbest_tar_tot_cov = 0
        for tar_cov in tar_covs:
            lbest_tar_tot_cov += lbest_cov[p][tar_cov]
            gbest_tar_tot_cov += gbest_cov[tar_cov]
        if lbest_tar_tot_cov > gbest_tar_tot_cov:
            gbest = np.copy(lbest[p])
            gbest_cov['line'] = lbest_cov[p]['line']
            gbest_cov['branch'] = lbest_cov[p]['branch']
            gbest_cov['cond'] = lbest_cov[p]['cond']
            gbest_cov['fsm'] = lbest_cov[p]['fsm']
            gbest_cov['tgl'] = lbest_cov[p]['tgl']
            gbest_cov['total'] = lbest_cov[p]['total']
            # glcov_incre = True

    # if glcov_incre:
    #     saturate_ct = 0
    # else:
    #     saturate_ct += 1

    # if saturate_ct > reset_parameter:
    #     reset_seed = True

    return lbest, lbest_cov, gbest, gbest_cov, saturate_cts, particle_seed_ids, testcases_to_sim, particle_mut


def update_P_V(lbest, gbest, P, V, seeds_itr, particle_seed_ids, saturate_cts, num_mut_algo):
    c = 0.5
    r1 = 0.5 # todo: random generate
    r2 = 0.5 # todo: random generate
    for p in range(len(P)):
        if particle_seed_ids[p] == -1:
            #fc.write(f'saturate ct: {saturate_cts[p]}, reset seed and position for particle {p}\n')
            saturate_cts[p] = 0
            # reset particle position and velocity
            P[p] = np.random.randint(100, size = (1, num_mut_algo))
            V[p] = np.random.randint(low=-100, high=100, size = (1, num_mut_algo))
        elif seeds_itr[p] == False:
            V[p] = c*V[p] + r1 * (lbest[p] - P[p]) + r2 * (gbest - P[p])
            P[p] = P[p] + V[p]
            # replace negative value to 0
            P[p][P[p]<0] = 0
        elif seeds_itr[p] == True:
            seeds_itr[p] = False

    # normalize # TODO: dont let the random generated values effect the
    # surviving particles when normalizing
    P = normalize(P, axis=1, norm='l1')
    V = normalize(V, axis=1, norm='l1')

    return P, V, seeds_itr, saturate_cts


##this function generates the next set of inputs for pso
#def gen_new_pso_inputs(P, progs_to_mut, gen_prog_no, f_log):
#
#    #mutate each of the program retained after feedback
#    mutation_prob = 100 #float(20) + float(80/num_progs_to_gen)
#    # print(progs_to_mut)
#    # exit()
#    progs_to_sim = []
#    
#    for p_id, prog_data in enumerate(progs_to_mut): # mutate file once
#        if prog_data is None: # skip particles that require new seeds
#            progs_to_sim.append(None)
#            continue
#
#        hex_file_in = prog_data[0]
#        file_no = str(prog_data[2])
#        if not run == 'debug':
#            mutate_pso_prog(outputs_dir, hex_file_in, gen_prog_no, mutation_prob\
#                        , nop_inst_bin_32, P, p_id, debug_print)
#        progs_to_sim.append([outputs_dir + '/' + hex_file_t.substitute( \
#                        fno = str(gen_prog_no)), 0, gen_prog_no])
#        f_log.write("Mutated " + file_no + " " + str(gen_prog_no) + f"for particle {p_id}\n")
#        gen_prog_no += 1
#    
#    return gen_prog_no, progs_to_sim


#def cal_cov_pso(cov_data, tot_cov_bins, tot_cov, sim_file_no_data, P_tot_cov_bins):
#    P_tot_cov_so_far = [{'line':0, 'branch':0, 'cond':0, 'fsm':0, 'tgl':0, 'total':0} for i in range(num_particle)]
#    tot_cov_so_far = {'line':0, 'branch':0, 'cond':0, 'fsm':0, 'tgl':0, 'total':0}
#    p_id = 0
#    tot_cov_bins_tmp = copy.deepcopy(tot_cov_bins)
#    incremental_cov_data_frm_fn = []
#    for cov_data_i, file_no in zip(cov_data, sim_file_no_data):
#        bins = cov_data_i # note that the data is stored as char
#        tot_cov_so_far['total'] = 0
#        if tot_cov_bins == []: # first cov bin, so directly copy data
#            tot_cov_bins = [ord(b) for b in bins]
#            #tot_cov_bins_tmp = copy.deepcopy(tot_cov_bins)
#        if P_tot_cov_bins[p_id] == []:
#            P_tot_cov_bins[p_id] = [ord(b) for b in bins]
#        i = 0
#        for cov_type in cov_types:
#            tot_cov_so_far[cov_type] = 0
#            for j in range(no_cov_points[cov_type]):
#                k = i + j  #this is the index from cov point array
#                value = 1 if P_tot_cov_bins[p_id][k] or ord(bins[k]) else 0
#                P_tot_cov_bins[p_id][k] = value
#                P_tot_cov_so_far[p_id][cov_type] = (P_tot_cov_so_far[p_id][cov_type]+1) if value else P_tot_cov_so_far[p_id][cov_type]
#                value_merge = 1 if tot_cov_bins[k] or ord(bins[k]) else 0
#                tot_cov_bins[k] = value_merge
#                tot_cov_so_far[cov_type] = (tot_cov_so_far[cov_type]+1) if value_merge else tot_cov_so_far[cov_type]
#            P_tot_cov_so_far[p_id]['total'] += P_tot_cov_so_far[p_id][cov_type]
#            tot_cov_so_far['total'] += tot_cov_so_far[cov_type]
#            i = k+1 # update num of tot cov points till this cov type
#        p_id += 1
#        cov_incr = tot_cov_so_far['total'] - tot_cov
#        tot_cov = tot_cov_so_far['total']
#        prog_cov_data = [cov_incr, file_no, 0, tot_cov, 0, 0]
#        for cov_type in cov_types:
#            prog_cov_data.append(tot_cov_so_far[cov_type])
#        incremental_cov_data_frm_fn.append(prog_cov_data)
#
#    assert p_id == num_particle, f"cal_cov_pso: the coverage of each particle has issue {p_id}."
#
#    #log the coverages
#    f_cov_log = open(cov_log_path, 'a')
#    for cov_data in incremental_cov_data_frm_fn:
#        incr_cov = str(cov_data[0])
#        file_no = str(cov_data[1])
#        tot_cov = str(cov_data[3])
#        cov_type_data = ''
#        if len(cov_data) > 6: 
#            for i in range(6, len(cov_data)): 
#                cov_type_data += ','
#                cov_type_data += str(cov_data[i])
#        f_cov_log.write(file_no + "," + incr_cov + "," + tot_cov + cov_type_data + "\n")
#
#    f_cov_log.close()
#    # print(cov_P)
#    #return cov_P, tot_cov_so_far, tot_cov_bins
#    return P_tot_cov_so_far, P_tot_cov_bins, tot_cov_so_far, tot_cov_bins