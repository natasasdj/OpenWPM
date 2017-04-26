import os
import re
from urlparse import urlparse
import sys

main_dir = sys.argv[1]
output_dir = os.path.join(sys.argv[1],'OpenWPM/analysis_redirect/output/')
urls_file = open(os.path.join(output_dir, 'urls'))

queries_file = open(os.path.join(output_dir, 'queries'),'a')
no_redirects_file = open(os.path.join(output_dir, 'no_redirects'),'a')

firstLine = True
for line in urls_file:
    line = line.rstrip()
    line_split = line.split(" ")
    no_urls= len(line_split)/4
    if firstLine: 
        firstLine = False
    else:
        queries_file.write("\n")
        no_redirects_file.write("\n")
    for i in range(no_urls): 
        print i 
        if i != 0: queries_file.write(" ")     
        no_redirects_file.write(str(no_urls))
        print line_split[i*4+0] + " " + line_split[i*4+1] + " " + line_split[i*4+2]
        queries_file.write(line_split[i*4+0] + " " + line_split[i*4+1] + " " + line_split[i*4+2])
        url = line_split[i*4+3]
        print url
        queries_file.write(" ")
        queries_search = re.search("\?(.*?)(#|$)",url)
        if queries_search is None:
            domain = "*" 
            queries = "*"
        else:
            queries = queries_search.group(1)
            domain = urlparse(url).hostname.strip('www.')
        queries_file.write(domain + ' ' + queries)

queries_file.close()    
urls_file.close()
no_redirects_file.close()

