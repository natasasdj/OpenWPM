#!/bin/bash

for i in {1..1}
do
    echo $i
    start=${i}01
    echo $start
    data_dir=/data/indes/user/ifouad/output/output_$start 
    echo $data_dir
    res_dir=/home/nsarafij/OpenWPM/analysis_parallel/results
    python 01b_responseDomains_sqlite.py $data_dir $res_dir
done

