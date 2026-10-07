#this file lists all the RISC-V instructions and their formats

##instructions are grouped based on the structure of their  mnemonics
#inst_format_dict = { "r"  : 0, "r1" : 1, "r2" : 2
#                    ,"i"  : 3, "i1" : 4, "i2" : 5 
#                    ,"u"  : 6, "s"  : 7, "b"  : 8 
#                    ,"j"  : 9 }

##instruction types/names based on their functionality i
#    (should have called this name)
#inst_type_dict = { 
#        "Arithmetic" : 0,    "Jump & Link" : 1, "Branches" : 2,  "Loads" : 3\
#       ,"Stores" : 4,        "Compare" : 5,     "Logical" : 6,   "Shifts" : 7\
#       ,"Sync" : 8,          "System" : 9,      "CSR Access" : 10\
#       ,"Multiply" : 11,     "Divide" : 12,     "Remainder" : 13\
#       ,"Load Reserved" : 14,"Store Cond" : 15, "Swap Atomic":16\
#       ,"Add Atomic" : 17,   "Logical Atomic" : 18,    "Min/Max Atomic":19 }



#RV32I extension instructions and their formats:
#rv32i dict:
#  key: instruction in assembly language
#  value: [0:instrn type, 1:instrn format type, 2:bits[], 3:bits[], \
#          4:bits[],      5:extension,  \
#          6:single_inst_run/multi_inst_run(for profiling), \
#          7:clone_no(for profiling)]
#note: 
#  - fence .i wont match with table in spec, see section 2.7 
rv32i = {
        "LUI"    : [ "Arithmetic" , "u" , "xxxxxxx", "xxx", "0110111", "RV32I", "0", 300 ],
        "AUIPC"  : [ "Arithmetic" , "u" , "xxxxxxx", "xxx", "0010111", "RV32I", "0", 301 ],
        "JAL"    : [ "Jump & Link", "j" , "xxxxxxx", "xxx", "1101111", "RV32I", "1", 302 ],
        "JALR"   : [ "Jump & Link", "i" , "xxxxxxx", "000", "1100111", "RV32I", "1", 303 ],
        "BEQ"    : [ "Branches"   , "b" , "xxxxxxx", "000", "1100011", "RV32I", "1", 304 ],
        "BNE"    : [ "Branches"   , "b" , "xxxxxxx", "001", "1100011", "RV32I", "1", 305 ],
        "BLT"    : [ "Branches"   , "b" , "xxxxxxx", "100", "1100011", "RV32I", "1", 306 ],
        "BGE"    : [ "Branches"   , "b" , "xxxxxxx", "101", "1100011", "RV32I", "1", 307 ],
        "BLTU"   : [ "Branches"   , "b" , "xxxxxxx", "110", "1100011", "RV32I", "1", 308 ],
        "BGEU"   : [ "Branches"   , "b" , "xxxxxxx", "111", "1100011", "RV32I", "1", 309 ],
        "LB"     : [ "Loads"      , "i" , "xxxxxxx", "000", "0000011", "RV32I", "0", 310 ],
        "LH"     : [ "Loads"      , "i" , "xxxxxxx", "001", "0000011", "RV32I", "1", 311 ],
        "LW"     : [ "Loads"      , "i" , "xxxxxxx", "010", "0000011", "RV32I", "1", 312 ],
        "LBU"    : [ "Loads"      , "i" , "xxxxxxx", "100", "0000011", "RV32I", "0", 313 ],
        "LHU"    : [ "Loads"      , "i" , "xxxxxxx", "101", "0000011", "RV32I", "1", 314 ],
        "SB"     : [ "Stores"     , "s" , "xxxxxxx", "000", "0100011", "RV32I", "1", 315 ],
        "SH"     : [ "Stores"     , "s" , "xxxxxxx", "001", "0100011", "RV32I", "1", 316 ],
        "SW"     : [ "Stores"     , "s" , "xxxxxxx", "010", "0100011", "RV32I", "1", 317 ],
        "ADDI"   : [ "Arithmetic" , "i" , "xxxxxxx", "000", "0010011", "RV32I", "0", 318 ],
        "SLTI"   : [ "Compare"    , "i" , "xxxxxxx", "010", "0010011", "RV32I", "0", 319 ],
        "SLTIU"  : [ "Compare"    , "i" , "xxxxxxx", "011", "0010011", "RV32I", "0", 500 ],
        "XORI"   : [ "Logical"    , "i" , "xxxxxxx", "100", "0010011", "RV32I", "0", 501 ],
        "ORI"    : [ "Logical"    , "i" , "xxxxxxx", "110", "0010011", "RV32I", "0", 502 ],
        "ANDI"   : [ "Logical"    , "i" , "xxxxxxx", "111", "0010011", "RV32I", "0", 503 ],
        "SLLI"   : [ "Shifts"     , "r" , "0000000", "001", "0010011", "RV32I", "0", 504 ],
        "SRLI"   : [ "Shifts"     , "r" , "0000000", "101", "0010011", "RV32I", "0", 505 ],
        "SRAI"   : [ "Shifts"     , "r" , "0100000", "101", "0010011", "RV32I", "0", 506 ],
        "ADD"    : [ "Arithmetic" , "r" , "0000000", "000", "0110011", "RV32I", "0", 507 ],
        "SUB"    : [ "Arithmetic" , "r" , "0100000", "000", "0110011", "RV32I", "0", 508 ],
        "SLL"    : [ "Shifts"     , "r" , "0000000", "001", "0110011", "RV32I", "0", 509 ],
        "SLT"    : [ "Compare"    , "r" , "0000000", "010", "0110011", "RV32I", "0", 510 ],
        "SLTU"   : [ "Compare"    , "r" , "0000000", "011", "0110011", "RV32I", "0", 511 ],
        "XOR"    : [ "Logical"    , "r" , "0000000", "100", "0110011", "RV32I", "0", 512 ],
        "SRL"    : [ "Shifts"     , "r" , "0000000", "101", "0110011", "RV32I", "0", 513 ],
        "SRA"    : [ "Shifts"     , "r" , "0100000", "101", "0110011", "RV32I", "0", 514 ],
        "OR"     : [ "Logical"    , "r" , "0000000", "110", "0110011", "RV32I", "0", 515 ],
        "AND"    : [ "Logical"    , "r" , "0000000", "111", "0110011", "RV32I", "0", 516 ],
        "FENCE"  : [ "Sync"       , "i1", "0000xxx", "000", "0001111", "RV32I", "0", 517 ],
        "FENCE.I": [ "Sync"       , "i2", "xxxxxxx", "001", "0001111", "RV32I", "1", 118 ],
        "ECALL"  : [ "System"     , "i2", "0000000", "000", "1110011", "RV32I", "1", 119 ],
        "EBREAK" : [ "System"     , "i2", "0000000", "000", "1110011", "RV32I", "1", 100 ],
        "CSRRW"  : [ "CSR Access" , "i" , "xxxxxxx", "001", "1110011", "RV32I", "1", 101 ],
        "CSRRS"  : [ "CSR Access" , "i" , "xxxxxxx", "010", "1110011", "RV32I", "1", 102 ],
        "CSRRC"  : [ "CSR Access" , "i" , "xxxxxxx", "011", "1110011", "RV32I", "1", 103 ],
        "CSRRWI" : [ "CSR Access" , "i" , "xxxxxxx", "101", "1110011", "RV32I", "1", 104 ],
        "CSRRSI" : [ "CSR Access" , "i" , "xxxxxxx", "110", "1110011", "RV32I", "1", 105 ],
        "CSRRCI" : [ "CSR Access" , "i" , "xxxxxxx", "111", "1110011", "RV32I", "1", 106 ]
        }

rv64i = {
        "LWU"   : [ "Loads"     , "i" , "xxxxxxx", "110", "0000011", "RV64I", "1", 107 ],
        "LD"    : [ "Loads"     , "i" , "xxxxxxx", "011", "0000011", "RV64I", "1", 108 ],
        "SD"    : [ "Stores"    , "s" , "xxxxxxx", "011", "0100011", "RV64I", "1", 109 ],
        "SLLI"  : [ "Shifts"    , "r1", "000000x", "001", "0010011", "RV64I", "0", 600 ],
        "SRLI"  : [ "Shifts"    , "r1", "000000x", "101", "0010011", "RV64I", "0", 601 ],
        "SRAI"  : [ "Shifts"    , "r1", "010000x", "101", "0010011", "RV64I", "0", 602 ],
        "ADDIW" : [ "Arithmetic", "i" , "xxxxxxx", "000", "0011011", "RV64I", "0", 603 ],
        "SLLIW" : [ "Shifts"    , "r" , "0000000", "001", "0011011", "RV64I", "0", 604 ],
        "SRLIW" : [ "Shifts"    , "r" , "0000000", "101", "0011011", "RV64I", "0", 605 ],
        "SRAIW" : [ "Shifts"    , "r" , "0100000", "101", "0011011", "RV64I", "0", 606 ],
        "ADDW"  : [ "Arithmetic", "r" , "0000000", "000", "0111011", "RV64I", "0", 607 ],
        "SUBW"  : [ "Arithmetic", "r" , "0100000", "000", "0111011", "RV64I", "0", 608 ],
        "SLLW"  : [ "Shifts"    , "r" , "0000000", "001", "0111011", "RV64I", "0", 609 ],
        "SRLW"  : [ "Shifts"    , "r" , "0000000", "101", "0111011", "RV64I", "0", 610 ],
        "SRAW"  : [ "Shifts"    , "r" , "0100000", "101", "0111011", "RV64I", "0", 611 ]
        }                                                                             
rv32m = {                                                                             
        "MUL"   : [ "Multiply"  , "r", "0000001", "000", "0110011", "RV32M", "0", 612 ],
        "MULH"  : [ "Multiply"  , "r", "0000001", "001", "0110011", "RV32M", "0", 613 ],
        "MULHSU": [ "Multiply"  , "r", "0000001", "010", "0110011", "RV32M", "0", 614 ],
        "MULHU" : [ "Multiply"  , "r", "0000001", "011", "0110011", "RV32M", "0", 615 ],
        "DIV"   : [ "Divide"    , "r", "0000001", "100", "0110011", "RV32M", "0", 616 ],
        "DIVU"  : [ "Divide"    , "r", "0000001", "101", "0110011", "RV32M", "0", 617 ],
        "REM"   : [ "Remainder" , "r", "0000001", "110", "0110011", "RV32M", "0", 618 ],
        "REMU"  : [ "Remainder" , "r", "0000001", "111", "0110011", "RV32M", "0", 619 ]
        }
rv64m = {
        "MULW"  : [ "Multiply"  , "r", "0000001", "000", "0111011", "RV64M", "0", 800 ],
        "DIVW"  : [ "Divide"    , "r", "0000001", "100", "0111011", "RV64M", "0", 801 ],
        "DIVUW" : [ "Divide"    , "r", "0000001", "101", "0111011", "RV64M", "0", 802 ],
        "REMW"  : [ "Remainder" , "r", "0000001", "110", "0111011", "RV64M", "0", 803 ],
        "REMUW" : [ "Remainder" , "r", "0000001", "111", "0111011", "RV64M", "0", 804 ]
        }
rv32a = {
   "LR.W"     : [ "Load Reserved" , "r2", "00010xx", "010", "0101111", "RV32A", "1", 110 ],
   "SC.W"     : [ "Store Cond"    , "r2", "00011xx", "010", "0101111", "RV32A", "1", 111 ],
   "AMOSWAP.W": [ "Swap Atomic"   , "r2", "00001xx", "010", "0101111", "RV32A", "1", 112 ],
   "AMOADD.W" : [ "Add Atomic"    , "r2", "00000xx", "010", "0101111", "RV32A", "1", 113 ],
   "AMOXOR.W" : [ "Logical Atomic", "r2", "00100xx", "010", "0101111", "RV32A", "1", 114 ],
   "AMOAND.W" : [ "Logical Atomic", "r2", "01100xx", "010", "0101111", "RV32A", "1", 115 ],
   "AMOOR.W"  : [ "Logical Atomic", "r2", "01000xx", "010", "0101111", "RV32A", "1", 116 ],
   "AMOMIN.W" : [ "Min/Max Atomic", "r2", "10000xx", "010", "0101111", "RV32A", "1", 117 ],
   "AMOMAX.W" : [ "Min/Max Atomic", "r2", "10100xx", "010", "0101111", "RV32A", "1", 412 ],
   "AMOMINU.W": [ "Min/Max Atomic", "r2", "11000xx", "010", "0101111", "RV32A", "1", 413 ],
   "AMOMAXU.W": [ "Min/Max Atomic", "r2", "11100xx", "010", "0101111", "RV32A", "1", 400 ]
   }
rv64a = {
   "LR.D"     : [ "Load Reserved" , "r2", "00010xx", "011", "0101111", "RV64A", "1", 401 ],
   "SC.D"     : [ "Store Cond"    , "r2", "00011xx", "011", "0101111", "RV64A", "1", 402 ],
   "AMOSWAP.D": [ "Swap Atomic"   , "r2", "00001xx", "011", "0101111", "RV64A", "1", 403 ],
   "AMOADD.D" : [ "Add Atomic"    , "r2", "00000xx", "011", "0101111", "RV64A", "1", 404 ],
   "AMOXOR.D" : [ "Logical Atomic", "r2", "00100xx", "011", "0101111", "RV64A", "1", 405 ],
   "AMOAND.D" : [ "Logical Atomic", "r2", "01100xx", "011", "0101111", "RV64A", "1", 406 ],
   "AMOOR.D"  : [ "Logical Atomic", "r2", "01000xx", "011", "0101111", "RV64A", "1", 407 ],
   "AMOMIN.D" : [ "Min/Max Atomic", "r2", "10000xx", "011", "0101111", "RV64A", "1", 408 ],
   "AMOMAX.D" : [ "Min/Max Atomic", "r2", "10100xx", "011", "0101111", "RV64A", "1", 409 ],
   "AMOMINU.D": [ "Min/Max Atomic", "r2", "11000xx", "011", "0101111", "RV64A", "1", 410 ],
   "AMOMAXU.D": [ "Min/Max Atomic", "r2", "11100xx", "011", "0101111", "RV64A", "1", 411 ]
        }


