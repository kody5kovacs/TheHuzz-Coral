#!/bin/bash

curr_dir=$PWD

cd $1

rm -rf simv.vdb

./bazel-bin/tests/vcs_sim/rvv_core_mini_verification_axi_sim_simv \
    -cm line+cond+tgl+branch+fsm+assert \
    -cm_dir ./simv.vdb \
    +binary=$3 \
    -no_save \
    1> sim.log 2>&1

cd $curr_dir