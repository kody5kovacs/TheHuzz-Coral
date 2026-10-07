"""
Created by: Rahul Kande
This script is used to generate testcases
- Notes: 

- TODOs: 
"""

#Imports
import subprocess, os, random, sys, re
import uuid
from tqdm import tqdm

import thehuzz_utils


def gen_multi_prog( del_repo, mode, core\
                        , no_threads, inst_output_path, sw_dir\
                        , num_progs, prog_gen_xargs\
                        , trash_dir='/tmp/', debug_print=False):

    inst_output_path_name = os.path.basename(inst_output_path)
    generated_test_files = [] # record all generated test files

    #print(inst_output_path, inst_dump_path)
    if del_repo:
        thehuzz_utils.delete_dir(inst_output_path, True, 'move', f"{trash_dir}/prog_gen_{uuid.uuid1()}")
    
    for prog_no in range(num_progs):
        #open file
        file_name = f'inst_file_{prog_no}.c' 
        file_fullpath = os.path.join(inst_output_path, file_name)
        file_p = open(file_fullpath, 'w')
        generated_test_files.append(thehuzz_utils.change_extension(file_fullpath, 'hex'))
   
        if (mode == 'random'):
            gen_random_prog(file_p, *prog_gen_xargs)
        elif (mode in ['thehuzz']):
            gen_fuzzer_prog(file_p, *prog_gen_xargs, mode)
        elif(mode in ['mabfuzz']):
            gen_fuzzer_prog(file_p, *prog_gen_xargs, mode)
        elif(mode in ['psofuzz']):
            gen_fuzzer_prog(file_p, *prog_gen_xargs, mode)
        else:
            print("Unknown mode received", mode)
            exit()

    make_silent = " " if debug_print else " -s "
    multicore_make = f" -j {no_threads} "
    
    compile_cmd = f'cd {sw_dir}; make {make_silent} compile_all {multicore_make} C_DIR={inst_output_path}; cd - > /dev/null'
    
    subprocess.call(compile_cmd, shell=True)

    return generated_test_files


def gen_random_prog(file_p, num_inst_in_prog, opcode_list, inst_list_all_w_ext\
                    , num_nops_at_start, num_nops_at_end\
                    , core, first_opcode_list=[]):
    
    #write to file
    write_c_frame_start(file_p, num_nops_at_start, core=core, mode='random')
    #RVV: vtype resets to vill, so every vector inst traps until a vsetvli runs.
    #first_opcode_list is picked at random, so it cannot be relied on to put one
    #first. emit it unconditionally whenever vector insts are in the pool.
    if any(inst_list_all_w_ext[o][1].startswith('v') for o in opcode_list):
        write_asm(vec_prologue_inst(fixed=True), file_p)
    
    #create instructions
    for j in range(num_inst_in_prog):
        inst_op = random.choice(opcode_list)
        inst_data = inst_list_all_w_ext[inst_op]
        inst = create_inst(inst_op[0], inst_data, core, file_p, 'rand')
        write_asm(inst, file_p) #write inst to file
    
    write_c_frame_end(file_p, num_nops_at_end)
    
    #close file
    file_p.close()


"""
- For normal fuzzer, generate half insts with opcodes that wont casuse issues, 
    rest half is random
"""
def gen_fuzzer_prog(file_p, num_inst_in_prog, opcode_list, inst_list_all_w_ext\
                    , num_nops_at_start, num_nops_at_end, first_opcode_list\
                    , core, mode):
    #write to file
    write_c_frame_start(file_p, num_nops_at_start, mode=mode, core=core)
    #RVV: vtype resets to vill, so every vector inst traps until a vsetvli runs.
    #first_opcode_list is picked at random, so it cannot be relied on to put one
    #first. emit it unconditionally whenever vector insts are in the pool.
    if any(inst_list_all_w_ext[o][1].startswith('v') for o in opcode_list):
        write_asm(vec_prologue_inst(fixed=True), file_p)
    
    # determine the sequence of instructions
    # first half will be simple insts and rest will be all insts
    op_seq = [random.choice(first_opcode_list) for i in range( int(num_inst_in_prog/2) )] 
    op_seq += [random.choice(opcode_list) for i in range(num_inst_in_prog - int(num_inst_in_prog/2))]

    # create the insts from the sequence
    inst_seq = []
    for op in op_seq: 
        inst_data = inst_list_all_w_ext[op]
        write_asm(create_inst(op[0], inst_data, core, file_p, 'fuzz'), file_p)
    
    write_c_frame_end(file_p, num_nops_at_end)
    
    #close file
    file_p.close()


