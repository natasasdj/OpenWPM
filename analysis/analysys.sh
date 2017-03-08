for i in {0..0}
do
    echo $i
    start=${i}01
    echo $start
    echo "/home/nsarafij/project/data/output_$start/"
    python images_sqlite.py "/home/nsarafij/project/data/output_$start/"   
done
