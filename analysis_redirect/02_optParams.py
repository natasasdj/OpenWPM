import os

output_dir = '/home/nsarafij/project/OpenWPM/analysis_redirect/output/'
urls_file = open(os.path.join(output_dir, 'urls'))

params_file = open(os.path.join(output_dir, 'params'),'a')


#urls_file = ["1 0 http://www.google.com/ http://www.google.fr/?gfe_rd=cr&ei=7MKmWICgGJWDaMaGo9gD https://www.google.fr/?gfe_rd=cr&ei=7MKmWICgGJWDaMaGo9gD&gws_rd=ssl"]
firstLine = True
#k = 0
for line in urls_file:
    #if k==1: break
    line = line.rstrip()
    line_split = line.split(" ")
    #print line_split
    urls = line_split[3:]
    #print urls
    if firstLine: 
        firstLine = False
    else:
        pass
        #params_file.write("\n")
    #print line_split[0] + " " + line_split[1] + " "
    #print urls
    #params_file.write(line_split[0] + " " + line_split[1] + " " + line_split[2])
    for url in urls:
        #params_file.write(" ")
        params = url.split("?",1)
        print line_split[0] + " " + line_split[1] + " " + line_split[2]+ ' ' + url + "\n"  
        if len(params)==1: 
            params = "*"
        else:
            params = params[1]
        print params
        params_file.write(params)
    #k += 1

params_file.close()    
urls_file.close()