#Writes C start framework into program file (like int main, libraries, ect)
def write_c_frame_start(f_inst, num_nops_at_start, core, mode='thehuzz'):
    #input: none
    #ouput: writes to program file
    # select a random nop to insert label for branch insts
    inst_no = random.randint(0,num_nops_at_start-1)
    line = '#include <stdio.h>\n#include <stdint.h>\n\nint main(void)\n{\n'
    
    for i in range(0,num_nops_at_start): #add 4 nop instructions
        if i == inst_no:
            line = line + 'asm volatile ( "L_b_non_prof: ADDI x0, x0, 0" );\n'
        else:
            line = line + 'asm volatile ( "ADDI x0, x0, 0" );\n'

    f_inst.write(line + "\n")


#Writes C end framework into program file (return 0, ect)
def  write_c_frame_end(f_inst, num_nops_at_end):
    #input: none
    #ouput: writes to program file
    line = ""
    for i in range(0,num_nops_at_end): #add nop instructions
        line = line + 'asm volatile ( "ADDI x0, x0, 0" );\n' 

    line = line + '\nreturn 0;\n}'
    f_inst.write(line + "\n")
    

#---------------------------------------------------------------------------
# RVV (Zve32x) operand generation
#---------------------------------------------------------------------------
# vtype fields that are legal to encode. an illegal SEW/LMUL combination sets
# vill and makes every following vector inst trap, which is a legitimate fuzz
# target, but it is NOT something the assembler will reject - it assembles fine
# and fails at run time. keep the illegal combos here if you want them.
VEC_SEW  = ['e8', 'e16', 'e32']
VEC_LMUL = ['mf8', 'mf4', 'mf2', 'm1', 'm2', 'm4', 'm8']
VEC_TA   = ['ta', 'tu']
VEC_MA   = ['ma', 'mu']

def _vreg(align=1):
    #align: whole-register insts require vd/vs2 to be a multiple of nr, and GAS
    #       rejects a misaligned one at assemble time
    return "v" + str(random.randrange(0, 32, align))

def _xreg():
    return "x" + str(random.randint(0,31))

def _vimm():
    # .vi forms are signed 5-bit on some insts (vadd.vi: -16..15) and unsigned
    # 5-bit on others (vsll.vi, vrgather.vi, vnclip.wi: 0..31). 0..15 is the
    # intersection, so it assembles for every .vi inst in the table.
    return str(random.randint(0,15))

def _vtypei():
    return (random.choice(VEC_SEW) + "," + random.choice(VEC_LMUL) + ","
            + random.choice(VEC_TA) + "," + random.choice(VEC_MA))

def _vm():
    # ", v0.t" makes the inst masked (vm=0). half the time, unmasked.
    return random.choice(["", ", v0.t"])

def _nr_from_name(inst_op):
    # VMV2R.V -> 2, VL4RE16.V -> 4, VS8R.V -> 8
    m = re.match(r'^VMV(\d)R\.V$|^VL(\d)RE\d+\.V$|^VS(\d)R\.V$', inst_op)
    if not m:
        return 1
    return int([g for g in m.groups() if g][0])


