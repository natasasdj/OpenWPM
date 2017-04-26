import os
import sets
import operator
import sys

main_dir = sys.argv[1]
output_dir = os.path.join(main_dir,'OpenWPM/analysis_redirect/output/')

def domains_line(key,line):
    domains = sets.Set()
    for split1 in line.split(' & '):
        splits2 = split1.split(' ')
        if key in splits2[1:]: domains.add(splits2[0])
    return domains

def domains_file(key):
    domains = sets.Set()
    keys_fhand = open(os.path.join(output_dir,'keys'))
    for line in keys_fhand:
        for domain in domains_line(key,line):
            domains.add(domain)
    keys_fhand.close()
    return domains

with open(os.path.join(output_dir,'keysPersist')) as fhand:
	keys_dict = dict()
	for line in fhand:
	    line_keys = dict()
	    keys = line.rstrip().split()
	    #print keys
	    for key in keys:
		if key not in keys_dict:
		    keys_dict[key] = 1
		    line_keys[key] = 1
		elif key not in line_keys:
		        keys_dict[key] = keys_dict[key] + 1
		        line_keys[key] = 1
                

keysDict_sorted = sorted(keys_dict.items(), key=operator.itemgetter(1), reverse = True)
keys,values = zip(*keysDict_sorted)


open(os.path.join(output_dir,'domains'),'a') as domains_fhand:
	for key in keys:
	    domains_fhand.write(key + ' *')
	    domains = domains_file(key)
	    for domain in domains:
		domains_fhand.write(' ' + domain)
	    domains_fhand.write('\n') 


    

                  



         



