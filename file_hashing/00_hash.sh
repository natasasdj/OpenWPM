#!/bin/bash
# no of browsers, no of start site, no of sites, no of links

#!/bin/bash
# no of browsers, no of start site, no of sites, no of links

main_dir="/root/"
for i in {11..14}
do
    echo $i
    data_dir=${main_dir}data/output_${i}01/
    echo $data_dir
    python ${main_dir}OpenWPM/file_hashing/01_fileHashing.py $main_dir $data_dir
done