#create a vector instruction operand string
#input:  inst_op  - mnemonic as it appears in riscv_isa.rvv (upper case)
#        i_type   - format token, field 1 of the rvv dict entry
#output: full assembly string, or None if the format token is unknown
def create_vec_inst(inst_op, i_type):
    nr = _nr_from_name(inst_op)

    #--- configuration ---
    if i_type == 'vcfg':                                    #vsetvli rd, rs1, vtypei
        return inst_op + " " + _xreg() + "," + _xreg() + "," + _vtypei()
    if i_type == 'vcfgi':                                   #vsetivli rd, uimm, vtypei
        return inst_op + " " + _xreg() + "," + str(random.randint(0,31)) + "," + _vtypei()
    if i_type == 'vcfgr':                                   #vsetvl rd, rs1, rs2
        return inst_op + " " + _xreg() + "," + _xreg() + "," + _xreg()

    #--- OP-V arithmetic, maskable ---
    if i_type == 'vvv':                                     #vd, vs2, vs1, vm
        return inst_op + " " + _vreg() + "," + _vreg() + "," + _vreg() + _vm()
    if i_type == 'vvx':                                     #vd, vs2, rs1, vm
        return inst_op + " " + _vreg() + "," + _vreg() + "," + _xreg() + _vm()
    if i_type == 'vxv':                                     #vd, rs1, vs2, vm (vmacc/vwmacc .vx)
        return inst_op + " " + _vreg() + "," + _xreg() + "," + _vreg() + _vm()
    if i_type == 'vvi':                                     #vd, vs2, imm, vm
        return inst_op + " " + _vreg() + "," + _vreg() + "," + _vimm() + _vm()

    #--- OP-V arithmetic, vm hardwired to 1 (no mask operand allowed) ---
    if i_type == 'vvvn':
        return inst_op + " " + _vreg() + "," + _vreg() + "," + _vreg()
    if i_type == 'vvxn':
        return inst_op + " " + _vreg() + "," + _vreg() + "," + _xreg()
    if i_type == 'vvin':
        return inst_op + " " + _vreg() + "," + _vreg() + "," + _vimm()

    #--- carry/borrow and merge: v0 is an explicit operand, vm must be 0 ---
    if i_type == 'vvvm':
        return inst_op + " " + _vreg() + "," + _vreg() + "," + _vreg() + ",v0"
    if i_type == 'vvxm':
        return inst_op + " " + _vreg() + "," + _vreg() + "," + _xreg() + ",v0"
    if i_type == 'vvim':
        return inst_op + " " + _vreg() + "," + _vreg() + "," + _vimm() + ",v0"

    #--- whole-vector move (2 operands, vm hardwired to 1) ---
    if i_type == 'vmvv':
        return inst_op + " " + _vreg() + "," + _vreg()
    if i_type == 'vmvx':
        return inst_op + " " + _vreg() + "," + _xreg()
    if i_type == 'vmvi':
        return inst_op + " " + _vreg() + "," + _vimm()

    #--- loads and stores ---
    # NOTE: the base address in rs1 is whatever junk happens to be in that
    # register. that is the same thing the existing 's'/'Loads' paths do, and
    # it is why LH/LW/SH/SW sit in inst_sim_issue_1.
    if i_type == 'vld':                                     #vd, (rs1), vm
        return inst_op + " " + _vreg() + ",(" + _xreg() + ")" + _vm()
    if i_type == 'vst':                                     #vs3, (rs1), vm
        return inst_op + " " + _vreg() + ",(" + _xreg() + ")" + _vm()
    if i_type in ('vlds', 'vsts'):                          #vd, (rs1), rs2, vm
        return inst_op + " " + _vreg() + ",(" + _xreg() + ")," + _xreg() + _vm()
    if i_type in ('vldi', 'vsti'):                          #vd, (rs1), vs2, vm
        return inst_op + " " + _vreg() + ",(" + _xreg() + ")," + _vreg() + _vm()
    if i_type in ('vldr', 'vstr'):                          #vd, (rs1) - no mask (also vlm.v/vsm.v, nr=1)
        return inst_op + " " + _vreg(nr) + ",(" + _xreg() + ")"

    #--- mask and permutation ---
    if i_type == 'vldw':                                    #vd, vs2, vm
        return inst_op + " " + _vreg() + "," + _vreg() + _vm()
    if i_type == 'vrd':                                     #rd, vs2, vm
        return inst_op + " " + _xreg() + "," + _vreg() + _vm()
    if i_type == 'vmm':                                     #vd, vs2, vs1 - no mask
        return inst_op + " " + _vreg() + "," + _vreg() + "," + _vreg()
    if i_type == 'vd1':                                     #vd, vm
        return inst_op + " " + _vreg() + _vm()
    if i_type == 'vxs':                                     #rd, vs2
        return inst_op + " " + _xreg() + "," + _vreg()
    if i_type == 'vsx':                                     #vd, rs1
        return inst_op + " " + _vreg() + "," + _xreg()
    if i_type == 'vwr':                                     #vd, vs2, both aligned to nr
        return inst_op + " " + _vreg(nr) + "," + _vreg(nr)

    #--- mask pseudo-ops ---
    if i_type == 'vm1':                                     #vd, vs2
        return inst_op + " " + _vreg() + "," + _vreg()
    if i_type == 'vm0':                                     #vd
        return inst_op + " " + _vreg()

    return None


#emit a vsetvli that makes vtype valid, so the vector insts that follow do not
#all trap on vill. rd != x0 and rs1 == x0 means "set vl to VLMAX".
def vec_prologue_inst(fixed=True):
    if fixed:
        return "VSETVLI x5,x0,e32,m1,ta,ma"
    return "VSETVLI " + _xreg() + ",x0," + _vtypei()