##RVV (Zve32x) - vector extension for Coral NPU
##generated from RISCVV_Instruction_List_Summary - RVV_Zve32x_Instructions.csv
##encodings cross-checked against qemu/target/riscv/insn32.decode
#value: [0:instrn type, 1:instrn format type, 2:bits[31:25], 3:bits[14:12],
#        4:opcode, 5:extension, 6:single_inst_run/multi_inst_run(for profiling),
#        7:clone_no(for profiling), 8:bits[24:20], 9:bits[19:15]]
#note: rvv entries carry TWO extra fields (8 and 9) that the rv32i/m/a entries
#      do not. many rvv insts fix bits[24:20] and/or bits[19:15] as opcode
#      rather than operand (vle8.v vs vle8ff.v differ ONLY in bits[24:20];
#      vcpop.m vs vfirst.m differ ONLY in bits[19:15]). "xxxxx" = operand.
#      the checker in gen_testcase.py builds exp_inst from fields 2,3,4 only,
#      so it will NOT tell those pairs apart until it is extended to use 8/9.
#bits[31:25] for OP-V   = funct6(6) + vm(1)
#bits[31:25] for vld/vst = nf(3) + mew(1) + mop(2) + vm(1)
#  mop: 00 unit-stride, 01 indexed-unordered, 10 strided, 11 indexed-ordered
#  nf = number of fields - 1, so segment n=2 -> nf field 001
#funct3 for OP-V: OPIVV 000, OPFVV 001, OPMVV 010, OPIVI 011, OPIVX 100,
#                 OPFVF 101, OPMVX 110, OPCFG 111
#funct3 for vld/vst is the width field: e8 000, e16 101, e32 110
#format types (all need a branch in create_inst):
#  "vcfg"  rd, rs1, vtypei        "vcfgi" rd, uimm, vtypei   "vcfgr" rd, rs1, rs2
#  "vvv"   vd, vs2, vs1, vm       "vvx"  vd, vs2, rs1, vm    "vvi" vd, vs2, imm, vm
#  "vvvm"  vd, vs2, vs1, v0       "vvxm" vd, vs2, rs1, v0    "vvim" vd, vs2, imm, v0
#          (vm bit must be 0 on these - v0 is an explicit operand, no ".t")
#  "vld"   vd, (rs1), vm          "vst"  vs3, (rs1), vm
#  "vlds"  vd, (rs1), rs2, vm     "vsts" vs3, (rs1), rs2, vm   (strided)
#  "vldi"  vd, (rs1), vs2, vm     "vsti" vs3, (rs1), vs2, vm   (indexed)
#  "vldr"  vd, (rs1)              "vstr" vs3, (rs1)            (whole register, and vlm.v/vsm.v)
#  "vldw"  vd, vs2, vm            "vrd"  rd, vs2, vm
#  "vmm"   vd, vs2, vs1           "vd1"  vd, vm
#  "vxs"   rd, vs2                "vsx"  vd, rs1               "vwr" vd, vs2
#  "vm1"   vd, vs2                "vm0"  vd                    (mask pseudo-ops)
#  "vxv"   vd, rs1, vs2, vm   (multiply-add .vx: scalar comes BEFORE vs2)
#  "vvvn"  vd, vs2, vs1           "vvxn" vd, vs2, rs1    "vvin" vd, vs2, imm
#          (vm bit hardwired to 1 - these forms take no mask, no ".t")
#  "vmvv"  vd, vs1                "vmvx" vd, rs1         "vmvi" vd, imm
#WARNING: every one of these traps with an illegal instruction until vtype is
#         valid. vsetvli must run before any of them - see write_c_frame_start
#         and first_opcode_list in gen_testcase.py.
rvv = {
   #--- Configuration-setting ---
   "VSETVLI"        : [ "Vec Config"   , "vcfg" , "0xxxxxx", "111", "1010111", "Zve32x", "1", 1000, "xxxxx", "xxxxx" ],
   "VSETIVLI"       : [ "Vec Config"   , "vcfgi", "11xxxxx", "111", "1010111", "Zve32x", "1", 1001, "xxxxx", "xxxxx" ],
   "VSETVL"         : [ "Vec Config"   , "vcfgr", "1000000", "111", "1010111", "Zve32x", "1", 1002, "xxxxx", "xxxxx" ],
   #--- Vector loads/stores - unit-stride ---
   "VLE8.V"         : [ "Vec Load"     , "vld"  , "000000x", "000", "0000111", "Zve32x", "1", 1003, "00000", "xxxxx" ],
   "VLE16.V"        : [ "Vec Load"     , "vld"  , "000000x", "101", "0000111", "Zve32x", "1", 1004, "00000", "xxxxx" ],
   "VLE32.V"        : [ "Vec Load"     , "vld"  , "000000x", "110", "0000111", "Zve32x", "1", 1005, "00000", "xxxxx" ],
   "VSE8.V"         : [ "Vec Store"    , "vst"  , "000000x", "000", "0100111", "Zve32x", "1", 1006, "00000", "xxxxx" ],
   "VSE16.V"        : [ "Vec Store"    , "vst"  , "000000x", "101", "0100111", "Zve32x", "1", 1007, "00000", "xxxxx" ],
   "VSE32.V"        : [ "Vec Store"    , "vst"  , "000000x", "110", "0100111", "Zve32x", "1", 1008, "00000", "xxxxx" ],
   "VLM.V"          : [ "Vec Load"     , "vldr" , "0000001", "000", "0000111", "Zve32x", "1", 1009, "01011", "xxxxx" ],
   "VSM.V"          : [ "Vec Store"    , "vstr" , "0000001", "000", "0100111", "Zve32x", "1", 1010, "01011", "xxxxx" ],
   #--- Vector loads/stores - constant-stride ---
   "VLSE8.V"        : [ "Vec Load"     , "vlds" , "000010x", "000", "0000111", "Zve32x", "1", 1011, "xxxxx", "xxxxx" ],
   "VLSE16.V"       : [ "Vec Load"     , "vlds" , "000010x", "101", "0000111", "Zve32x", "1", 1012, "xxxxx", "xxxxx" ],
   "VLSE32.V"       : [ "Vec Load"     , "vlds" , "000010x", "110", "0000111", "Zve32x", "1", 1013, "xxxxx", "xxxxx" ],
   "VSSE8.V"        : [ "Vec Store"    , "vsts" , "000010x", "000", "0100111", "Zve32x", "1", 1014, "xxxxx", "xxxxx" ],
   "VSSE16.V"       : [ "Vec Store"    , "vsts" , "000010x", "101", "0100111", "Zve32x", "1", 1015, "xxxxx", "xxxxx" ],
   "VSSE32.V"       : [ "Vec Store"    , "vsts" , "000010x", "110", "0100111", "Zve32x", "1", 1016, "xxxxx", "xxxxx" ],
   #--- Vector loads/stores - indexed ---
   "VLUXEI8.V"      : [ "Vec Load"     , "vldi" , "000001x", "000", "0000111", "Zve32x", "1", 1017, "xxxxx", "xxxxx" ],
   "VLUXEI16.V"     : [ "Vec Load"     , "vldi" , "000001x", "101", "0000111", "Zve32x", "1", 1018, "xxxxx", "xxxxx" ],
   "VLUXEI32.V"     : [ "Vec Load"     , "vldi" , "000001x", "110", "0000111", "Zve32x", "1", 1019, "xxxxx", "xxxxx" ],
   "VLOXEI8.V"      : [ "Vec Load"     , "vldi" , "000011x", "000", "0000111", "Zve32x", "1", 1020, "xxxxx", "xxxxx" ],
   "VLOXEI16.V"     : [ "Vec Load"     , "vldi" , "000011x", "101", "0000111", "Zve32x", "1", 1021, "xxxxx", "xxxxx" ],
   "VLOXEI32.V"     : [ "Vec Load"     , "vldi" , "000011x", "110", "0000111", "Zve32x", "1", 1022, "xxxxx", "xxxxx" ],
   "VSUXEI8.V"      : [ "Vec Store"    , "vsti" , "000001x", "000", "0100111", "Zve32x", "1", 1023, "xxxxx", "xxxxx" ],
   "VSUXEI16.V"     : [ "Vec Store"    , "vsti" , "000001x", "101", "0100111", "Zve32x", "1", 1024, "xxxxx", "xxxxx" ],
   "VSUXEI32.V"     : [ "Vec Store"    , "vsti" , "000001x", "110", "0100111", "Zve32x", "1", 1025, "xxxxx", "xxxxx" ],
   "VSOXEI8.V"      : [ "Vec Store"    , "vsti" , "000011x", "000", "0100111", "Zve32x", "1", 1026, "xxxxx", "xxxxx" ],
   "VSOXEI16.V"     : [ "Vec Store"    , "vsti" , "000011x", "101", "0100111", "Zve32x", "1", 1027, "xxxxx", "xxxxx" ],
   "VSOXEI32.V"     : [ "Vec Store"    , "vsti" , "000011x", "110", "0100111", "Zve32x", "1", 1028, "xxxxx", "xxxxx" ],
   #--- Vector loads/stores - fault-only-first ---
   "VLE8FF.V"       : [ "Vec Load FF"  , "vld"  , "000000x", "000", "0000111", "Zve32x", "1", 1029, "10000", "xxxxx" ],
   "VLE16FF.V"      : [ "Vec Load FF"  , "vld"  , "000000x", "101", "0000111", "Zve32x", "1", 1030, "10000", "xxxxx" ],
   "VLE32FF.V"      : [ "Vec Load FF"  , "vld"  , "000000x", "110", "0000111", "Zve32x", "1", 1031, "10000", "xxxxx" ],
   #--- Vector loads/stores - segment ---
   "VLSEG2E8.V"     : [ "Vec Load Seg" , "vld"  , "001000x", "000", "0000111", "Zve32x", "1", 1032, "00000", "xxxxx" ],
   "VLSEG2E16.V"    : [ "Vec Load Seg" , "vld"  , "001000x", "101", "0000111", "Zve32x", "1", 1033, "00000", "xxxxx" ],
   "VLSEG2E32.V"    : [ "Vec Load Seg" , "vld"  , "001000x", "110", "0000111", "Zve32x", "1", 1034, "00000", "xxxxx" ],
   "VLSEG3E8.V"     : [ "Vec Load Seg" , "vld"  , "010000x", "000", "0000111", "Zve32x", "1", 1035, "00000", "xxxxx" ],
   "VLSEG3E16.V"    : [ "Vec Load Seg" , "vld"  , "010000x", "101", "0000111", "Zve32x", "1", 1036, "00000", "xxxxx" ],
   "VLSEG3E32.V"    : [ "Vec Load Seg" , "vld"  , "010000x", "110", "0000111", "Zve32x", "1", 1037, "00000", "xxxxx" ],
   "VLSEG4E8.V"     : [ "Vec Load Seg" , "vld"  , "011000x", "000", "0000111", "Zve32x", "1", 1038, "00000", "xxxxx" ],
   "VLSEG4E16.V"    : [ "Vec Load Seg" , "vld"  , "011000x", "101", "0000111", "Zve32x", "1", 1039, "00000", "xxxxx" ],
   "VLSEG4E32.V"    : [ "Vec Load Seg" , "vld"  , "011000x", "110", "0000111", "Zve32x", "1", 1040, "00000", "xxxxx" ],
   "VLSEG5E8.V"     : [ "Vec Load Seg" , "vld"  , "100000x", "000", "0000111", "Zve32x", "1", 1041, "00000", "xxxxx" ],
   "VLSEG5E16.V"    : [ "Vec Load Seg" , "vld"  , "100000x", "101", "0000111", "Zve32x", "1", 1042, "00000", "xxxxx" ],
   "VLSEG5E32.V"    : [ "Vec Load Seg" , "vld"  , "100000x", "110", "0000111", "Zve32x", "1", 1043, "00000", "xxxxx" ],
   "VLSEG6E8.V"     : [ "Vec Load Seg" , "vld"  , "101000x", "000", "0000111", "Zve32x", "1", 1044, "00000", "xxxxx" ],
   "VLSEG6E16.V"    : [ "Vec Load Seg" , "vld"  , "101000x", "101", "0000111", "Zve32x", "1", 1045, "00000", "xxxxx" ],
   "VLSEG6E32.V"    : [ "Vec Load Seg" , "vld"  , "101000x", "110", "0000111", "Zve32x", "1", 1046, "00000", "xxxxx" ],
   "VLSEG7E8.V"     : [ "Vec Load Seg" , "vld"  , "110000x", "000", "0000111", "Zve32x", "1", 1047, "00000", "xxxxx" ],
   "VLSEG7E16.V"    : [ "Vec Load Seg" , "vld"  , "110000x", "101", "0000111", "Zve32x", "1", 1048, "00000", "xxxxx" ],
   "VLSEG7E32.V"    : [ "Vec Load Seg" , "vld"  , "110000x", "110", "0000111", "Zve32x", "1", 1049, "00000", "xxxxx" ],
   "VLSEG8E8.V"     : [ "Vec Load Seg" , "vld"  , "111000x", "000", "0000111", "Zve32x", "1", 1050, "00000", "xxxxx" ],
   "VLSEG8E16.V"    : [ "Vec Load Seg" , "vld"  , "111000x", "101", "0000111", "Zve32x", "1", 1051, "00000", "xxxxx" ],
   "VLSEG8E32.V"    : [ "Vec Load Seg" , "vld"  , "111000x", "110", "0000111", "Zve32x", "1", 1052, "00000", "xxxxx" ],
   "VSSEG2E8.V"     : [ "Vec Store Seg", "vst"  , "001000x", "000", "0100111", "Zve32x", "1", 1053, "00000", "xxxxx" ],
   "VSSEG2E16.V"    : [ "Vec Store Seg", "vst"  , "001000x", "101", "0100111", "Zve32x", "1", 1054, "00000", "xxxxx" ],
   "VSSEG2E32.V"    : [ "Vec Store Seg", "vst"  , "001000x", "110", "0100111", "Zve32x", "1", 1055, "00000", "xxxxx" ],
   "VSSEG3E8.V"     : [ "Vec Store Seg", "vst"  , "010000x", "000", "0100111", "Zve32x", "1", 1056, "00000", "xxxxx" ],
   "VSSEG3E16.V"    : [ "Vec Store Seg", "vst"  , "010000x", "101", "0100111", "Zve32x", "1", 1057, "00000", "xxxxx" ],
   "VSSEG3E32.V"    : [ "Vec Store Seg", "vst"  , "010000x", "110", "0100111", "Zve32x", "1", 1058, "00000", "xxxxx" ],
   "VSSEG4E8.V"     : [ "Vec Store Seg", "vst"  , "011000x", "000", "0100111", "Zve32x", "1", 1059, "00000", "xxxxx" ],
   "VSSEG4E16.V"    : [ "Vec Store Seg", "vst"  , "011000x", "101", "0100111", "Zve32x", "1", 1060, "00000", "xxxxx" ],
   "VSSEG4E32.V"    : [ "Vec Store Seg", "vst"  , "011000x", "110", "0100111", "Zve32x", "1", 1061, "00000", "xxxxx" ],
   "VSSEG5E8.V"     : [ "Vec Store Seg", "vst"  , "100000x", "000", "0100111", "Zve32x", "1", 1062, "00000", "xxxxx" ],
   "VSSEG5E16.V"    : [ "Vec Store Seg", "vst"  , "100000x", "101", "0100111", "Zve32x", "1", 1063, "00000", "xxxxx" ],
   "VSSEG5E32.V"    : [ "Vec Store Seg", "vst"  , "100000x", "110", "0100111", "Zve32x", "1", 1064, "00000", "xxxxx" ],
   "VSSEG6E8.V"     : [ "Vec Store Seg", "vst"  , "101000x", "000", "0100111", "Zve32x", "1", 1065, "00000", "xxxxx" ],
   "VSSEG6E16.V"    : [ "Vec Store Seg", "vst"  , "101000x", "101", "0100111", "Zve32x", "1", 1066, "00000", "xxxxx" ],
   "VSSEG6E32.V"    : [ "Vec Store Seg", "vst"  , "101000x", "110", "0100111", "Zve32x", "1", 1067, "00000", "xxxxx" ],
   "VSSEG7E8.V"     : [ "Vec Store Seg", "vst"  , "110000x", "000", "0100111", "Zve32x", "1", 1068, "00000", "xxxxx" ],
   "VSSEG7E16.V"    : [ "Vec Store Seg", "vst"  , "110000x", "101", "0100111", "Zve32x", "1", 1069, "00000", "xxxxx" ],
   "VSSEG7E32.V"    : [ "Vec Store Seg", "vst"  , "110000x", "110", "0100111", "Zve32x", "1", 1070, "00000", "xxxxx" ],
   "VSSEG8E8.V"     : [ "Vec Store Seg", "vst"  , "111000x", "000", "0100111", "Zve32x", "1", 1071, "00000", "xxxxx" ],
   "VSSEG8E16.V"    : [ "Vec Store Seg", "vst"  , "111000x", "101", "0100111", "Zve32x", "1", 1072, "00000", "xxxxx" ],
   "VSSEG8E32.V"    : [ "Vec Store Seg", "vst"  , "111000x", "110", "0100111", "Zve32x", "1", 1073, "00000", "xxxxx" ],
   "VLSSEG2E8.V"    : [ "Vec Load Seg" , "vlds" , "001010x", "000", "0000111", "Zve32x", "1", 1074, "xxxxx", "xxxxx" ],
   "VLSSEG2E16.V"   : [ "Vec Load Seg" , "vlds" , "001010x", "101", "0000111", "Zve32x", "1", 1075, "xxxxx", "xxxxx" ],
   "VLSSEG2E32.V"   : [ "Vec Load Seg" , "vlds" , "001010x", "110", "0000111", "Zve32x", "1", 1076, "xxxxx", "xxxxx" ],
   "VLSSEG3E8.V"    : [ "Vec Load Seg" , "vlds" , "010010x", "000", "0000111", "Zve32x", "1", 1077, "xxxxx", "xxxxx" ],
   "VLSSEG3E16.V"   : [ "Vec Load Seg" , "vlds" , "010010x", "101", "0000111", "Zve32x", "1", 1078, "xxxxx", "xxxxx" ],
   "VLSSEG3E32.V"   : [ "Vec Load Seg" , "vlds" , "010010x", "110", "0000111", "Zve32x", "1", 1079, "xxxxx", "xxxxx" ],
   "VLSSEG4E8.V"    : [ "Vec Load Seg" , "vlds" , "011010x", "000", "0000111", "Zve32x", "1", 1080, "xxxxx", "xxxxx" ],
   "VLSSEG4E16.V"   : [ "Vec Load Seg" , "vlds" , "011010x", "101", "0000111", "Zve32x", "1", 1081, "xxxxx", "xxxxx" ],
   "VLSSEG4E32.V"   : [ "Vec Load Seg" , "vlds" , "011010x", "110", "0000111", "Zve32x", "1", 1082, "xxxxx", "xxxxx" ],
   "VLSSEG5E8.V"    : [ "Vec Load Seg" , "vlds" , "100010x", "000", "0000111", "Zve32x", "1", 1083, "xxxxx", "xxxxx" ],
   "VLSSEG5E16.V"   : [ "Vec Load Seg" , "vlds" , "100010x", "101", "0000111", "Zve32x", "1", 1084, "xxxxx", "xxxxx" ],
   "VLSSEG5E32.V"   : [ "Vec Load Seg" , "vlds" , "100010x", "110", "0000111", "Zve32x", "1", 1085, "xxxxx", "xxxxx" ],
   "VLSSEG6E8.V"    : [ "Vec Load Seg" , "vlds" , "101010x", "000", "0000111", "Zve32x", "1", 1086, "xxxxx", "xxxxx" ],
   "VLSSEG6E16.V"   : [ "Vec Load Seg" , "vlds" , "101010x", "101", "0000111", "Zve32x", "1", 1087, "xxxxx", "xxxxx" ],
   "VLSSEG6E32.V"   : [ "Vec Load Seg" , "vlds" , "101010x", "110", "0000111", "Zve32x", "1", 1088, "xxxxx", "xxxxx" ],
   "VLSSEG7E8.V"    : [ "Vec Load Seg" , "vlds" , "110010x", "000", "0000111", "Zve32x", "1", 1089, "xxxxx", "xxxxx" ],
   "VLSSEG7E16.V"   : [ "Vec Load Seg" , "vlds" , "110010x", "101", "0000111", "Zve32x", "1", 1090, "xxxxx", "xxxxx" ],
   "VLSSEG7E32.V"   : [ "Vec Load Seg" , "vlds" , "110010x", "110", "0000111", "Zve32x", "1", 1091, "xxxxx", "xxxxx" ],
   "VLSSEG8E8.V"    : [ "Vec Load Seg" , "vlds" , "111010x", "000", "0000111", "Zve32x", "1", 1092, "xxxxx", "xxxxx" ],
   "VLSSEG8E16.V"   : [ "Vec Load Seg" , "vlds" , "111010x", "101", "0000111", "Zve32x", "1", 1093, "xxxxx", "xxxxx" ],
   "VLSSEG8E32.V"   : [ "Vec Load Seg" , "vlds" , "111010x", "110", "0000111", "Zve32x", "1", 1094, "xxxxx", "xxxxx" ],
   "VSSSEG2E8.V"    : [ "Vec Store Seg", "vsts" , "001010x", "000", "0100111", "Zve32x", "1", 1095, "xxxxx", "xxxxx" ],
   "VSSSEG2E16.V"   : [ "Vec Store Seg", "vsts" , "001010x", "101", "0100111", "Zve32x", "1", 1096, "xxxxx", "xxxxx" ],
   "VSSSEG2E32.V"   : [ "Vec Store Seg", "vsts" , "001010x", "110", "0100111", "Zve32x", "1", 1097, "xxxxx", "xxxxx" ],
   "VSSSEG3E8.V"    : [ "Vec Store Seg", "vsts" , "010010x", "000", "0100111", "Zve32x", "1", 1098, "xxxxx", "xxxxx" ],
   "VSSSEG3E16.V"   : [ "Vec Store Seg", "vsts" , "010010x", "101", "0100111", "Zve32x", "1", 1099, "xxxxx", "xxxxx" ],
   "VSSSEG3E32.V"   : [ "Vec Store Seg", "vsts" , "010010x", "110", "0100111", "Zve32x", "1", 1100, "xxxxx", "xxxxx" ],
   "VSSSEG4E8.V"    : [ "Vec Store Seg", "vsts" , "011010x", "000", "0100111", "Zve32x", "1", 1101, "xxxxx", "xxxxx" ],
   "VSSSEG4E16.V"   : [ "Vec Store Seg", "vsts" , "011010x", "101", "0100111", "Zve32x", "1", 1102, "xxxxx", "xxxxx" ],
   "VSSSEG4E32.V"   : [ "Vec Store Seg", "vsts" , "011010x", "110", "0100111", "Zve32x", "1", 1103, "xxxxx", "xxxxx" ],
   "VSSSEG5E8.V"    : [ "Vec Store Seg", "vsts" , "100010x", "000", "0100111", "Zve32x", "1", 1104, "xxxxx", "xxxxx" ],
   "VSSSEG5E16.V"   : [ "Vec Store Seg", "vsts" , "100010x", "101", "0100111", "Zve32x", "1", 1105, "xxxxx", "xxxxx" ],
   "VSSSEG5E32.V"   : [ "Vec Store Seg", "vsts" , "100010x", "110", "0100111", "Zve32x", "1", 1106, "xxxxx", "xxxxx" ],
   "VSSSEG6E8.V"    : [ "Vec Store Seg", "vsts" , "101010x", "000", "0100111", "Zve32x", "1", 1107, "xxxxx", "xxxxx" ],
   "VSSSEG6E16.V"   : [ "Vec Store Seg", "vsts" , "101010x", "101", "0100111", "Zve32x", "1", 1108, "xxxxx", "xxxxx" ],
   "VSSSEG6E32.V"   : [ "Vec Store Seg", "vsts" , "101010x", "110", "0100111", "Zve32x", "1", 1109, "xxxxx", "xxxxx" ],
   "VSSSEG7E8.V"    : [ "Vec Store Seg", "vsts" , "110010x", "000", "0100111", "Zve32x", "1", 1110, "xxxxx", "xxxxx" ],
   "VSSSEG7E16.V"   : [ "Vec Store Seg", "vsts" , "110010x", "101", "0100111", "Zve32x", "1", 1111, "xxxxx", "xxxxx" ],
   "VSSSEG7E32.V"   : [ "Vec Store Seg", "vsts" , "110010x", "110", "0100111", "Zve32x", "1", 1112, "xxxxx", "xxxxx" ],
   "VSSSEG8E8.V"    : [ "Vec Store Seg", "vsts" , "111010x", "000", "0100111", "Zve32x", "1", 1113, "xxxxx", "xxxxx" ],
   "VSSSEG8E16.V"   : [ "Vec Store Seg", "vsts" , "111010x", "101", "0100111", "Zve32x", "1", 1114, "xxxxx", "xxxxx" ],
   "VSSSEG8E32.V"   : [ "Vec Store Seg", "vsts" , "111010x", "110", "0100111", "Zve32x", "1", 1115, "xxxxx", "xxxxx" ],
   "VLUXSEG2EI8.V"  : [ "Vec Load Seg" , "vldi" , "001001x", "000", "0000111", "Zve32x", "1", 1116, "xxxxx", "xxxxx" ],
   "VLUXSEG2EI16.V" : [ "Vec Load Seg" , "vldi" , "001001x", "101", "0000111", "Zve32x", "1", 1117, "xxxxx", "xxxxx" ],
   "VLUXSEG2EI32.V" : [ "Vec Load Seg" , "vldi" , "001001x", "110", "0000111", "Zve32x", "1", 1118, "xxxxx", "xxxxx" ],
   "VLUXSEG3EI8.V"  : [ "Vec Load Seg" , "vldi" , "010001x", "000", "0000111", "Zve32x", "1", 1119, "xxxxx", "xxxxx" ],
   "VLUXSEG3EI16.V" : [ "Vec Load Seg" , "vldi" , "010001x", "101", "0000111", "Zve32x", "1", 1120, "xxxxx", "xxxxx" ],
   "VLUXSEG3EI32.V" : [ "Vec Load Seg" , "vldi" , "010001x", "110", "0000111", "Zve32x", "1", 1121, "xxxxx", "xxxxx" ],
   "VLUXSEG4EI8.V"  : [ "Vec Load Seg" , "vldi" , "011001x", "000", "0000111", "Zve32x", "1", 1122, "xxxxx", "xxxxx" ],
   "VLUXSEG4EI16.V" : [ "Vec Load Seg" , "vldi" , "011001x", "101", "0000111", "Zve32x", "1", 1123, "xxxxx", "xxxxx" ],
   "VLUXSEG4EI32.V" : [ "Vec Load Seg" , "vldi" , "011001x", "110", "0000111", "Zve32x", "1", 1124, "xxxxx", "xxxxx" ],
   "VLUXSEG5EI8.V"  : [ "Vec Load Seg" , "vldi" , "100001x", "000", "0000111", "Zve32x", "1", 1125, "xxxxx", "xxxxx" ],
   "VLUXSEG5EI16.V" : [ "Vec Load Seg" , "vldi" , "100001x", "101", "0000111", "Zve32x", "1", 1126, "xxxxx", "xxxxx" ],
   "VLUXSEG5EI32.V" : [ "Vec Load Seg" , "vldi" , "100001x", "110", "0000111", "Zve32x", "1", 1127, "xxxxx", "xxxxx" ],
   "VLUXSEG6EI8.V"  : [ "Vec Load Seg" , "vldi" , "101001x", "000", "0000111", "Zve32x", "1", 1128, "xxxxx", "xxxxx" ],
   "VLUXSEG6EI16.V" : [ "Vec Load Seg" , "vldi" , "101001x", "101", "0000111", "Zve32x", "1", 1129, "xxxxx", "xxxxx" ],
   "VLUXSEG6EI32.V" : [ "Vec Load Seg" , "vldi" , "101001x", "110", "0000111", "Zve32x", "1", 1130, "xxxxx", "xxxxx" ],
   "VLUXSEG7EI8.V"  : [ "Vec Load Seg" , "vldi" , "110001x", "000", "0000111", "Zve32x", "1", 1131, "xxxxx", "xxxxx" ],
   "VLUXSEG7EI16.V" : [ "Vec Load Seg" , "vldi" , "110001x", "101", "0000111", "Zve32x", "1", 1132, "xxxxx", "xxxxx" ],
   "VLUXSEG7EI32.V" : [ "Vec Load Seg" , "vldi" , "110001x", "110", "0000111", "Zve32x", "1", 1133, "xxxxx", "xxxxx" ],
   "VLUXSEG8EI8.V"  : [ "Vec Load Seg" , "vldi" , "111001x", "000", "0000111", "Zve32x", "1", 1134, "xxxxx", "xxxxx" ],
   "VLUXSEG8EI16.V" : [ "Vec Load Seg" , "vldi" , "111001x", "101", "0000111", "Zve32x", "1", 1135, "xxxxx", "xxxxx" ],
   "VLUXSEG8EI32.V" : [ "Vec Load Seg" , "vldi" , "111001x", "110", "0000111", "Zve32x", "1", 1136, "xxxxx", "xxxxx" ],
   "VLOXSEG2EI8.V"  : [ "Vec Load Seg" , "vldi" , "001011x", "000", "0000111", "Zve32x", "1", 1137, "xxxxx", "xxxxx" ],
   "VLOXSEG2EI16.V" : [ "Vec Load Seg" , "vldi" , "001011x", "101", "0000111", "Zve32x", "1", 1138, "xxxxx", "xxxxx" ],
   "VLOXSEG2EI32.V" : [ "Vec Load Seg" , "vldi" , "001011x", "110", "0000111", "Zve32x", "1", 1139, "xxxxx", "xxxxx" ],
   "VLOXSEG3EI8.V"  : [ "Vec Load Seg" , "vldi" , "010011x", "000", "0000111", "Zve32x", "1", 1140, "xxxxx", "xxxxx" ],
   "VLOXSEG3EI16.V" : [ "Vec Load Seg" , "vldi" , "010011x", "101", "0000111", "Zve32x", "1", 1141, "xxxxx", "xxxxx" ],
   "VLOXSEG3EI32.V" : [ "Vec Load Seg" , "vldi" , "010011x", "110", "0000111", "Zve32x", "1", 1142, "xxxxx", "xxxxx" ],
   "VLOXSEG4EI8.V"  : [ "Vec Load Seg" , "vldi" , "011011x", "000", "0000111", "Zve32x", "1", 1143, "xxxxx", "xxxxx" ],
   "VLOXSEG4EI16.V" : [ "Vec Load Seg" , "vldi" , "011011x", "101", "0000111", "Zve32x", "1", 1144, "xxxxx", "xxxxx" ],
   "VLOXSEG4EI32.V" : [ "Vec Load Seg" , "vldi" , "011011x", "110", "0000111", "Zve32x", "1", 1145, "xxxxx", "xxxxx" ],
   "VLOXSEG5EI8.V"  : [ "Vec Load Seg" , "vldi" , "100011x", "000", "0000111", "Zve32x", "1", 1146, "xxxxx", "xxxxx" ],
   "VLOXSEG5EI16.V" : [ "Vec Load Seg" , "vldi" , "100011x", "101", "0000111", "Zve32x", "1", 1147, "xxxxx", "xxxxx" ],
   "VLOXSEG5EI32.V" : [ "Vec Load Seg" , "vldi" , "100011x", "110", "0000111", "Zve32x", "1", 1148, "xxxxx", "xxxxx" ],
   "VLOXSEG6EI8.V"  : [ "Vec Load Seg" , "vldi" , "101011x", "000", "0000111", "Zve32x", "1", 1149, "xxxxx", "xxxxx" ],
   "VLOXSEG6EI16.V" : [ "Vec Load Seg" , "vldi" , "101011x", "101", "0000111", "Zve32x", "1", 1150, "xxxxx", "xxxxx" ],
   "VLOXSEG6EI32.V" : [ "Vec Load Seg" , "vldi" , "101011x", "110", "0000111", "Zve32x", "1", 1151, "xxxxx", "xxxxx" ],
   "VLOXSEG7EI8.V"  : [ "Vec Load Seg" , "vldi" , "110011x", "000", "0000111", "Zve32x", "1", 1152, "xxxxx", "xxxxx" ],
   "VLOXSEG7EI16.V" : [ "Vec Load Seg" , "vldi" , "110011x", "101", "0000111", "Zve32x", "1", 1153, "xxxxx", "xxxxx" ],
   "VLOXSEG7EI32.V" : [ "Vec Load Seg" , "vldi" , "110011x", "110", "0000111", "Zve32x", "1", 1154, "xxxxx", "xxxxx" ],
   "VLOXSEG8EI8.V"  : [ "Vec Load Seg" , "vldi" , "111011x", "000", "0000111", "Zve32x", "1", 1155, "xxxxx", "xxxxx" ],
   "VLOXSEG8EI16.V" : [ "Vec Load Seg" , "vldi" , "111011x", "101", "0000111", "Zve32x", "1", 1156, "xxxxx", "xxxxx" ],
   "VLOXSEG8EI32.V" : [ "Vec Load Seg" , "vldi" , "111011x", "110", "0000111", "Zve32x", "1", 1157, "xxxxx", "xxxxx" ],
   "VSUXSEG2EI8.V"  : [ "Vec Store Seg", "vsti" , "001001x", "000", "0100111", "Zve32x", "1", 1158, "xxxxx", "xxxxx" ],
   "VSUXSEG2EI16.V" : [ "Vec Store Seg", "vsti" , "001001x", "101", "0100111", "Zve32x", "1", 1159, "xxxxx", "xxxxx" ],
   "VSUXSEG2EI32.V" : [ "Vec Store Seg", "vsti" , "001001x", "110", "0100111", "Zve32x", "1", 1160, "xxxxx", "xxxxx" ],
   "VSUXSEG3EI8.V"  : [ "Vec Store Seg", "vsti" , "010001x", "000", "0100111", "Zve32x", "1", 1161, "xxxxx", "xxxxx" ],
   "VSUXSEG3EI16.V" : [ "Vec Store Seg", "vsti" , "010001x", "101", "0100111", "Zve32x", "1", 1162, "xxxxx", "xxxxx" ],
   "VSUXSEG3EI32.V" : [ "Vec Store Seg", "vsti" , "010001x", "110", "0100111", "Zve32x", "1", 1163, "xxxxx", "xxxxx" ],
   "VSUXSEG4EI8.V"  : [ "Vec Store Seg", "vsti" , "011001x", "000", "0100111", "Zve32x", "1", 1164, "xxxxx", "xxxxx" ],
   "VSUXSEG4EI16.V" : [ "Vec Store Seg", "vsti" , "011001x", "101", "0100111", "Zve32x", "1", 1165, "xxxxx", "xxxxx" ],
   "VSUXSEG4EI32.V" : [ "Vec Store Seg", "vsti" , "011001x", "110", "0100111", "Zve32x", "1", 1166, "xxxxx", "xxxxx" ],
   "VSUXSEG5EI8.V"  : [ "Vec Store Seg", "vsti" , "100001x", "000", "0100111", "Zve32x", "1", 1167, "xxxxx", "xxxxx" ],
   "VSUXSEG5EI16.V" : [ "Vec Store Seg", "vsti" , "100001x", "101", "0100111", "Zve32x", "1", 1168, "xxxxx", "xxxxx" ],
   "VSUXSEG5EI32.V" : [ "Vec Store Seg", "vsti" , "100001x", "110", "0100111", "Zve32x", "1", 1169, "xxxxx", "xxxxx" ],
   "VSUXSEG6EI8.V"  : [ "Vec Store Seg", "vsti" , "101001x", "000", "0100111", "Zve32x", "1", 1170, "xxxxx", "xxxxx" ],
   "VSUXSEG6EI16.V" : [ "Vec Store Seg", "vsti" , "101001x", "101", "0100111", "Zve32x", "1", 1171, "xxxxx", "xxxxx" ],
   "VSUXSEG6EI32.V" : [ "Vec Store Seg", "vsti" , "101001x", "110", "0100111", "Zve32x", "1", 1172, "xxxxx", "xxxxx" ],
   "VSUXSEG7EI8.V"  : [ "Vec Store Seg", "vsti" , "110001x", "000", "0100111", "Zve32x", "1", 1173, "xxxxx", "xxxxx" ],
   "VSUXSEG7EI16.V" : [ "Vec Store Seg", "vsti" , "110001x", "101", "0100111", "Zve32x", "1", 1174, "xxxxx", "xxxxx" ],
   "VSUXSEG7EI32.V" : [ "Vec Store Seg", "vsti" , "110001x", "110", "0100111", "Zve32x", "1", 1175, "xxxxx", "xxxxx" ],
   "VSUXSEG8EI8.V"  : [ "Vec Store Seg", "vsti" , "111001x", "000", "0100111", "Zve32x", "1", 1176, "xxxxx", "xxxxx" ],
   "VSUXSEG8EI16.V" : [ "Vec Store Seg", "vsti" , "111001x", "101", "0100111", "Zve32x", "1", 1177, "xxxxx", "xxxxx" ],
   "VSUXSEG8EI32.V" : [ "Vec Store Seg", "vsti" , "111001x", "110", "0100111", "Zve32x", "1", 1178, "xxxxx", "xxxxx" ],
   "VSOXSEG2EI8.V"  : [ "Vec Store Seg", "vsti" , "001011x", "000", "0100111", "Zve32x", "1", 1179, "xxxxx", "xxxxx" ],
   "VSOXSEG2EI16.V" : [ "Vec Store Seg", "vsti" , "001011x", "101", "0100111", "Zve32x", "1", 1180, "xxxxx", "xxxxx" ],
   "VSOXSEG2EI32.V" : [ "Vec Store Seg", "vsti" , "001011x", "110", "0100111", "Zve32x", "1", 1181, "xxxxx", "xxxxx" ],
   "VSOXSEG3EI8.V"  : [ "Vec Store Seg", "vsti" , "010011x", "000", "0100111", "Zve32x", "1", 1182, "xxxxx", "xxxxx" ],
   "VSOXSEG3EI16.V" : [ "Vec Store Seg", "vsti" , "010011x", "101", "0100111", "Zve32x", "1", 1183, "xxxxx", "xxxxx" ],
   "VSOXSEG3EI32.V" : [ "Vec Store Seg", "vsti" , "010011x", "110", "0100111", "Zve32x", "1", 1184, "xxxxx", "xxxxx" ],
   "VSOXSEG4EI8.V"  : [ "Vec Store Seg", "vsti" , "011011x", "000", "0100111", "Zve32x", "1", 1185, "xxxxx", "xxxxx" ],
   "VSOXSEG4EI16.V" : [ "Vec Store Seg", "vsti" , "011011x", "101", "0100111", "Zve32x", "1", 1186, "xxxxx", "xxxxx" ],
   "VSOXSEG4EI32.V" : [ "Vec Store Seg", "vsti" , "011011x", "110", "0100111", "Zve32x", "1", 1187, "xxxxx", "xxxxx" ],
   "VSOXSEG5EI8.V"  : [ "Vec Store Seg", "vsti" , "100011x", "000", "0100111", "Zve32x", "1", 1188, "xxxxx", "xxxxx" ],
   "VSOXSEG5EI16.V" : [ "Vec Store Seg", "vsti" , "100011x", "101", "0100111", "Zve32x", "1", 1189, "xxxxx", "xxxxx" ],
   "VSOXSEG5EI32.V" : [ "Vec Store Seg", "vsti" , "100011x", "110", "0100111", "Zve32x", "1", 1190, "xxxxx", "xxxxx" ],
   "VSOXSEG6EI8.V"  : [ "Vec Store Seg", "vsti" , "101011x", "000", "0100111", "Zve32x", "1", 1191, "xxxxx", "xxxxx" ],
   "VSOXSEG6EI16.V" : [ "Vec Store Seg", "vsti" , "101011x", "101", "0100111", "Zve32x", "1", 1192, "xxxxx", "xxxxx" ],
   "VSOXSEG6EI32.V" : [ "Vec Store Seg", "vsti" , "101011x", "110", "0100111", "Zve32x", "1", 1193, "xxxxx", "xxxxx" ],
   "VSOXSEG7EI8.V"  : [ "Vec Store Seg", "vsti" , "110011x", "000", "0100111", "Zve32x", "1", 1194, "xxxxx", "xxxxx" ],
   "VSOXSEG7EI16.V" : [ "Vec Store Seg", "vsti" , "110011x", "101", "0100111", "Zve32x", "1", 1195, "xxxxx", "xxxxx" ],
   "VSOXSEG7EI32.V" : [ "Vec Store Seg", "vsti" , "110011x", "110", "0100111", "Zve32x", "1", 1196, "xxxxx", "xxxxx" ],
   "VSOXSEG8EI8.V"  : [ "Vec Store Seg", "vsti" , "111011x", "000", "0100111", "Zve32x", "1", 1197, "xxxxx", "xxxxx" ],
   "VSOXSEG8EI16.V" : [ "Vec Store Seg", "vsti" , "111011x", "101", "0100111", "Zve32x", "1", 1198, "xxxxx", "xxxxx" ],
   "VSOXSEG8EI32.V" : [ "Vec Store Seg", "vsti" , "111011x", "110", "0100111", "Zve32x", "1", 1199, "xxxxx", "xxxxx" ],
   #--- Vector loads/stores - segment fault-only-first ---
   "VLSEG2E8FF.V"   : [ "Vec Load SegFF", "vld"  , "001000x", "000", "0000111", "Zve32x", "1", 1433, "10000", "xxxxx" ],
   "VLSEG2E16FF.V"  : [ "Vec Load SegFF", "vld"  , "001000x", "101", "0000111", "Zve32x", "1", 1434, "10000", "xxxxx" ],
   "VLSEG2E32FF.V"  : [ "Vec Load SegFF", "vld"  , "001000x", "110", "0000111", "Zve32x", "1", 1435, "10000", "xxxxx" ],
   "VLSEG3E8FF.V"   : [ "Vec Load SegFF", "vld"  , "010000x", "000", "0000111", "Zve32x", "1", 1436, "10000", "xxxxx" ],
   "VLSEG3E16FF.V"  : [ "Vec Load SegFF", "vld"  , "010000x", "101", "0000111", "Zve32x", "1", 1437, "10000", "xxxxx" ],
   "VLSEG3E32FF.V"  : [ "Vec Load SegFF", "vld"  , "010000x", "110", "0000111", "Zve32x", "1", 1438, "10000", "xxxxx" ],
   "VLSEG4E8FF.V"   : [ "Vec Load SegFF", "vld"  , "011000x", "000", "0000111", "Zve32x", "1", 1439, "10000", "xxxxx" ],
   "VLSEG4E16FF.V"  : [ "Vec Load SegFF", "vld"  , "011000x", "101", "0000111", "Zve32x", "1", 1440, "10000", "xxxxx" ],
   "VLSEG4E32FF.V"  : [ "Vec Load SegFF", "vld"  , "011000x", "110", "0000111", "Zve32x", "1", 1441, "10000", "xxxxx" ],
   "VLSEG5E8FF.V"   : [ "Vec Load SegFF", "vld"  , "100000x", "000", "0000111", "Zve32x", "1", 1442, "10000", "xxxxx" ],
   "VLSEG5E16FF.V"  : [ "Vec Load SegFF", "vld"  , "100000x", "101", "0000111", "Zve32x", "1", 1443, "10000", "xxxxx" ],
   "VLSEG5E32FF.V"  : [ "Vec Load SegFF", "vld"  , "100000x", "110", "0000111", "Zve32x", "1", 1444, "10000", "xxxxx" ],
   "VLSEG6E8FF.V"   : [ "Vec Load SegFF", "vld"  , "101000x", "000", "0000111", "Zve32x", "1", 1445, "10000", "xxxxx" ],
   "VLSEG6E16FF.V"  : [ "Vec Load SegFF", "vld"  , "101000x", "101", "0000111", "Zve32x", "1", 1446, "10000", "xxxxx" ],
   "VLSEG6E32FF.V"  : [ "Vec Load SegFF", "vld"  , "101000x", "110", "0000111", "Zve32x", "1", 1447, "10000", "xxxxx" ],
   "VLSEG7E8FF.V"   : [ "Vec Load SegFF", "vld"  , "110000x", "000", "0000111", "Zve32x", "1", 1448, "10000", "xxxxx" ],
   "VLSEG7E16FF.V"  : [ "Vec Load SegFF", "vld"  , "110000x", "101", "0000111", "Zve32x", "1", 1449, "10000", "xxxxx" ],
   "VLSEG7E32FF.V"  : [ "Vec Load SegFF", "vld"  , "110000x", "110", "0000111", "Zve32x", "1", 1450, "10000", "xxxxx" ],
   "VLSEG8E8FF.V"   : [ "Vec Load SegFF", "vld"  , "111000x", "000", "0000111", "Zve32x", "1", 1451, "10000", "xxxxx" ],
   "VLSEG8E16FF.V"  : [ "Vec Load SegFF", "vld"  , "111000x", "101", "0000111", "Zve32x", "1", 1452, "10000", "xxxxx" ],
   "VLSEG8E32FF.V"  : [ "Vec Load SegFF", "vld"  , "111000x", "110", "0000111", "Zve32x", "1", 1453, "10000", "xxxxx" ],
   #--- Vector loads/stores - whole register ---
   "VL1RE8.V"       : [ "Vec Load WR"  , "vldr" , "0000001", "000", "0000111", "Zve32x", "1", 1200, "01000", "xxxxx" ],
   "VL1RE16.V"      : [ "Vec Load WR"  , "vldr" , "0000001", "101", "0000111", "Zve32x", "1", 1201, "01000", "xxxxx" ],
   "VL1RE32.V"      : [ "Vec Load WR"  , "vldr" , "0000001", "110", "0000111", "Zve32x", "1", 1202, "01000", "xxxxx" ],
   "VL2RE8.V"       : [ "Vec Load WR"  , "vldr" , "0010001", "000", "0000111", "Zve32x", "1", 1203, "01000", "xxxxx" ],
   "VL2RE16.V"      : [ "Vec Load WR"  , "vldr" , "0010001", "101", "0000111", "Zve32x", "1", 1204, "01000", "xxxxx" ],
   "VL2RE32.V"      : [ "Vec Load WR"  , "vldr" , "0010001", "110", "0000111", "Zve32x", "1", 1205, "01000", "xxxxx" ],
   "VL4RE8.V"       : [ "Vec Load WR"  , "vldr" , "0110001", "000", "0000111", "Zve32x", "1", 1206, "01000", "xxxxx" ],
   "VL4RE16.V"      : [ "Vec Load WR"  , "vldr" , "0110001", "101", "0000111", "Zve32x", "1", 1207, "01000", "xxxxx" ],
   "VL4RE32.V"      : [ "Vec Load WR"  , "vldr" , "0110001", "110", "0000111", "Zve32x", "1", 1208, "01000", "xxxxx" ],
   "VL8RE8.V"       : [ "Vec Load WR"  , "vldr" , "1110001", "000", "0000111", "Zve32x", "1", 1209, "01000", "xxxxx" ],
   "VL8RE16.V"      : [ "Vec Load WR"  , "vldr" , "1110001", "101", "0000111", "Zve32x", "1", 1210, "01000", "xxxxx" ],
   "VL8RE32.V"      : [ "Vec Load WR"  , "vldr" , "1110001", "110", "0000111", "Zve32x", "1", 1211, "01000", "xxxxx" ],
   "VS1R.V"         : [ "Vec Store WR" , "vstr" , "0000001", "000", "0100111", "Zve32x", "1", 1212, "01000", "xxxxx" ],
   "VS2R.V"         : [ "Vec Store WR" , "vstr" , "0010001", "000", "0100111", "Zve32x", "1", 1213, "01000", "xxxxx" ],
   "VS4R.V"         : [ "Vec Store WR" , "vstr" , "0110001", "000", "0100111", "Zve32x", "1", 1214, "01000", "xxxxx" ],
   "VS8R.V"         : [ "Vec Store WR" , "vstr" , "1110001", "000", "0100111", "Zve32x", "1", 1215, "01000", "xxxxx" ],
   #--- Integer arithmetic - add/subtract ---
   "VADD.VV"        : [ "Vec Arith"    , "vvv"  , "000000x", "000", "1010111", "Zve32x", "0", 1216, "xxxxx", "xxxxx" ],
   "VADD.VX"        : [ "Vec Arith"    , "vvx"  , "000000x", "100", "1010111", "Zve32x", "0", 1217, "xxxxx", "xxxxx" ],
   "VADD.VI"        : [ "Vec Arith"    , "vvi"  , "000000x", "011", "1010111", "Zve32x", "0", 1218, "xxxxx", "xxxxx" ],
   "VSUB.VV"        : [ "Vec Arith"    , "vvv"  , "000010x", "000", "1010111", "Zve32x", "0", 1219, "xxxxx", "xxxxx" ],
   "VSUB.VX"        : [ "Vec Arith"    , "vvx"  , "000010x", "100", "1010111", "Zve32x", "0", 1220, "xxxxx", "xxxxx" ],
   "VRSUB.VX"       : [ "Vec Arith"    , "vvx"  , "000011x", "100", "1010111", "Zve32x", "0", 1221, "xxxxx", "xxxxx" ],
   "VRSUB.VI"       : [ "Vec Arith"    , "vvi"  , "000011x", "011", "1010111", "Zve32x", "0", 1222, "xxxxx", "xxxxx" ],
   #--- Integer arithmetic - widening add/subtract ---
   "VWADDU.VV"      : [ "Vec Widen"    , "vvv"  , "110000x", "010", "1010111", "Zve32x", "0", 1223, "xxxxx", "xxxxx" ],
   "VWADDU.VX"      : [ "Vec Widen"    , "vvx"  , "110000x", "110", "1010111", "Zve32x", "0", 1224, "xxxxx", "xxxxx" ],
   "VWSUBU.VV"      : [ "Vec Widen"    , "vvv"  , "110010x", "010", "1010111", "Zve32x", "0", 1225, "xxxxx", "xxxxx" ],
   "VWSUBU.VX"      : [ "Vec Widen"    , "vvx"  , "110010x", "110", "1010111", "Zve32x", "0", 1226, "xxxxx", "xxxxx" ],
   "VWADD.VV"       : [ "Vec Widen"    , "vvv"  , "110001x", "010", "1010111", "Zve32x", "0", 1227, "xxxxx", "xxxxx" ],
   "VWADD.VX"       : [ "Vec Widen"    , "vvx"  , "110001x", "110", "1010111", "Zve32x", "0", 1228, "xxxxx", "xxxxx" ],
   "VWSUB.VV"       : [ "Vec Widen"    , "vvv"  , "110011x", "010", "1010111", "Zve32x", "0", 1229, "xxxxx", "xxxxx" ],
   "VWSUB.VX"       : [ "Vec Widen"    , "vvx"  , "110011x", "110", "1010111", "Zve32x", "0", 1230, "xxxxx", "xxxxx" ],
   "VWADDU.WV"      : [ "Vec Widen"    , "vvv"  , "110100x", "010", "1010111", "Zve32x", "0", 1231, "xxxxx", "xxxxx" ],
   "VWADDU.WX"      : [ "Vec Widen"    , "vvx"  , "110100x", "110", "1010111", "Zve32x", "0", 1232, "xxxxx", "xxxxx" ],
   "VWSUBU.WV"      : [ "Vec Widen"    , "vvv"  , "110110x", "010", "1010111", "Zve32x", "0", 1233, "xxxxx", "xxxxx" ],
   "VWSUBU.WX"      : [ "Vec Widen"    , "vvx"  , "110110x", "110", "1010111", "Zve32x", "0", 1234, "xxxxx", "xxxxx" ],
   "VWADD.WV"       : [ "Vec Widen"    , "vvv"  , "110101x", "010", "1010111", "Zve32x", "0", 1235, "xxxxx", "xxxxx" ],
   "VWADD.WX"       : [ "Vec Widen"    , "vvx"  , "110101x", "110", "1010111", "Zve32x", "0", 1236, "xxxxx", "xxxxx" ],
   "VWSUB.WV"       : [ "Vec Widen"    , "vvv"  , "110111x", "010", "1010111", "Zve32x", "0", 1237, "xxxxx", "xxxxx" ],
   "VWSUB.WX"       : [ "Vec Widen"    , "vvx"  , "110111x", "110", "1010111", "Zve32x", "0", 1238, "xxxxx", "xxxxx" ],
   #--- Integer arithmetic - integer extension ---
   "VZEXT.VF2"      : [ "Vec Ext"      , "vldw" , "010010x", "010", "1010111", "Zve32x", "0", 1239, "xxxxx", "00110" ],
   "VSEXT.VF2"      : [ "Vec Ext"      , "vldw" , "010010x", "010", "1010111", "Zve32x", "0", 1240, "xxxxx", "00111" ],
   "VZEXT.VF4"      : [ "Vec Ext"      , "vldw" , "010010x", "010", "1010111", "Zve32x", "0", 1241, "xxxxx", "00100" ],
   "VSEXT.VF4"      : [ "Vec Ext"      , "vldw" , "010010x", "010", "1010111", "Zve32x", "0", 1242, "xxxxx", "00101" ],
   "VZEXT.VF8"      : [ "Vec Ext"      , "vldw" , "010010x", "010", "1010111", "Zve32x", "0", 1243, "xxxxx", "00010" ],
   "VSEXT.VF8"      : [ "Vec Ext"      , "vldw" , "010010x", "010", "1010111", "Zve32x", "0", 1244, "xxxxx", "00011" ],
   #--- Integer arithmetic - add-with-carry/subtract-with-borrow ---
   "VADC.VVM"       : [ "Vec Carry"    , "vvvm" , "0100000", "000", "1010111", "Zve32x", "0", 1245, "xxxxx", "xxxxx" ],
   "VADC.VXM"       : [ "Vec Carry"    , "vvxm" , "0100000", "100", "1010111", "Zve32x", "0", 1246, "xxxxx", "xxxxx" ],
   "VADC.VIM"       : [ "Vec Carry"    , "vvim" , "0100000", "011", "1010111", "Zve32x", "0", 1247, "xxxxx", "xxxxx" ],
   "VMADC.VVM"      : [ "Vec Carry"    , "vvvm" , "0100010", "000", "1010111", "Zve32x", "0", 1248, "xxxxx", "xxxxx" ],
   "VMADC.VXM"      : [ "Vec Carry"    , "vvxm" , "0100010", "100", "1010111", "Zve32x", "0", 1249, "xxxxx", "xxxxx" ],
   "VMADC.VIM"      : [ "Vec Carry"    , "vvim" , "0100010", "011", "1010111", "Zve32x", "0", 1250, "xxxxx", "xxxxx" ],
   "VMADC.VV"       : [ "Vec Carry"    , "vvvn"  , "0100011", "000", "1010111", "Zve32x", "0", 1251, "xxxxx", "xxxxx" ],
   "VMADC.VX"       : [ "Vec Carry"    , "vvxn"  , "0100011", "100", "1010111", "Zve32x", "0", 1252, "xxxxx", "xxxxx" ],
   "VMADC.VI"       : [ "Vec Carry"    , "vvin"  , "0100011", "011", "1010111", "Zve32x", "0", 1253, "xxxxx", "xxxxx" ],
   "VSBC.VVM"       : [ "Vec Carry"    , "vvvm" , "0100100", "000", "1010111", "Zve32x", "0", 1254, "xxxxx", "xxxxx" ],
   "VSBC.VXM"       : [ "Vec Carry"    , "vvxm" , "0100100", "100", "1010111", "Zve32x", "0", 1255, "xxxxx", "xxxxx" ],
   "VMSBC.VVM"      : [ "Vec Carry"    , "vvvm" , "0100110", "000", "1010111", "Zve32x", "0", 1256, "xxxxx", "xxxxx" ],
   "VMSBC.VXM"      : [ "Vec Carry"    , "vvxm" , "0100110", "100", "1010111", "Zve32x", "0", 1257, "xxxxx", "xxxxx" ],
   "VMSBC.VV"       : [ "Vec Carry"    , "vvvn"  , "0100111", "000", "1010111", "Zve32x", "0", 1258, "xxxxx", "xxxxx" ],
   "VMSBC.VX"       : [ "Vec Carry"    , "vvxn"  , "0100111", "100", "1010111", "Zve32x", "0", 1259, "xxxxx", "xxxxx" ],
   #--- Integer arithmetic - bitwise logical ---
   "VAND.VV"        : [ "Vec Logical"  , "vvv"  , "001001x", "000", "1010111", "Zve32x", "0", 1260, "xxxxx", "xxxxx" ],
   "VAND.VX"        : [ "Vec Logical"  , "vvx"  , "001001x", "100", "1010111", "Zve32x", "0", 1261, "xxxxx", "xxxxx" ],
   "VAND.VI"        : [ "Vec Logical"  , "vvi"  , "001001x", "011", "1010111", "Zve32x", "0", 1262, "xxxxx", "xxxxx" ],
   "VOR.VV"         : [ "Vec Logical"  , "vvv"  , "001010x", "000", "1010111", "Zve32x", "0", 1263, "xxxxx", "xxxxx" ],
   "VOR.VX"         : [ "Vec Logical"  , "vvx"  , "001010x", "100", "1010111", "Zve32x", "0", 1264, "xxxxx", "xxxxx" ],
   "VOR.VI"         : [ "Vec Logical"  , "vvi"  , "001010x", "011", "1010111", "Zve32x", "0", 1265, "xxxxx", "xxxxx" ],
   "VXOR.VV"        : [ "Vec Logical"  , "vvv"  , "001011x", "000", "1010111", "Zve32x", "0", 1266, "xxxxx", "xxxxx" ],
   "VXOR.VX"        : [ "Vec Logical"  , "vvx"  , "001011x", "100", "1010111", "Zve32x", "0", 1267, "xxxxx", "xxxxx" ],
   "VXOR.VI"        : [ "Vec Logical"  , "vvi"  , "001011x", "011", "1010111", "Zve32x", "0", 1268, "xxxxx", "xxxxx" ],
   #--- Integer arithmetic - shifts ---
   "VSLL.VV"        : [ "Vec Shifts"   , "vvv"  , "100101x", "000", "1010111", "Zve32x", "0", 1269, "xxxxx", "xxxxx" ],
   "VSLL.VX"        : [ "Vec Shifts"   , "vvx"  , "100101x", "100", "1010111", "Zve32x", "0", 1270, "xxxxx", "xxxxx" ],
   "VSLL.VI"        : [ "Vec Shifts"   , "vvi"  , "100101x", "011", "1010111", "Zve32x", "0", 1271, "xxxxx", "xxxxx" ],
   "VSRL.VV"        : [ "Vec Shifts"   , "vvv"  , "101000x", "000", "1010111", "Zve32x", "0", 1272, "xxxxx", "xxxxx" ],
   "VSRL.VX"        : [ "Vec Shifts"   , "vvx"  , "101000x", "100", "1010111", "Zve32x", "0", 1273, "xxxxx", "xxxxx" ],
   "VSRL.VI"        : [ "Vec Shifts"   , "vvi"  , "101000x", "011", "1010111", "Zve32x", "0", 1274, "xxxxx", "xxxxx" ],
   "VSRA.VV"        : [ "Vec Shifts"   , "vvv"  , "101001x", "000", "1010111", "Zve32x", "0", 1275, "xxxxx", "xxxxx" ],
   "VSRA.VX"        : [ "Vec Shifts"   , "vvx"  , "101001x", "100", "1010111", "Zve32x", "0", 1276, "xxxxx", "xxxxx" ],
   "VSRA.VI"        : [ "Vec Shifts"   , "vvi"  , "101001x", "011", "1010111", "Zve32x", "0", 1277, "xxxxx", "xxxxx" ],
   #--- Integer arithmetic - narrowing shifts ---
   "VNSRL.WV"       : [ "Vec Narrow"   , "vvv"  , "101100x", "000", "1010111", "Zve32x", "0", 1278, "xxxxx", "xxxxx" ],
   "VNSRL.WX"       : [ "Vec Narrow"   , "vvx"  , "101100x", "100", "1010111", "Zve32x", "0", 1279, "xxxxx", "xxxxx" ],
   "VNSRL.WI"       : [ "Vec Narrow"   , "vvi"  , "101100x", "011", "1010111", "Zve32x", "0", 1280, "xxxxx", "xxxxx" ],
   "VNSRA.WV"       : [ "Vec Narrow"   , "vvv"  , "101101x", "000", "1010111", "Zve32x", "0", 1281, "xxxxx", "xxxxx" ],
   "VNSRA.WX"       : [ "Vec Narrow"   , "vvx"  , "101101x", "100", "1010111", "Zve32x", "0", 1282, "xxxxx", "xxxxx" ],
   "VNSRA.WI"       : [ "Vec Narrow"   , "vvi"  , "101101x", "011", "1010111", "Zve32x", "0", 1283, "xxxxx", "xxxxx" ],
   #--- Integer arithmetic - compare ---
   "VMSEQ.VV"       : [ "Vec Compare"  , "vvv"  , "011000x", "000", "1010111", "Zve32x", "0", 1284, "xxxxx", "xxxxx" ],
   "VMSEQ.VX"       : [ "Vec Compare"  , "vvx"  , "011000x", "100", "1010111", "Zve32x", "0", 1285, "xxxxx", "xxxxx" ],
   "VMSEQ.VI"       : [ "Vec Compare"  , "vvi"  , "011000x", "011", "1010111", "Zve32x", "0", 1286, "xxxxx", "xxxxx" ],
   "VMSNE.VV"       : [ "Vec Compare"  , "vvv"  , "011001x", "000", "1010111", "Zve32x", "0", 1287, "xxxxx", "xxxxx" ],
   "VMSNE.VX"       : [ "Vec Compare"  , "vvx"  , "011001x", "100", "1010111", "Zve32x", "0", 1288, "xxxxx", "xxxxx" ],
   "VMSNE.VI"       : [ "Vec Compare"  , "vvi"  , "011001x", "011", "1010111", "Zve32x", "0", 1289, "xxxxx", "xxxxx" ],
   "VMSLTU.VV"      : [ "Vec Compare"  , "vvv"  , "011010x", "000", "1010111", "Zve32x", "0", 1290, "xxxxx", "xxxxx" ],
   "VMSLTU.VX"      : [ "Vec Compare"  , "vvx"  , "011010x", "100", "1010111", "Zve32x", "0", 1291, "xxxxx", "xxxxx" ],
   "VMSLT.VV"       : [ "Vec Compare"  , "vvv"  , "011011x", "000", "1010111", "Zve32x", "0", 1292, "xxxxx", "xxxxx" ],
   "VMSLT.VX"       : [ "Vec Compare"  , "vvx"  , "011011x", "100", "1010111", "Zve32x", "0", 1293, "xxxxx", "xxxxx" ],
   "VMSLEU.VV"      : [ "Vec Compare"  , "vvv"  , "011100x", "000", "1010111", "Zve32x", "0", 1294, "xxxxx", "xxxxx" ],
   "VMSLEU.VX"      : [ "Vec Compare"  , "vvx"  , "011100x", "100", "1010111", "Zve32x", "0", 1295, "xxxxx", "xxxxx" ],
   "VMSLEU.VI"      : [ "Vec Compare"  , "vvi"  , "011100x", "011", "1010111", "Zve32x", "0", 1296, "xxxxx", "xxxxx" ],
   "VMSLE.VV"       : [ "Vec Compare"  , "vvv"  , "011101x", "000", "1010111", "Zve32x", "0", 1297, "xxxxx", "xxxxx" ],
   "VMSLE.VX"       : [ "Vec Compare"  , "vvx"  , "011101x", "100", "1010111", "Zve32x", "0", 1298, "xxxxx", "xxxxx" ],
   "VMSLE.VI"       : [ "Vec Compare"  , "vvi"  , "011101x", "011", "1010111", "Zve32x", "0", 1299, "xxxxx", "xxxxx" ],
   "VMSGTU.VX"      : [ "Vec Compare"  , "vvx"  , "011110x", "100", "1010111", "Zve32x", "0", 1300, "xxxxx", "xxxxx" ],
   "VMSGTU.VI"      : [ "Vec Compare"  , "vvi"  , "011110x", "011", "1010111", "Zve32x", "0", 1301, "xxxxx", "xxxxx" ],
   "VMSGT.VX"       : [ "Vec Compare"  , "vvx"  , "011111x", "100", "1010111", "Zve32x", "0", 1302, "xxxxx", "xxxxx" ],
   "VMSGT.VI"       : [ "Vec Compare"  , "vvi"  , "011111x", "011", "1010111", "Zve32x", "0", 1303, "xxxxx", "xxxxx" ],
   #--- Integer arithmetic - min/max ---
   "VMINU.VV"       : [ "Vec Min/Max"  , "vvv"  , "000100x", "000", "1010111", "Zve32x", "0", 1304, "xxxxx", "xxxxx" ],
   "VMINU.VX"       : [ "Vec Min/Max"  , "vvx"  , "000100x", "100", "1010111", "Zve32x", "0", 1305, "xxxxx", "xxxxx" ],
   "VMIN.VV"        : [ "Vec Min/Max"  , "vvv"  , "000101x", "000", "1010111", "Zve32x", "0", 1306, "xxxxx", "xxxxx" ],
   "VMIN.VX"        : [ "Vec Min/Max"  , "vvx"  , "000101x", "100", "1010111", "Zve32x", "0", 1307, "xxxxx", "xxxxx" ],
   "VMAXU.VV"       : [ "Vec Min/Max"  , "vvv"  , "000110x", "000", "1010111", "Zve32x", "0", 1308, "xxxxx", "xxxxx" ],
   "VMAXU.VX"       : [ "Vec Min/Max"  , "vvx"  , "000110x", "100", "1010111", "Zve32x", "0", 1309, "xxxxx", "xxxxx" ],
   "VMAX.VV"        : [ "Vec Min/Max"  , "vvv"  , "000111x", "000", "1010111", "Zve32x", "0", 1310, "xxxxx", "xxxxx" ],
   "VMAX.VX"        : [ "Vec Min/Max"  , "vvx"  , "000111x", "100", "1010111", "Zve32x", "0", 1311, "xxxxx", "xxxxx" ],
   #--- Integer arithmetic - multiply ---
   "VMUL.VV"        : [ "Vec Multiply" , "vvv"  , "100101x", "010", "1010111", "Zve32x", "0", 1312, "xxxxx", "xxxxx" ],
   "VMUL.VX"        : [ "Vec Multiply" , "vvx"  , "100101x", "110", "1010111", "Zve32x", "0", 1313, "xxxxx", "xxxxx" ],
   "VMULH.VV"       : [ "Vec Multiply" , "vvv"  , "100111x", "010", "1010111", "Zve32x", "0", 1314, "xxxxx", "xxxxx" ],
   "VMULH.VX"       : [ "Vec Multiply" , "vvx"  , "100111x", "110", "1010111", "Zve32x", "0", 1315, "xxxxx", "xxxxx" ],
   "VMULHU.VV"      : [ "Vec Multiply" , "vvv"  , "100100x", "010", "1010111", "Zve32x", "0", 1316, "xxxxx", "xxxxx" ],
   "VMULHU.VX"      : [ "Vec Multiply" , "vvx"  , "100100x", "110", "1010111", "Zve32x", "0", 1317, "xxxxx", "xxxxx" ],
   "VMULHSU.VV"     : [ "Vec Multiply" , "vvv"  , "100110x", "010", "1010111", "Zve32x", "0", 1318, "xxxxx", "xxxxx" ],
   "VMULHSU.VX"     : [ "Vec Multiply" , "vvx"  , "100110x", "110", "1010111", "Zve32x", "0", 1319, "xxxxx", "xxxxx" ],
   #--- Integer arithmetic - divide ---
   "VDIVU.VV"       : [ "Vec Divide"   , "vvv"  , "100000x", "010", "1010111", "Zve32x", "0", 1320, "xxxxx", "xxxxx" ],
   "VDIVU.VX"       : [ "Vec Divide"   , "vvx"  , "100000x", "110", "1010111", "Zve32x", "0", 1321, "xxxxx", "xxxxx" ],
   "VDIV.VV"        : [ "Vec Divide"   , "vvv"  , "100001x", "010", "1010111", "Zve32x", "0", 1322, "xxxxx", "xxxxx" ],
   "VDIV.VX"        : [ "Vec Divide"   , "vvx"  , "100001x", "110", "1010111", "Zve32x", "0", 1323, "xxxxx", "xxxxx" ],
   "VREMU.VV"       : [ "Vec Divide"   , "vvv"  , "100010x", "010", "1010111", "Zve32x", "0", 1324, "xxxxx", "xxxxx" ],
   "VREMU.VX"       : [ "Vec Divide"   , "vvx"  , "100010x", "110", "1010111", "Zve32x", "0", 1325, "xxxxx", "xxxxx" ],
   "VREM.VV"        : [ "Vec Divide"   , "vvv"  , "100011x", "010", "1010111", "Zve32x", "0", 1326, "xxxxx", "xxxxx" ],
   "VREM.VX"        : [ "Vec Divide"   , "vvx"  , "100011x", "110", "1010111", "Zve32x", "0", 1327, "xxxxx", "xxxxx" ],
   #--- Integer arithmetic - widening multiply ---
   "VWMUL.VV"       : [ "Vec Widen"    , "vvv"  , "111011x", "010", "1010111", "Zve32x", "0", 1328, "xxxxx", "xxxxx" ],
   "VWMUL.VX"       : [ "Vec Widen"    , "vvx"  , "111011x", "110", "1010111", "Zve32x", "0", 1329, "xxxxx", "xxxxx" ],
   "VWMULU.VV"      : [ "Vec Widen"    , "vvv"  , "111000x", "010", "1010111", "Zve32x", "0", 1330, "xxxxx", "xxxxx" ],
   "VWMULU.VX"      : [ "Vec Widen"    , "vvx"  , "111000x", "110", "1010111", "Zve32x", "0", 1331, "xxxxx", "xxxxx" ],
   "VWMULSU.VV"     : [ "Vec Widen"    , "vvv"  , "111010x", "010", "1010111", "Zve32x", "0", 1332, "xxxxx", "xxxxx" ],
   "VWMULSU.VX"     : [ "Vec Widen"    , "vvx"  , "111010x", "110", "1010111", "Zve32x", "0", 1333, "xxxxx", "xxxxx" ],
   #--- Integer arithmetic - single-width multiply-add ---
   "VMACC.VV"       : [ "Vec MulAdd"   , "vvv"  , "101101x", "010", "1010111", "Zve32x", "0", 1334, "xxxxx", "xxxxx" ],
   "VMACC.VX"       : [ "Vec MulAdd"   , "vxv"  , "101101x", "110", "1010111", "Zve32x", "0", 1335, "xxxxx", "xxxxx" ],
   "VNMSAC.VV"      : [ "Vec MulAdd"   , "vvv"  , "101111x", "010", "1010111", "Zve32x", "0", 1336, "xxxxx", "xxxxx" ],
   "VNMSAC.VX"      : [ "Vec MulAdd"   , "vxv"  , "101111x", "110", "1010111", "Zve32x", "0", 1337, "xxxxx", "xxxxx" ],
   "VMADD.VV"       : [ "Vec MulAdd"   , "vvv"  , "101001x", "010", "1010111", "Zve32x", "0", 1338, "xxxxx", "xxxxx" ],
   "VMADD.VX"       : [ "Vec MulAdd"   , "vxv"  , "101001x", "110", "1010111", "Zve32x", "0", 1339, "xxxxx", "xxxxx" ],
   "VNMSUB.VV"      : [ "Vec MulAdd"   , "vvv"  , "101011x", "010", "1010111", "Zve32x", "0", 1340, "xxxxx", "xxxxx" ],
   "VNMSUB.VX"      : [ "Vec MulAdd"   , "vxv"  , "101011x", "110", "1010111", "Zve32x", "0", 1341, "xxxxx", "xxxxx" ],
   #--- Integer arithmetic - widening multiply-add ---
   "VWMACCU.VV"     : [ "Vec Widen"    , "vvv"  , "111100x", "010", "1010111", "Zve32x", "0", 1342, "xxxxx", "xxxxx" ],
   "VWMACCU.VX"     : [ "Vec Widen"    , "vxv"  , "111100x", "110", "1010111", "Zve32x", "0", 1343, "xxxxx", "xxxxx" ],
   "VWMACC.VV"      : [ "Vec Widen"    , "vvv"  , "111101x", "010", "1010111", "Zve32x", "0", 1344, "xxxxx", "xxxxx" ],
   "VWMACC.VX"      : [ "Vec Widen"    , "vxv"  , "111101x", "110", "1010111", "Zve32x", "0", 1345, "xxxxx", "xxxxx" ],
   "VWMACCSU.VV"    : [ "Vec Widen"    , "vvv"  , "111111x", "010", "1010111", "Zve32x", "0", 1346, "xxxxx", "xxxxx" ],
   "VWMACCSU.VX"    : [ "Vec Widen"    , "vxv"  , "111111x", "110", "1010111", "Zve32x", "0", 1347, "xxxxx", "xxxxx" ],
   "VWMACCUS.VX"    : [ "Vec Widen"    , "vxv"  , "111110x", "110", "1010111", "Zve32x", "0", 1348, "xxxxx", "xxxxx" ],
   #--- Integer arithmetic - merge/move ---
   "VMERGE.VVM"     : [ "Vec Merge"    , "vvvm" , "0101110", "000", "1010111", "Zve32x", "0", 1349, "xxxxx", "xxxxx" ],
   "VMERGE.VXM"     : [ "Vec Merge"    , "vvxm" , "0101110", "100", "1010111", "Zve32x", "0", 1350, "xxxxx", "xxxxx" ],
   "VMERGE.VIM"     : [ "Vec Merge"    , "vvim" , "0101110", "011", "1010111", "Zve32x", "0", 1351, "xxxxx", "xxxxx" ],
   "VMV.V.V"        : [ "Vec Merge"    , "vmvv"  , "0101111", "000", "1010111", "Zve32x", "0", 1352, "00000", "xxxxx" ],
   "VMV.V.X"        : [ "Vec Merge"    , "vmvx"  , "0101111", "100", "1010111", "Zve32x", "0", 1353, "00000", "xxxxx" ],
   "VMV.V.I"        : [ "Vec Merge"    , "vmvi"  , "0101111", "011", "1010111", "Zve32x", "0", 1354, "00000", "xxxxx" ],
   #--- Fixed-point arithmetic - saturating add/subtract ---
   "VSADDU.VV"      : [ "Vec Fixed-Pt" , "vvv"  , "100000x", "000", "1010111", "Zve32x", "0", 1355, "xxxxx", "xxxxx" ],
   "VSADDU.VX"      : [ "Vec Fixed-Pt" , "vvx"  , "100000x", "100", "1010111", "Zve32x", "0", 1356, "xxxxx", "xxxxx" ],
   "VSADDU.VI"      : [ "Vec Fixed-Pt" , "vvi"  , "100000x", "011", "1010111", "Zve32x", "0", 1357, "xxxxx", "xxxxx" ],
   "VSADD.VV"       : [ "Vec Fixed-Pt" , "vvv"  , "100001x", "000", "1010111", "Zve32x", "0", 1358, "xxxxx", "xxxxx" ],
   "VSADD.VX"       : [ "Vec Fixed-Pt" , "vvx"  , "100001x", "100", "1010111", "Zve32x", "0", 1359, "xxxxx", "xxxxx" ],
   "VSADD.VI"       : [ "Vec Fixed-Pt" , "vvi"  , "100001x", "011", "1010111", "Zve32x", "0", 1360, "xxxxx", "xxxxx" ],
   "VSSUBU.VV"      : [ "Vec Fixed-Pt" , "vvv"  , "100010x", "000", "1010111", "Zve32x", "0", 1361, "xxxxx", "xxxxx" ],
   "VSSUBU.VX"      : [ "Vec Fixed-Pt" , "vvx"  , "100010x", "100", "1010111", "Zve32x", "0", 1362, "xxxxx", "xxxxx" ],
   "VSSUB.VV"       : [ "Vec Fixed-Pt" , "vvv"  , "100011x", "000", "1010111", "Zve32x", "0", 1363, "xxxxx", "xxxxx" ],
   "VSSUB.VX"       : [ "Vec Fixed-Pt" , "vvx"  , "100011x", "100", "1010111", "Zve32x", "0", 1364, "xxxxx", "xxxxx" ],
   #--- Fixed-point arithmetic - averaging add/subtract ---
   "VAADDU.VV"      : [ "Vec Fixed-Pt" , "vvv"  , "001000x", "010", "1010111", "Zve32x", "0", 1365, "xxxxx", "xxxxx" ],
   "VAADDU.VX"      : [ "Vec Fixed-Pt" , "vvx"  , "001000x", "110", "1010111", "Zve32x", "0", 1366, "xxxxx", "xxxxx" ],
   "VAADD.VV"       : [ "Vec Fixed-Pt" , "vvv"  , "001001x", "010", "1010111", "Zve32x", "0", 1367, "xxxxx", "xxxxx" ],
   "VAADD.VX"       : [ "Vec Fixed-Pt" , "vvx"  , "001001x", "110", "1010111", "Zve32x", "0", 1368, "xxxxx", "xxxxx" ],
   "VASUBU.VV"      : [ "Vec Fixed-Pt" , "vvv"  , "001010x", "010", "1010111", "Zve32x", "0", 1369, "xxxxx", "xxxxx" ],
   "VASUBU.VX"      : [ "Vec Fixed-Pt" , "vvx"  , "001010x", "110", "1010111", "Zve32x", "0", 1370, "xxxxx", "xxxxx" ],
   "VASUB.VV"       : [ "Vec Fixed-Pt" , "vvv"  , "001011x", "010", "1010111", "Zve32x", "0", 1371, "xxxxx", "xxxxx" ],
   "VASUB.VX"       : [ "Vec Fixed-Pt" , "vvx"  , "001011x", "110", "1010111", "Zve32x", "0", 1372, "xxxxx", "xxxxx" ],
   #--- Fixed-point arithmetic - fractional multiply ---
   "VSMUL.VV"       : [ "Vec Fixed-Pt" , "vvv"  , "100111x", "000", "1010111", "Zve32x", "0", 1373, "xxxxx", "xxxxx" ],
   "VSMUL.VX"       : [ "Vec Fixed-Pt" , "vvx"  , "100111x", "100", "1010111", "Zve32x", "0", 1374, "xxxxx", "xxxxx" ],
   #--- Fixed-point arithmetic - scaling shift ---
   "VSSRL.VV"       : [ "Vec Fixed-Pt" , "vvv"  , "101010x", "000", "1010111", "Zve32x", "0", 1375, "xxxxx", "xxxxx" ],
   "VSSRL.VX"       : [ "Vec Fixed-Pt" , "vvx"  , "101010x", "100", "1010111", "Zve32x", "0", 1376, "xxxxx", "xxxxx" ],
   "VSSRL.VI"       : [ "Vec Fixed-Pt" , "vvi"  , "101010x", "011", "1010111", "Zve32x", "0", 1377, "xxxxx", "xxxxx" ],
   "VSSRA.VV"       : [ "Vec Fixed-Pt" , "vvv"  , "101011x", "000", "1010111", "Zve32x", "0", 1378, "xxxxx", "xxxxx" ],
   "VSSRA.VX"       : [ "Vec Fixed-Pt" , "vvx"  , "101011x", "100", "1010111", "Zve32x", "0", 1379, "xxxxx", "xxxxx" ],
   "VSSRA.VI"       : [ "Vec Fixed-Pt" , "vvi"  , "101011x", "011", "1010111", "Zve32x", "0", 1380, "xxxxx", "xxxxx" ],
   #--- Fixed-point arithmetic - narrowing clip ---
   "VNCLIPU.WV"     : [ "Vec Fixed-Pt" , "vvv"  , "101110x", "000", "1010111", "Zve32x", "0", 1381, "xxxxx", "xxxxx" ],
   "VNCLIPU.WX"     : [ "Vec Fixed-Pt" , "vvx"  , "101110x", "100", "1010111", "Zve32x", "0", 1382, "xxxxx", "xxxxx" ],
   "VNCLIPU.WI"     : [ "Vec Fixed-Pt" , "vvi"  , "101110x", "011", "1010111", "Zve32x", "0", 1383, "xxxxx", "xxxxx" ],
   "VNCLIP.WV"      : [ "Vec Fixed-Pt" , "vvv"  , "101111x", "000", "1010111", "Zve32x", "0", 1384, "xxxxx", "xxxxx" ],
   "VNCLIP.WX"      : [ "Vec Fixed-Pt" , "vvx"  , "101111x", "100", "1010111", "Zve32x", "0", 1385, "xxxxx", "xxxxx" ],
   "VNCLIP.WI"      : [ "Vec Fixed-Pt" , "vvi"  , "101111x", "011", "1010111", "Zve32x", "0", 1386, "xxxxx", "xxxxx" ],
   #--- Reduction - integer ---
   "VREDSUM.VS"     : [ "Vec Reduce"   , "vvv"  , "000000x", "010", "1010111", "Zve32x", "0", 1387, "xxxxx", "xxxxx" ],
   "VREDMAXU.VS"    : [ "Vec Reduce"   , "vvv"  , "000110x", "010", "1010111", "Zve32x", "0", 1388, "xxxxx", "xxxxx" ],
   "VREDMAX.VS"     : [ "Vec Reduce"   , "vvv"  , "000111x", "010", "1010111", "Zve32x", "0", 1389, "xxxxx", "xxxxx" ],
   "VREDMINU.VS"    : [ "Vec Reduce"   , "vvv"  , "000100x", "010", "1010111", "Zve32x", "0", 1390, "xxxxx", "xxxxx" ],
   "VREDMIN.VS"     : [ "Vec Reduce"   , "vvv"  , "000101x", "010", "1010111", "Zve32x", "0", 1391, "xxxxx", "xxxxx" ],
   "VREDAND.VS"     : [ "Vec Reduce"   , "vvv"  , "000001x", "010", "1010111", "Zve32x", "0", 1392, "xxxxx", "xxxxx" ],
   "VREDOR.VS"      : [ "Vec Reduce"   , "vvv"  , "000010x", "010", "1010111", "Zve32x", "0", 1393, "xxxxx", "xxxxx" ],
   "VREDXOR.VS"     : [ "Vec Reduce"   , "vvv"  , "000011x", "010", "1010111", "Zve32x", "0", 1394, "xxxxx", "xxxxx" ],
   "VWREDSUMU.VS"   : [ "Vec Reduce"   , "vvv"  , "110000x", "000", "1010111", "Zve32x", "0", 1395, "xxxxx", "xxxxx" ],
   "VWREDSUM.VS"    : [ "Vec Reduce"   , "vvv"  , "110001x", "000", "1010111", "Zve32x", "0", 1396, "xxxxx", "xxxxx" ],
   #--- Mask instructions ---
   "VMAND.MM"       : [ "Vec Mask"     , "vmm"  , "0110011", "010", "1010111", "Zve32x", "0", 1397, "xxxxx", "xxxxx" ],
   "VMNAND.MM"      : [ "Vec Mask"     , "vmm"  , "0111011", "010", "1010111", "Zve32x", "0", 1398, "xxxxx", "xxxxx" ],
   "VMANDN.MM"      : [ "Vec Mask"     , "vmm"  , "0110001", "010", "1010111", "Zve32x", "0", 1399, "xxxxx", "xxxxx" ],
   "VMXOR.MM"       : [ "Vec Mask"     , "vmm"  , "0110111", "010", "1010111", "Zve32x", "0", 1400, "xxxxx", "xxxxx" ],
   "VMOR.MM"        : [ "Vec Mask"     , "vmm"  , "0110101", "010", "1010111", "Zve32x", "0", 1401, "xxxxx", "xxxxx" ],
   "VMNOR.MM"       : [ "Vec Mask"     , "vmm"  , "0111101", "010", "1010111", "Zve32x", "0", 1402, "xxxxx", "xxxxx" ],
   "VMORN.MM"       : [ "Vec Mask"     , "vmm"  , "0111001", "010", "1010111", "Zve32x", "0", 1403, "xxxxx", "xxxxx" ],
   "VMXNOR.MM"      : [ "Vec Mask"     , "vmm"  , "0111111", "010", "1010111", "Zve32x", "0", 1404, "xxxxx", "xxxxx" ],
   "VMMV.M"         : [ "Vec Mask"     , "vm1"  , "0110011", "010", "1010111", "Zve32x", "0", 1405, "xxxxx", "xxxxx" ], #alias of vmand.mm
   "VMCLR.M"        : [ "Vec Mask"     , "vm0"  , "0110111", "010", "1010111", "Zve32x", "0", 1406, "xxxxx", "xxxxx" ], #alias of vmxor.mm
   "VMSET.M"        : [ "Vec Mask"     , "vm0"  , "0111111", "010", "1010111", "Zve32x", "0", 1407, "xxxxx", "xxxxx" ], #alias of vmxnor.mm
   "VMNOT.M"        : [ "Vec Mask"     , "vm1"  , "0111011", "010", "1010111", "Zve32x", "0", 1408, "xxxxx", "xxxxx" ], #alias of vmnand.mm
   "VCPOP.M"        : [ "Vec Mask"     , "vrd"  , "010000x", "010", "1010111", "Zve32x", "0", 1409, "xxxxx", "10000" ],
   "VFIRST.M"       : [ "Vec Mask"     , "vrd"  , "010000x", "010", "1010111", "Zve32x", "0", 1410, "xxxxx", "10001" ],
   "VMSBF.M"        : [ "Vec Mask"     , "vldw" , "010100x", "010", "1010111", "Zve32x", "0", 1411, "xxxxx", "00001" ],
   "VMSIF.M"        : [ "Vec Mask"     , "vldw" , "010100x", "010", "1010111", "Zve32x", "0", 1412, "xxxxx", "00011" ],
   "VMSOF.M"        : [ "Vec Mask"     , "vldw" , "010100x", "010", "1010111", "Zve32x", "0", 1413, "xxxxx", "00010" ],
   "VIOTA.M"        : [ "Vec Mask"     , "vldw" , "010100x", "010", "1010111", "Zve32x", "0", 1414, "xxxxx", "10000" ],
   "VID.V"          : [ "Vec Mask"     , "vd1"  , "010100x", "010", "1010111", "Zve32x", "0", 1415, "00000", "10001" ],
   #--- Permutation - scalar move ---
   "VMV.X.S"        : [ "Vec Permute"  , "vxs"  , "0100001", "010", "1010111", "Zve32x", "0", 1416, "xxxxx", "00000" ],
   "VMV.S.X"        : [ "Vec Permute"  , "vsx"  , "0100001", "110", "1010111", "Zve32x", "0", 1417, "00000", "xxxxx" ],
   #--- Permutation - slides ---
   "VSLIDEUP.VX"    : [ "Vec Permute"  , "vvx"  , "001110x", "100", "1010111", "Zve32x", "0", 1418, "xxxxx", "xxxxx" ],
   "VSLIDEUP.VI"    : [ "Vec Permute"  , "vvi"  , "001110x", "011", "1010111", "Zve32x", "0", 1419, "xxxxx", "xxxxx" ],
   "VSLIDEDOWN.VX"  : [ "Vec Permute"  , "vvx"  , "001111x", "100", "1010111", "Zve32x", "0", 1420, "xxxxx", "xxxxx" ],
   "VSLIDEDOWN.VI"  : [ "Vec Permute"  , "vvi"  , "001111x", "011", "1010111", "Zve32x", "0", 1421, "xxxxx", "xxxxx" ],
   "VSLIDE1UP.VX"   : [ "Vec Permute"  , "vvx"  , "001110x", "110", "1010111", "Zve32x", "0", 1422, "xxxxx", "xxxxx" ],
   "VSLIDE1DOWN.VX" : [ "Vec Permute"  , "vvx"  , "001111x", "110", "1010111", "Zve32x", "0", 1423, "xxxxx", "xxxxx" ],
   #--- Permutation - gather ---
   "VRGATHER.VV"    : [ "Vec Permute"  , "vvv"  , "001100x", "000", "1010111", "Zve32x", "0", 1424, "xxxxx", "xxxxx" ],
   "VRGATHEREI16.VV": [ "Vec Permute"  , "vvv"  , "001110x", "000", "1010111", "Zve32x", "0", 1425, "xxxxx", "xxxxx" ],
   "VRGATHER.VX"    : [ "Vec Permute"  , "vvx"  , "001100x", "100", "1010111", "Zve32x", "0", 1426, "xxxxx", "xxxxx" ],
   "VRGATHER.VI"    : [ "Vec Permute"  , "vvi"  , "001100x", "011", "1010111", "Zve32x", "0", 1427, "xxxxx", "xxxxx" ],
   #--- Permutation - compress ---
   "VCOMPRESS.VM"   : [ "Vec Permute"  , "vmm"  , "0101111", "010", "1010111", "Zve32x", "0", 1428, "xxxxx", "xxxxx" ],
   #--- Permutation - whole register move ---
   "VMV1R.V"        : [ "Vec Permute"  , "vwr"  , "1001111", "011", "1010111", "Zve32x", "0", 1429, "xxxxx", "00000" ],
   "VMV2R.V"        : [ "Vec Permute"  , "vwr"  , "1001111", "011", "1010111", "Zve32x", "0", 1430, "xxxxx", "00001" ],
   "VMV4R.V"        : [ "Vec Permute"  , "vwr"  , "1001111", "011", "1010111", "Zve32x", "0", 1431, "xxxxx", "00011" ],
   "VMV8R.V"        : [ "Vec Permute"  , "vwr"  , "1001111", "011", "1010111", "Zve32x", "0", 1432, "xxxxx", "00111" ]
   #--- Excluded - vector floating-point (not in Zve32x) ---
   #vfadd.vv/vx, vfsub.vv/vx, vfrsub.vf   # Vector floating-point add/subtract — requires Zve32f/Zve64f, not in Coral NPU's ISA string
   #vfmul.vv/vx, vfdiv.vv/vx, vfrdiv.vf   # Vector floating-point multiply/divide — excluded
   #vfmacc/vfnmacc/vfmsac/vfnmsac/vfmadd/vfnmadd/vfmsub/vfnmsub   # Vector floating-point fused multiply-add family — excluded
   #vfsqrt.v, vfrsqrt7.v, vfrec7.v   # Vector floating-point square-root / reciprocal estimate — excluded
   #vfmin.vv/vx, vfmax.vv/vx   # Vector floating-point min/max — excluded
   #vfsgnj.vv/vx, vfsgnjn.vv/vx, vfsgnjx.vv/vx   # Vector floating-point sign-injection — excluded
   #vmfeq/vmfne/vmflt/vmfle/vmfgt/vmfge   # Vector floating-point compare family — excluded
   #vfclass.v   # Vector floating-point classify — excluded
   #vfmerge.vfm, vfmv.v.f   # Vector floating-point merge/move — excluded
   #vfcvt.*, vfwcvt.*, vfncvt.*   # Vector floating-point/integer conversions (single-width, widening, narrowing) — excluded
   #vfredosum.vs, vfredusum.vs, vfredmax.vs, vfredmin.vs, vfwredosum.vs, vfwredusum.vs   # Vector floating-point reductions — excluded
   #vfmv.f.s, vfmv.s.f, vfslide1up.vf, vfslide1down.vf   # Floating-point scalar move / slide-by-1 — excluded
   #--- Excluded - EEW=64 variants (not in Zve32x) ---
   #vle64.v, vse64.v, vlse64.v, vsse64.v, vluxei64.v/vloxei64.v/vsuxei64.v/vsoxei64.v, vle64ff.v   # 64-bit element-width load/store variants — Zve32x max EEW is 32
   }



