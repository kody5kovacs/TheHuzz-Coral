# >>> cy-dir-helper initialize >>>
CY_DIR=/data/kody5kovacs/HWFuzzing/TheHuzz/benchmarks/chipyard_1130
# <<< cy-dir-helper initialize <<<

# >>> init-submodules initialize >>>
__DIR=/data/kody5kovacs/HWFuzzing/TheHuzz/benchmarks/chipyard_1130
PATH=$__DIR/software/firemarshal:$PATH
# <<< init-submodules initialize <<<

export CHIPYARD_TOOLCHAIN_SOURCED=1
export RISCV=/data/kody5kovacs/HWFuzzing/TheHuzz/benchmarks/chipyard_1130/riscv-tools-install
export PATH=${RISCV}/bin:${PATH}
export LD_LIBRARY_PATH=${RISCV}/lib${LD_LIBRARY_PATH:+":${LD_LIBRARY_PATH}"}
