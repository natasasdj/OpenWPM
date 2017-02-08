f=laptop/iotop$1.txt
echo $f
while true; do
   iotop -n 1 -b | head >> $f
   sleep 1
done


