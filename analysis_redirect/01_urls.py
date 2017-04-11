import sqlite3
import pandas as pd
import os


#data_dir = sys.argv[1]
main_dir = '/home/nsarafij/project/'
data_dir = os.path.join(main_dir,'data/output_001/')
#output_dir = sys.argv[2]
output_dir = os.path.join(main_dir,'OpenWPM/analysis_redirect/output/')
anal_dir = os.path.join(main_dir,'OpenWPM/analysis/results/')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)



db_file = os.path.join(data_dir,'crawl-data.sqlite')
conn = sqlite3.connect(db_file)

db2_file = os.path.join(anal_dir,'images.sqlite')
conn2 = sqlite3.connect(db2_file)


query = 'SELECT * FROM http_responses ORDER BY site_id ASC, link_id ASC, response_id ASC'
df = pd.read_sql_query(query,conn)

urls_file = open(os.path.join(output_dir, 'urls'),'a') 
prev_link = None
prev_location = None
prev_redirect = False
for ind, row in df.iterrows():        
    if 300 <= row['response_status'] < 400:
        if prev_link != (row['site_id'], row['link_id']) or row['url'] != prev_location: 
            s=""
            prev_redirect = True             
            #if row['site_id'] > 10: break
            
            #if prev_link is not None: 
                #urls_file.write('\n')
                #s += '\n' 
            #print "****",row['url'], row['location']
            #urls_file.write(str(row['site_id']) + ' ' + str(row['link_id']) + ' ' + row['url'] + ' ' + row['location'])
            s += str(row['site_id']) + ' ' + str(row['link_id']) + ' ' + str(row['response_id']) + ' ' + row['url'] + ' ' + row['location']             
            prev_link = (row['site_id'], row['link_id'])            
        else:
            #urls_file.write(' ' + row['location']) 
            s += ' ' + row['location']
            #print row['location']
            #if row['url'] != prev_location: print "error"
        prev_location = row['location']
    else:
        #print "else:"
        if prev_redirect == True and not pd.isnull(row['file_name']) and (not 'html' in row['file_name']):
            prev_redirect = False
            if row['url'] == prev_location:
                query = 'SELECT pixels FROM Images WHERE site_id = {} AND link_id = {} AND resp_id = {}'.format(row['site_id'], row['link_id'], row['response_id']) 
                df2 = pd.read_sql_query(query,conn2)
                #print df2
                if (not df2.shape[0] == 0) and df2['pixels'][0]==1: 
                    print row['site_id'], row['link_id'], row['response_id']
                    urls_file.write(s+'\n')
         
                 
 

urls_file.close()
conn2.close()
conn.close()
