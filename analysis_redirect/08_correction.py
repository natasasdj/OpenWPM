with open('/home/nsarafij/project/OpenWPM/analysis_redirect/output/no_redirects','a') as f:
    with open('/home/nsarafij/project/OpenWPM/analysis_redirect/output/no_redirects_1') as f1:
        firstLine = True
        for line in f1:
            #print line
            line = line.rstrip()
            #print line
            no=line.split()[0][0]
            if no=='1':
                no = line.split()[0][0:2]
                print no
            #print no
            if firstLine:
                firstLine = False
            else:
                f.write('\n')
            f.write(no)


