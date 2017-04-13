import os
import re

output_dir = '/home/nsarafij/project/OpenWPM/analysis_redirect/output/'
urls_file = open(os.path.join(output_dir, 'urls'))

queries_file = open(os.path.join(output_dir, 'queries'),'a')


firstLine = True
for line in urls_file:
    line = line.rstrip()
    line_split = line.split(" ")
    urls = line_split[3:]
    if firstLine: 
        firstLine = False
    else:
        queries_file.write("\n")
    print line_split[0] + " " + line_split[1] + " " + line_split[2]
    queries_file.write(line_split[0] + " " + line_split[1] + " " + line_split[2])
    for url in urls:
        queries_file.write(" ")
        queries_search = re.search("\?(.*?)(#|$)",url)
        if queries_search is None: 
            queries = "*"
        else:
            queries = queries_search.group(1)
        queries_file.write(queries)

queries_file.close()    
urls_file.close()


