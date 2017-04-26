import os
import sets
import re
import sys

main_dir = sys.argv[1]
output_dir = os.path.join(sys.argv[1],'OpenWPM/analysis_redirect/output/')
params_file = open(os.path.join(output_dir, 'params'))
keysPersist_file = open(os.path.join(output_dir, 'keysPersist'),'a')
keys_file = open(os.path.join(output_dir, 'keys'),'a')


k = 0

#site_id = 0
for line in params_file:
    print line
    line_write = False
    linePersist_write = False
    #if k==3: break
    #line = line.rstrip("\n")
    #print line
    if line == '' or re.match('\s+',line): continue
    line_split = line.split(" & ")
    print line_split
    params = line_split
    #print line
    #print line_split[0]
    #print line_split[0].split(" ")  
    #if site_id != int(line_split[0].split(" ")[0]):
    #    site_id = int(line_split[0].split(" ")[0])
    #    print site_id   
    #print params
    keys_values_all = sets.Set()        
    for param in params:
        print param
        p = param.split(" ")
        key_write = False
        keyPersist_write = False   
        #print p
        if p[3] == "*": continue
        keys_values = p[4:]
        for key_value in keys_values:
            print key_value
            #print key_write, keyPersist_write            
            if key_write:  
                keys_file.write(' ')
                #print "key write space"                
            else:
                if line_write: 
                     keys_file.write(' & ') 
                else: 
                     line_write = True
                keys_file.write(p[3] + ' ')
                key_write = True
                 
            key = key_value.split("=")[0]
            keys_file.write(key)
            if key_value in keys_values_all:
                print keyPersist_write, key_value
                if keyPersist_write:  
                    keysPersist_file.write(' ')
                else:
                    if linePersist_write:
                        keysPersist_file.write(' ')
                    else:
                        linePersist_write = True
                    keyPersist_write = True                   
                print key 
                keysPersist_file.write(key)
                #print "key persist write True"               
            else:
                keys_values_all.add(key_value)             
    if line_write: keys_file.write("\n")
    if linePersist_write: keysPersist_file.write("\n")                     
    k += 1
    

params_file.close()
keysPersist_file.close()
keys_file.close()