#create instruction
#output: instruction string
def create_inst(inst_op, inst_data, core, f_inst=None, run_type ='fuzz', src1='NONE'):
    from riscv_isa import priv_reg 
    key = inst_data[0]
    inst = inst_op
    i_type = inst_data[1]

    #RVV: every vector format token starts with 'v'. handle them separately,
    #the scalar operand code below does not know about vector registers.
    if i_type.startswith('v'):
        vec_inst = create_vec_inst(inst_op, i_type)
        if vec_inst is None:
            print("ERROR: unknown vector format type:", i_type, "for", inst_op)
            exit()
        return vec_inst

    if i_type == 'r': 
        dest = "x" + str(random.randint(0,31))
        src1 = "x" + str(random.randint(0,31))

        if key == 'Shifts' and (inst[-1]=='I' or inst[-2:]=='IW'):
            src2 = str(random.randint(0,31)) #src2 is shift amt
        else:
            src2 = "x" + str(random.randint(0,31))

        inst = inst + " " + dest + "," + src1 + "," + src2

    if i_type == 'r1': #64 bit shifts
        dest = "x" + str(random.randint(0,31))
        src1 = "x" + str(random.randint(0,31))
        src2 = str(random.randint(0,63)) #src2 is shift amt
        inst = inst + " " + dest + "," + src1 + "," + src2

    if i_type == 'r2': 
        dest = "x" + str(random.randint(0,31))
        src1 = "x" + str(random.randint(0,31))
        src2 = "x" + str(random.randint(0,31))

        atomic_type = random.choice(['', '.AQ', '.RL'])
        inst = inst + atomic_type

        if key == 'Load Reserved': #lr.w t0, (a0)
            inst = inst + " " + dest + "," + "(" + src1 + ")"
        else:  #sc.w a0, a2, (a0)
            inst = inst + " " + dest + "," + src1 + "," + "(" + src2 + ")"

    elif i_type == 'i': 
        dest = "x" + str(random.randint(0,31))
        if key == 'CSR Access': #handles operand variation in case of privileged instruction
            if src1 == 'NONE': #use the same src1 if already provided
                src1 = random.choice(priv_reg)
        else:
            src1 = "x" + str(random.randint(0,31))

        if inst in ['CSRRW', 'CSRRS', 'CSRRC']: 
            imm = "x" + str(random.randint(0,31)) #its reg not imm in this case
        elif inst in ['CSRRWI', 'CSRRSI', 'CSRRCI']: 
            imm = str(random.randint(0,31))
        else:
            imm = str(random.randint(-2048,2047)) 

        if (key == 'Counters'):
            inst = inst + " " + dest
        elif (key == 'Loads'):
            inst = inst + " " + dest + ", " + imm + "(" + src1 + ")"
        else: 
            inst = inst + " " + dest + "," + src1 + "," + imm

    elif i_type == 'i1':  #FENCE inst
        arg1 = random.choice(['','i']) + random.choice(['','o'])\
               + random.choice(['','r']) + random.choice(['','w'])
        if arg1 != '':
            arg1 = ' ' + arg1
        arg2 = random.choice(['','i']) + random.choice(['','o'])\
               + random.choice(['','r']) + random.choice(['','w'])
        if arg1 == '' or arg2 == '': #either both should be there or none
            arg1 = ''
            arg2 = ''
        elif arg2 != '': #arg1 is there, so add comma if arg2 is there
            arg2 = ' ,' + arg2

        inst = inst + arg1 + arg2

    elif i_type == 'i2': 
        inst = inst

    elif i_type in ['u','j']: #j&u-type
        dest = "x" + str(random.randint(0,31))
        imm = str(random.randint(0,1048575)) 
        if (inst == 'JAL'):
            imm = str(random.randint(int("800010d0",16),int("80001f50",16)))
            imm = str(int(int(int(imm)/2)*2)) # make sure no 0 in lsb place fr addr offset
            inst = inst + " " + dest + "," + imm
        else:
            inst = inst + " " + dest + "," + imm

    elif i_type == 's': #s-type
        safe_store = 0 #set to 1 to allow generator add instruction that writes valid address to register
        src1 = "x" + str(random.randint(0,31))
        src2 = "x" + str(random.randint(0,31))
        dest = "x" + str(random.randint(0,31))
        if inst == 'SB' and safe_store: #sets base address stored in rs1 to be valid 
            imm_temp = str(2047)
            inst_temp = "ADDI "+src1+", x0, "+imm_temp
            
            if f_inst == None:
                print("***Warning: unable to do safe_store")
            else:
                write_asm(inst_temp, f_inst) #write inst to file
            imm = str(2047) 
        else:
            imm = str(random.randint(-2048,2047)) 
            
        #inst = inst + " " + src1 + "," + src2 + "," + imm
        inst = inst + " " + dest + ", " + imm + "(" + src1 + ")"

    elif i_type == 'b': #b-type
        dest = "x" + str(random.randint(0,31))
        src1 = "x" + str(random.randint(0,31))
        src2 = "x" + str(random.randint(0,31))
        # main starts at 80001720, the instrn can be 1724 to 18cc
        # we can go from 18cc - 800 to 1754 + 7ff = 800010cc to 1f53
        imm = str(random.randint(int("800010d0",16),int("80001f50",16)))
        imm = str(int(int(int(imm)/2)*2)) # make sure no 0 in lsb place fr addr offset
        if (run_type == 'prof'): # do this only for profiling
            inst = inst + " " + src1 + "," + src2 + "," + "L_b"
            # pick an rand offset
            imm = random.randint(0,127)
            for i in range(0,128):
                if i == imm:
                    label = "L_b: "
                else:
                    label = ""
                f_inst.write("\n")
                line = 'asm volatile ( "' + label + ' ADDI x0, x0, 0" );'
                f_inst.write(line)
        elif run_type == 'fuzz':
            inst = inst + " " + src1 + "," + src2 + "," + "L_b_non_prof"
        elif run_type == 'rand':
            inst = inst + " " + src1 + "," + src2 + "," + imm
        else:   
            print("ERROR: unknown run type found: ", run_type)
            print(inst_op, inst_data)
            exit()

        f_inst.write("\n")
              
        #inst = inst + " " + dest + "," + src1 + "," + src2
        
    return inst


