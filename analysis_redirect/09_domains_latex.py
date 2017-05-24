
with open('/home/nsarafij/project/OpenWPM/analysis_redirect/output/keysDomains_top10') as domains_file, open('/home/nsarafij/project/OpenWPM/analysis_redirect/output/domans_latex','a') as latex_file:
    k=0
    for line in domains_file:
        latex_file.write(' \hline \n')
        if k == 10: break
        line=line.rstrip()
        key_domains = line.split('*')
        key = key_domains[0]
        firstDomain = True
        domains_split = key_domains[1].split()
        no_domains = len(domains_split)/2
        for i in range(no_domains):
            if firstDomain:
                latex_file.write(key)
                firstDomain = False
            latex_file.write(' & ')
            latex_file.write(domains_split[i*2])
            latex_file.write(' & ')
            latex_file.write(domains_split[i*2 + 1])
            latex_file.write(' \\\\ \n')
        #if not firstDomain: latex_file.write(' \hline \n')
        
        k+=1
