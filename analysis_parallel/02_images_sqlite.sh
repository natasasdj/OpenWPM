#!/bin/bash
# 

for ((i = $1; i <= $2; i++));
do
    # echo $i
    start=${i}01
    #db=results/crawl-data-${i}.sqlite
    db=/workspaces/nef/data/indes/user/ifouad/output/output_$start/crawl-data.sqlite
    echo "copying crawl-data.sqlite database"
    #cp /workspaces/nef/data/indes/user/ifouad/output/output_$start/crawl-data.sqlite $db
    #echo /workspaces/nef/data/indes/user/ifouad/output/output_$start/crawl-data.sqlite 
    #echo $db
    echo $start
    echo images_${3}.sqlite
    echo "start running 02_images_sqlite.py"
    python /home/nsarafij/project/OpenWPM/analysis_parallel/02_images_sqlite.py /workspaces/nef/data/indes/user/ifouad/output/output_$start results images_${3}.sqlite $db
done


