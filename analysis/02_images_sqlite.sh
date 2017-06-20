#!/bin/bash

source /home/nsarafij/env/bin/activate
for i in {2..99}
do
    #echo $i
    start=${i}01
    echo $start
    python 02_images_sqlite.py /data/indes/user/ifouad/output/output_$start/ results   
done
