import os
import sqlite3
import pandas as pd
import plyvel
import hashlib
import bz2
import re


#data_dir = sys.argv[1]
data_dir = '/home/nsarafij/project/data/output_4701/'
no_db = int(data_dir[data_dir.find("_")+1:-3])

hash_dir = '/home/nsarafij/project/OpenWPM/file_hashing/'
db_path = os.path.join(hash_dir, 'hashImage.ldb')
hashImage = plyvel.DB(db_path, create_if_missing = True)
db_path = os.path.join(hash_dir, 'hashHtml.ldb')
hashHtml = plyvel.DB(db_path, create_if_missing = True)


db = os.path.join(hash_dir,'fileHashing.sqlite')
conn1 = sqlite3.connect(db)
cur1 = conn1.cursor()

cur1.execute('CREATE TABLE IF NOT EXISTS Images \
		(site_id INTEGER NOT NULL, link_id INTEGER NOT NULL, resp_id INTEGER NOT NULL, \
		 count INTEGER, file TEXT)')

cur1.execute('CREATE TABLE IF NOT EXISTS Htmls \
		(site_id INTEGER NOT NULL, link_id INTEGER NOT NULL, resp_id INTEGER NOT NULL, \
		 count INTEGER, file TEXT)')



db_file = data_dir + 'crawl-data.sqlite'
conn = sqlite3.connect(db_file)

no_sites = 100

def file_hash(fname):
    with open(fname, "rb") as fhand:
        hasher = hashlib.md5()
        buf = fhand.read()
        hasher.update(buf)
        return hasher.hexdigest()

def bzip2(fpath):
    compr_content = bz2.compress(open(fpath, 'rb').read())
    fh = open(fpath+'.bz2', "wb")
    fh.write(compr_content)
    fh.close()

def checkFile(siteID, linkID, respID, filename,filedir):
    print siteID, linkID, respID
    fpath = os.path.join(filedir,filename)
    if not os.path.exists(fpath):
        print "there is no file", filename
        if ("html" in filename) and os.path.exists(fpath+'.bz2'):
            print "*** file is already zipped ***"
        return
    
    if "html" in filename:
        hashDB = hashHtml
        fileDB = 'Htmls'
    else:
        hashDB = hashImage
        fileDB = 'Images'       
    fhash = file_hash(fpath)
    if hashDB.get(fhash) is None:
        hashDB.put(fhash.encode('utf8'),filename.encode('utf8'))
        query = 'INSERT INTO {} (site_id, link_id, resp_id, count, file) VALUES({},{},{},{},{})'.format(fileDB,siteID,linkID,respID,1, '"'+filename+'"')
        print query,cur1
        cur1.execute(query)
        if "html" in filename: 
            bzip2(fpath)
            os.remove(fpath) 
    return

def purge(directory, pattern):
    for f in os.listdir(directory):
        if re.search(pattern, f):
            print "*************************** purge ****************************************", f
            #os.remove(os.path.join(directory, f))


for i in range(no_db*100+1,no_db*100+2):  #no_sites+1  
    query = 'SELECT * FROM site_visits WHERE site_id = {0}'.format(i,)
    df = pd.read_sql_query(query,conn)
    file_dir = os.path.join(data_dir, 'httpResp','site-'+str(i))
    for index, row in df.iterrows():
        if row['link_id']==0:
            if pd.isnull(row['resp_time_3']): 
                purge(file_dir,"file-"+str(row['site_id'])+"-"+str(row['link_id'])+"-\d+")  
                continue 
        else:
            if pd.isnull(row['resp_time_2']): continue
        query = 'SELECT * FROM http_responses WHERE site_id = {0} AND link_id = {1}'.format(row['site_id'],row['link_id'])
        df = pd.read_sql_query(query,conn)
        for index, row in df.iterrows():
            if pd.isnull(row['file_name']): continue
            checkFile(row['site_id'],row['link_id'],row['response_id'],row['file_name'],file_dir)
        conn1.commit()



for key, value in hashHtml:
    print "dbHTML", key, value

for key, value in hashImage:
    print "dbHTML", key, value

query = 'SELECT * FROM Images'
df = pd.read_sql_query(query,conn1)

for f in os.listdir(file_dir): 
    if re.search(pattern, f):
        print f 
        os.remove(os.path.join(file_dir, f))

hashHtml.close()
hashImage.close()
conn1.close()
conn.close()

'''
for i in range(no_db*100+1,no_db*100+2):  #no_sites+1  
    query = 'SELECT * FROM site_visits WHERE site_id = {0}'.format(i,)
    df = pd.read_sql_query(query,conn)
    for index, row in df.iterrows():
        if row['link_id']==0:
            if pd.isnull(row['resp_time_3']): continue 
        else:
            if pd.isnull(row['resp_time_2']): continue
        query = 'SELECT * FROM http_responses WHERE site_id = {0} AND link_id = {1}'.format(row['site_id'],row['link_id'])
        df = pd.read_sql_query(query,conn)
        for index, row in df.iterrows():
            if pd.isnull(row['file_name']): continue
            checkFile(row['site_id'],row['link_id'],row['response_id'],row['file_name'])
        conn1.commit()
'''


        '''
        if pd.isnull(df.loc[0,'resp_time_3']): continue

        #print i, j
        if j!=0:  
            query = 'SELECT * FROM site_visits WHERE site_id = {0} AND link_id = {1}'.format(i, j)
            df = pd.read_sql_query(query,conn)
        if len(df.index)==0: break
        if pd.isnull(df.loc[0,'resp_time_2']):
            # j += 1 
            continue
        succ += 1              
          

        #f4 = open(filename,'a')
        
            if 'html' in row['file_name']:  continue
        '''