#writes assembly into asm volatile block of C file
def write_asm(inst, f_inst):
    #input: string of assembly instruction
    #output: writes to program file

    line = 'asm volatile ( "' + inst + '" );'
    f_inst.write(line + "\n")

def cmp_inst(exp_inst, result_inst):
    if len(exp_inst) != len(result_inst):
        return 0

    for exp_c, result_c in zip(exp_inst, result_inst):
        if not (exp_c == 'x' or (exp_c == result_c)):
            return 0
    return 1


#create a program with all the instrns
def create_prog_with_all_insts(del_repo, inst_output_path_name\
                               , inst_output_path, inst_dump_path\
                               , inst_list):
    #remove old seed files
    if del_repo:
        subprocess.call("rm -r " + inst_output_path,shell=True)
        subprocess.call("mkdir " + inst_output_path,shell=True)
        subprocess.call("rm -r " + inst_dump_path,shell=True)
    
    file_name = inst_output_path + "inst_file_0_itr_0.c"
    f_inst = open("./" + file_name,'w')
    #write to file
    write_c_frame_start(f_inst)
    for inst_op, inst_data in inst_list.items():
        #create instruction
        inst = create_inst(inst_op, inst_data,core,f_inst)
        write_asm(inst, f_inst) #write inst to file
    
    write_c_frame_end(f_inst)
    
    #close file
    f_inst.close()
    subprocess.call("make " + file_name.split('.c')[0],shell=True)


