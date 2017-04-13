import os
import sets
import urlparse
import re

output_dir = '/home/nsarafij/project/OpenWPM/analysis_redirect/output/'
queries_file = open(os.path.join(output_dir, 'queries'))
params_file = open(os.path.join(output_dir, 'params'),'a')
paramsNested_file = open(os.path.join(output_dir, 'paramsNested'),'a')

firstLine = True
#k = 0
for line in queries_file:
    #if k==2: break
    line = line.rstrip()
    line_split = line.split(" ")
    #print line_split
    queries = line_split[3:]   
    if firstLine: 
        firstLine = False
    else:
        paramsNested_file.write("\n")
        params_file.write("\n")
    paramsNested_file.write(line_split[0] + " " + line_split[1] + " " + line_split[2]) 
    params_file.write(line_split[0] + " " + line_split[1] + " " + line_split[2])
    print line_split[0] 
    for query in queries:
        paramsNested_file.write(' & ')
        params_file.write(' & ')
        if query == "*": continue
        if re.match('https?((://)|(%3A%2F%2F))',query): 
           query = '#=' + query 
        params_list = urlparse.parse_qsl(query)
        key_append = ""
        firstParam = True
        for key,value in params_list:
            if firstParam: 
                firstParam = False
            else:
                paramsNested_file.write(" ")
                params_file.write(" ")
            if re.match('https?((://)|(%3A%2F%2F))',value):
                #q = urlparse.parse_qsl(q)
                key_append = key_append + key + '#'
                params_file.write(key + '=' + value.replace(" ","%20"))
                #print key_append
                nested_params_list = urlparse.parse_qsl(urlparse.urlparse(value).query)
                for nested_key,nested_value in nested_params_list:
                    http_part_match = re.match('(https?((://)|(%3A%2F%2F))(.*?)\?)+(.*)(#|$)',nested_key)
                    if http_part_match:
                        nested_key=http_part_match.group(6)
                       #print nested_key
                    paramsNested_file.write(' ' + key_append + nested_key + "=" + nested_value.replace(" ","%20"))
                    params_file.write(' ' + nested_key + "=" + nested_value.replace(" ","%20"))
            else:
               paramsNested_file.write(key_append + key + '=' + value.replace(" ","%20")) 
               params_file.write(key + '=' + value.replace(" ","%20"))
    #k += 1
    

params_file.close()
paramsNested_file.close()
queries_file.close()

