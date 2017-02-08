f=laptop/top$1.txt
echo $f
while true; do
   top -n 1 -b | head >> $f
   sleep 1
done


