import os
import sqlite3
import pandas as pd
import plyvel
import hashlib
import bz2
import re
import sys

#main_dir = sys.argv[1]
#data_dir = sys.argv[2]
main_dir = '/home/nsarafij/project/'
data_dir = main_dir + 'data/output_4701/'
no_db = int(data_dir[data_dir.find("_")+1:-3])

#hash_dir = sys.argv[2]
hash_dir = main_dir + 'OpenWPM/file_hashing/db'
if not os.path.exists(hash_dir):
    os.makedirs(hash_dir)
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

def bzip2_decompress(fpath):
    decompr_content = bz2.decompress(open(fpath, 'rb').read())
    fh = open(fpath.rstrip('.bz2'), "wb")
    fh.write(decompr_content)
    fh.close()

def checkFile(siteID, linkID, respID, filename,filedir):
    print siteID, linkID, respID
    filepath = os.path.join(filedir,filename)
    zipped = False
    if not os.path.exists(filepath):
        if ("html" in filename) and os.path.exists(filepath+'.bz2'):
            #print "*** file is already zipped ***"
            zipped = True
        if not zipped: 
            #print "there is no file", filename
            return 
    if zipped:
       bzip2_decompress(filepath+'.bz2')
    if "html" in filename:
        hashDB = hashHtml
        fileDB = 'Htmls'
    else:
        hashDB = hashImage
        fileDB = 'Images'       
    filehash = file_hash(filepath)
    if hashDB.get(filehash) is None:
        # put hash into hashHtml or hashImage level db
        hashDB.put(filehash.encode('utf8'),filename.encode('utf8'))
        query = 'INSERT INTO {} (site_id, link_id, resp_id, count, file) VALUES({},{},{},{},{})'.format(fileDB,siteID,linkID,respID,1, '"'+filename+'"')
        #print query
        cur1.execute(query)
        if ("html" in filename): 
            if not zipped: bzip2(filepath)
            os.remove(filepath) 
    else:       
        # create symlink
        fname = hashDB.get(filehash.encode('utf8'))
        f = fname.rstrip(".html").split("-")
        fpath = os.path.join(main_dir, 'data', 'output_' + str((int(f[1])-1)/100) + '01','httpResp/site-' + f[1], fname)        
        os.remove(filepath) 
        if ("html" in filename): 
            os.symlink(fpath+'.bz2',filepath)
        else:
            os.symlink(fpath,filepath)        
        query = 'SELECT count FROM {} WHERE site_id = {} and link_id = {} and resp_id = {}'.format(fileDB,f[1],f[2],f[3])
        df = pd.read_sql_query(query,conn1)
        query = 'UPDATE {} SET count = {} WHERE site_id = {} and link_id = {} and resp_id = {}'.format(fileDB,df['count'][0] + 1,f[1],f[2],f[3])
        #print query
        cur1.execute(query)
    conn1.commit()    
       

def purge(directory, pattern):
    for f in os.listdir(directory):
        if re.search(pattern, f):
            #print "*************************** purge ****************************************", f
            os.remove(os.path.join(directory, f))

for i in range(no_db*100+3,no_db*100+no_sites+1):  #no_sites+1 
    print "site:", i 
    query = 'SELECT * FROM site_visits WHERE site_id = {0}'.format(i,)
    df = pd.read_sql_query(query,conn)
    file_dir = os.path.join(data_dir, 'httpResp','site-'+str(i))
    for index, row in df.iterrows():  
        if row['link_id']==0:
            if pd.isnull(row['resp_time_3']): 
                #print "**************** resp_time_3 is null **********************"
                purge(file_dir,"file-"+str(row['site_id'])+"-"+str(row['link_id'])+"-\d+") 
                os.rmdir(file_dir) 
                continue 
        else:
            if pd.isnull(row['resp_time_2']):
                #print "**************** resp_time_2 is null **********************", row['site_id'], row['link_id']
                purge(file_dir,"file-"+str(row['site_id'])+"-"+str(row['link_id'])+"-\d+") 
                continue
        query = 'SELECT * FROM http_responses WHERE site_id = {0} AND link_id = {1}'.format(row['site_id'],row['link_id'])
        df2 = pd.read_sql_query(query,conn)
        for index2, row2 in df2.iterrows():
            if pd.isnull(row2['file_name']): continue
            checkFile(row2['site_id'],row2['link_id'],row2['response_id'],row2['file_name'],file_dir)
        


'''
for key, value in hashHtml:
    print "dbHTML", key, value

for key, value in hashImage:
    print "dbHTML", key, value

query = 'SELECT * FROM Images'
df = pd.read_sql_query(query,conn1)
'''

hashHtml.close()
hashImage.close()
conn1.close()

conn.close()

