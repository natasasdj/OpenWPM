#!/bin/bash
# no of browsers, no of start site, no of sites, no of links

#!/bin/bash
# no of browsers, no of start site, no of sites, no of links

main_dir="/home/nsarafij/project/"
for i in {1..1}
do
    echo $i
    data_dir=${main_dir}data/output_${i}01/
    #echo $data_dir
    hash_dir=${main_dir}OpenWPM/file_hashing/
    #echo ${hash_dir}fileHashing.py
    #echo ${hash_dir}db
    python ${hash_dir}fileHashing.py $data_dir ${hash_dir}db
done