#privileged register list
#priv_reg = [ "ustatus","uie","utvec","uscratch","uepc","ucause","utval","uip","fflags","frm","fcsr","cycle","time","instret","hpmcounter3","cycleh","timeh","instreth","hpmcounter3h","sstatus","sedeleg","sideleg","sie","stvec","scounteren","sscratch","sepc","scause","sip","satp","mvendorid","marchid","mimpid","mhartid","mstatus","misa","medeleg","mideleg","mie","mtvec","mcounteren","mscratch","mepc","mcause","mip","pmpcfg0","pmpcfg1","pmpcfg2","pmpcfg3","pmpaddr0","mcycle","minstret","mhpmcounter3","mcycleh","minstreth","mhpmcounter3h","mhpmevent3","tselect","tdata1","tdata2","tdata3","dcsr","dpc","dpc"] 
#list that doesnt cause exceptions:
priv_reg = [ "sstatus","sie","stvec","scounteren","sscratch","sepc","scause"\
            ,"sip","satp","mstatus","misa","medeleg","mideleg","mie","mtvec"\
            ,"mcounteren","mscratch","mepc","mcause","mip","mcycle","minstret"\
            ,"mhpmcounter3","tselect","tdata1","tdata2","tdata3" ]

#vector CSRs. vl/vtype/vlenb are read-only, so CSRRW/CSRRS/CSRRC to them will
#trap - keep them out of priv_reg unless you want that as a fuzz target.
vec_csr = [ "vstart", "vxsat", "vxrm", "vcsr" ]         # writable, 0x008-0x00F
vec_csr_ro = [ "vl", "vtype", "vlenb" ]                 # 0xC20-0xC22
#uncomment to let the existing CSR Access insts fuzz the vector CSRs:
#priv_reg = priv_reg + vec_csr
#privileged registers not recognized by the toolchain: mtval, mcountinhibit, dscratch0, dscratch1, stval



