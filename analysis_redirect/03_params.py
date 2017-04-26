import os
import sets
import urlparse
import re
import sys

main_dir = sys.argv[1]
output_dir = os.path.join(sys.argv[1],'OpenWPM/analysis_redirect/output/')
queries_file = open(os.path.join(output_dir, 'queries'))
params_file = open(os.path.join(output_dir, 'params'),'a')
paramsNested_file = open(os.path.join(output_dir, 'paramsNested'),'a')

firstLine = True
#k = 0
for line in queries_file:
    #if k==3: break
    line = line.rstrip()
    line_split = line.split(" ")
    no_urls= len(line_split)/5  
    if firstLine: 
        firstLine = False
    else:
        paramsNested_file.write("\n")
        params_file.write("\n")   
    print line_split[0] 
    for i in range(no_urls):
        if i <> 0:
            paramsNested_file.write(' & ')
            params_file.write(' & ') 
        print i
        paramsNested_file.write(line_split[i*5+0] + " " + line_split[i*5+1] + " " + line_split[i*5+2] + " " + line_split[i*5+3] ) 
        params_file.write(line_split[i*5+0] + " " + line_split[i*5+1] + " " + line_split[i*5+2] + " " + line_split[i*5+3])
        query = line_split[i*5+4]       
        if query == "*": continue
        if re.match('https?((://)|(%3A%2F%2F))',query): 
           query = '#=' + query 
        params_list = urlparse.parse_qsl(query)
        key_append = ""
        for key,value in params_list:
            paramsNested_file.write(" ")
            params_file.write(" ")
            query_match=re.match('(https?((://)|(%3A%2F%2F))(.*?)(\?|(%3F))+)',value)
            if query_match:
                value = query_match.group()
                #q = urlparse.parse_qsl(q)
                value.replace(" ","%20").replace("\n","%0A").replace("\xc2\xa0","%C2%A0")
                key_append = key_append + key + '#'
                params_file.write(key + '=' + value)
                nested_params_list = urlparse.parse_qsl(urlparse.urlparse(value).query)
                for nested_key,nested_value in nested_params_list:
                    http_part_match = re.match('(https?((://)|(%3A%2F%2F))(.*?)\?)+(.*)(#|$)',nested_key)
                    if http_part_match:
                        nested_key=http_part_match.group(6)
                       #print nested_key
                    nested_value.replace(" ","%20").replace("\n","%0A").replace("\xc2\xa0","%C2%A0")
                    paramsNested_file.write(' ' + key_append + nested_key + "=" + nested_value )
                    params_file.write(' ' + nested_key + "=" + nested_value)
            else:
                value.replace(" ","%20").replace("\n","%0A").replace("\xc2\xa0","%C2%A0")
                paramsNested_file.write(key_append + key + '=' + value) 
                params_file.write(key + '=' + value)
    #k += 1
    

params_file.close()
paramsNested_file.close()
queries_file.close()

