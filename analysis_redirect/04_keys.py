import os
import sets

output_dir = '/home/nsarafij/project/OpenWPM/analysis_redirect/output/'
params_file = open(os.path.join(output_dir, 'params'))
keysPersist_file = open(os.path.join(output_dir, 'keysPersist'),'a')
keys_file = open(os.path.join(output_dir, 'keys'),'a')

firstLine = True
#k = 0
line_write = False
linePersist_write = False
site_id = 0
for line in params_file:
    line_write = False
    linePersist_write = False
    #if k==2: break
    line = line.rstrip("\n")
    #print line
    if line == '': continue
    line_split = line.split(" & ")
    params = line_split[1:]
    #print line
    #print line_split[0]
    #print line_split[0].split(" ")  
    if site_id != int(line_split[0].split(" ")[0]):
        site_id = int(line_split[0].split(" ")[0])
        print site_id   
    #print params
    keys_values_all = sets.Set()
    key_write = False
    keyPersist_write = False
    key_write = False
    keyPersist_write = False        
    for p in params:
        #print p
        if p == "": continue
        keys_values = p.split(" ")
        for key_value in keys_values:
            #print key_write, keyPersist_write
            if key_write:  
                keys_file.write(' ')
                #print "key write space" 
                line_write = True
            if keyPersist_write:  
                keysPersist_file.write(' ')
                #print "key persist write space"
                linePersist_write = True 
            key = key_value.split("=")[0]
            keys_file.write(key)
            key_write = True
            if key_value in keys_values_all:
                keysPersist_file.write(key)
                #print "key persist write True"
                keyPersist_write = True
            else:
                keys_values_all.add(key_value)
                keyPersist_write = False
        
    if line_write: keys_file.write("\n")
    if linePersist_write: keysPersist_file.write("\n")                     
    #k += 1
    

params_file.close()
keysPersist_file.close()
keys_file.close()


