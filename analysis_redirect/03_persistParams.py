import os
import sets

output_dir = '/home/nsarafij/project/OpenWPM/analysis_redirect/output/'
params_file = open(os.path.join(output_dir, 'params'))
pp_file = open(os.path.join(output_dir, 'persistParams'),'a')
keys_file = open(os.path.join(output_dir, 'keys'),'a')

firstLine = True
k = 0
for line in params_file:
    if k==10: break
    line = line.rstrip()
    line_split = line.split(" ")
    print line_split
    params = line_split[3:]   
    if firstLine: 
        firstLine = False
    else:
        pp_file.write("\n")
        keys_file.write("\n")
    print line_split[0] + " " + line_split[1]
    print params
    pp_file.write(line_split[0] + " " + line_split[1] + " " + line_split[2])
    keys_values_all = sets.Set()
    for p in params:
        #print p
        if p == "*": continue
        keys_values = p.split("&")
        #print keys_values
        keys_file.write(line_split[0] + " " + line_split[1] + " " + line_split[2] + " ")
        for key_value in keys_values:
            key = key_value.split("=")[0]
            keys_file.write(" " + key)
            if key_value in keys_values_all:
                pp_file.write(" " + key_value)
            else:
                keys_values_all.add(key_value)
                    
            
    #k += 1
    

params_file.close()
pp_file.close()
keys_file.close()