#nop instrn
nop_inst_bin_32 = "{0:032b}".format(int("00000013",16))


inst_compile_issue = ['BEQ', 'BNE', 'BLT', 'BGE', 'BLTU', 'BGEU']
inst_sim_issue_0 = ['JAL', 'JALR'] # processor is jumping around when simulated
#inst_sim_issue_1 = ['LB', 'LH', 'LW', 'LBU', 'LHU', 'SB', 'SH', 'SW'] #exceptions
inst_sim_issue_1 = ['LH', 'LW', 'LHU', 'SH', 'SW', 'LWU', 'LD', 'SD', 'SB'] #exceptions
inst_sim_issue_2 = ['CSRRW', 'CSRRS', 'CSRRC', 'CSRRWI', 'CSRRSI', 'CSRRCI']
                                    #exceptions when simulated
inst_sim_issue_4 = ['FENCE.I', 'ECALL', 'EBREAK'] # couldnt include in prev itrn
amo_types = ['SWAP', 'ADD', 'XOR', 'AND', 'OR', 'MIN', 'MAX', 'MINU', 'MAXU']
amo_inst = ['LR', 'SC'] + ['AMO'+x for x in amo_types]
inst_sim_issue_3 = [x+'.W' for x in amo_inst] + [x+'.D' for x in amo_inst]
                                    #simulation getting stuck