#generate program files per instrn:
def gen_all_inst_files(del_repo, check_all_prog_files\
                       , inst_output_path \
                       , num_inst_in_prog, num_itr_per_inst, inst_list\
                       , num_nops_at_start, num_nops_at_end\
                       , sw_dir, nop_inst_bin_32, no_threads=1\
                       , trash_dir='/tmp/', debug_print=False):
   
    #remove old seed files
    if del_repo:
        thehuzz_utils.delete_dir(inst_output_path, True, 'move', f"{trash_dir}/prog_gen_{uuid.uuid1()}")

    #generate and write instruction files
    op_cnt = 0
    for inst_op, inst_data in tqdm(inst_list.items(), desc="----Generating programs"):
        for itr_cnt in range(num_itr_per_inst):
            #print (inst_grp, inst_type[0])
            
            #open file
            file_name = "inst_file_" + str(op_cnt) + "_itr_" + str(itr_cnt)\
                        + ".c" 
            f_inst = open(os.path.join(inst_output_path, file_name),'w')
    
    
            #write to file
            write_c_frame_start(f_inst, num_nops_at_start)
    
            #create instruction
            #inst = create_inst(inst_op, inst_data)
            if str(inst_data[6]) == "1": # generate only 1 inst for this inst opcode
                num_inst_in_prog_local = 1
            else: 
                num_inst_in_prog_local = num_inst_in_prog

            for j in range(num_inst_in_prog_local):
                inst = create_inst(inst_op[0], inst_data,core,f_inst, 'prof')
                write_asm(inst, f_inst) #write inst to file
    
            write_c_frame_end(f_inst, num_nops_at_end)
    
            #close file
            f_inst.close()
        
        op_cnt = op_cnt + 1
  
    make_silent = " " if debug_print else " -s "
    print("----compiling programs")
    multicore_make = f" -j {no_threads} "
    compile_cmd = f'cd {sw_dir}; make {make_silent} compile_all {multicore_make} C_DIR={inst_output_path}; cd - > /dev/null'
    subprocess.call(compile_cmd, shell=True)
    print("----compiling programs done")

    #check if all instrns are generated properly
    print("----checking generated programs")
    if check_all_prog_files:
        op_cnt = 0
        error = 0
        for inst_op, inst_data in inst_list.items():

            # TODO: adjust checking for branch insts as they have more nops
            if inst_op[0] in ['BEQ', 'BNE', 'BLT', 'BGE', 'BLTU', 'BGEU']: 
                op_cnt = op_cnt + 1
                continue

            if str(inst_data[6]) == "1": # generate only 1 inst for this inst opcode
                num_inst_in_prog_local = 1
            else: 
                num_inst_in_prog_local = num_inst_in_prog

            num_inst_in_main = num_nops_at_start + num_inst_in_prog_local \
                               + num_nops_at_end
            op_bin = inst_data[4]
            funct3_bin = inst_data[3]
            funct7_bin = inst_data[2]
            exp_inst = funct7_bin + "x"*10 + funct3_bin + "x"*5 + op_bin
            exp_inst_list = [nop_inst_bin_32]*num_nops_at_start\
                            + [exp_inst]*num_inst_in_prog_local\
                            + [nop_inst_bin_32]*num_nops_at_end
            error = 0
            for itr_cnt in range(num_itr_per_inst):
    
                #open file
                file_name = "inst_file_" + str(op_cnt) + "_itr_" + str(itr_cnt)\
                            + ".riscv.dump" 
                try:
                    f_inst = open(os.path.join(inst_output_path,file_name),'r')
                except FileNotFoundError :
                    print("couldnt find file:" , op_cnt, inst_op, itr_cnt)
                    error = 1
                    break
        
                inside_main = 0
                result_inst_list = []
                inst_main_cnt = 0
                f_inst_lines = f_inst.readlines()
                for line in f_inst_lines:
                    if inside_main == 0: #yet to reach main section
                        if re.match("[0-9a-f]* <main>:", line): #found main
                            inside_main = 1
                        continue
                  
                    # inside main function, there could be instructions, empty
                    # lines, labels, etc. filter out only instructions
                    inst_re = "[^0-9a-f]*[0-9a-f]+:[^0-9a-f]+([0-9a-f]+)"
                    if not re.match(inst_re, line):
                        continue
                        #print("couldnt find instrn in file:"\
                        #       , op_cnt, inst_op, itr_cnt, line)
                        #error = 1

                    result_inst = re.match(inst_re, line).group(1)
                    if len(result_inst) == 4:
                        result_inst = "{0:016b}".format(int(result_inst, 16))
                    else:
                        result_inst = "{0:032b}".format(int(result_inst, 16))
                    result_inst_list.append(result_inst) 
                    inst_main_cnt = inst_main_cnt + 1
                    if inst_main_cnt == num_inst_in_main:
                        break
    
                #close file
                f_inst.close()
    
                #check the instrns
                if error:
                    break
                if inst_main_cnt != num_inst_in_main:
                    print("couldnt find enough instrns in file:"\
                           , op_cnt, inst_op, itr_cnt)
                    error = 1 
                    break
    
                for result_inst,exp_inst in zip(result_inst_list,exp_inst_list):
                    #print(result_inst, exp_inst)
                    if not cmp_inst(exp_inst, result_inst):
                        print("inst not matching in file:"\
                              , op_cnt, inst_op, itr_cnt, result_inst, exp_inst\
                              , "{0:08x}".format(int(result_inst,2)) )
                        error = 1
                        break
                if error:
                    break
            
            op_cnt = op_cnt + 1
    print("----checking generated programs done")
