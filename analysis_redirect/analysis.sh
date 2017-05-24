#!/bin/bash
# no of browsers, no of start site, no of sites, no of links

#!/bin/bash
# no of browsers, no of start site, no of sites, no of links

main_dir="/home/nsarafij/project/"
echo $main_dir
for i in {51..69}
do
    echo $i
    data_dir=${main_dir}data/output_${i}01/
    echo $data_dir
    redir_dir=${main_dir}OpenWPM/analysis_redirect/
    echo ${redir_dir}01_urls.py
    python ${redir_dir}01_urls.py $main_dir $data_dir
done