inst_single_line = inst_compile_issue + inst_sim_issue_0 + inst_sim_issue_1   #instructions which are generated when create_prog_sing_inst=1
#inst_compile_issue = []
                                        #inst gets compiled as other multi inst


                                        
# select which extensions to include:
# inst_isa = { "rv32i": [rv32i,1], "rv64i": [rv64i,1]
#             ,"rv32m": [rv32m,1], "rv64m": [rv64m,1]
#             ,"rv32a": [rv32a,1], "rv64a": [rv64a,1]
#         }
inst_isa = { "rv32i": rv32i, "rv64i": rv64i
            ,"rv32m": rv32m, "rv64m": rv64m
            ,"rv32a": rv32a, "rv64a": rv64a
            ,"rvv"  : rvv
        }

#create the dict of instrns: 
#***make sure that rv64i overwrites rv32i fr instsns like SLLI***
# inst_list_all = {}
# inst_list_all_w_ext = {}
# inst_list_full = {}
# inst_list = {}
# for ext,ext_data in inst_isa.items():
#     if ext_data[1] == 0:  #skip this extension
#         continue
#     ext_dict = ext_data[0]
#     for inst, inst_data in ext_dict.items():
#         inst_list_all[inst] = inst_data
#         inst_list_all_w_ext[(inst, ext)] = inst_data

#inst_list_full = copy.deepcopy(inst_list_all)
#if rm_insts:
#    for inst in inst_compile_issue + inst_sim_issue_0 + inst_sim_issue_1\
#                                   + inst_sim_issue_2 + inst_sim_issue_3\
#                                   + inst_sim_issue_4: 
#        try:
#            del inst_list_full[inst]
#        except KeyError:
#            print(inst, " not there to delete")
