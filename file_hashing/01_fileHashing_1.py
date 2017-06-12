import os
import sqlite3
import pandas as pd
import plyvel
import hashlib
import bz2
import re
import sys
from timeit import default_timer as timer

main_dir = sys.argv[1]
data_dir = sys.argv[2]
#main_dir = '/home/nsarafij/project/'
#data_dir = os.path.join(main_dir,'data/output_4801/')
no_db = int(data_dir[data_dir.find("_")+1:-3])
print no_db
#hash_dir = sys.argv[2]
hash_dir = os.path.join(main_dir, 'OpenWPM/file_hashing/db')
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
		 count INTEGER, file TEXT, PRIMARY KEY (site_id, link_id, resp_id))')
cur1.execute('CREATE TABLE IF NOT EXISTS Htmls \
		(site_id INTEGER NOT NULL, link_id INTEGER NOT NULL, resp_id INTEGER NOT NULL, \
		 count INTEGER, file TEXT, PRIMARY KEY (site_id, link_id, resp_id))')


db_file = os.path.join(data_dir, 'crawl-data.sqlite')
print db_file
conn = sqlite3.connect(db_file)

no_sites = 1

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
    #print siteID, linkID, respID
    t1 = timer()
    filepath = os.path.join(filedir,filename)
    zipped = False
    if os.path.islink(filepath): return
    if not os.path.exists(filepath):
        if ("html" in filename) and os.path.exists(filepath+'.bz2'):
            #print "*** file is already zipped ***"
            zipped = True
        if not zipped: 
            #print "there is no file", filename
            return
    
    if os.path.islink(filepath): return 
    if zipped:
       bzip2_decompress(filepath+'.bz2')
    if "html" in filename:
        hashDB = hashHtml
        fileDB = 'Htmls'
    else:
        hashDB = hashImage
        fileDB = 'Images' 
    t2 = timer()     
    filehash = file_hash(filepath)
    fname = hashDB.get(filehash.encode('utf8'))
    t3 = timer()
    t4 = None; t5 = None;
    if fname is None:
        # put hash into hashHtml or hashImage level db
        hashDB.put(filehash.encode('utf8'),filename.encode('utf8'))
        query = 'INSERT INTO {} (site_id, link_id, resp_id, count, file) VALUES({},{},{},{},{})'.format(fileDB,siteID,linkID,respID,1, '"'+filename+'"')
        #print query
        cur1.execute(query)
        if ("html" in filename): 
            if not zipped: bzip2(filepath)
            os.remove(filepath)
        t4 = timer()
    elif fname == filename:
         return 
    else:       
        # create symlink        
        f = fname.rstrip(".html").split("-")
        fpath = os.path.join(main_dir, 'data', 'output_' + str((int(f[1])-1)/100) + '01','httpResp/site-' + f[1], fname)        
        os.remove(filepath)        
        if ("html" in filename): 
            os.symlink(fpath+'.bz2',filepath)
        else:
            os.symlink(fpath,filepath)  
        #print f
        t5a = timer()      
        #query = 'SELECT count FROM {} WHERE site_id = {} and link_id = {} and resp_id = {}'.format(fileDB,f[1],f[2],f[3])
        cur1.execute('SELECT count FROM {} WHERE site_id = {} and link_id = {} and resp_id = {}'.format(fileDB,f[1],f[2],f[3]))
        #df = pd.read_sql_query(query,conn1)
        #print df
        t5b = timer()
        data=cur1.fetchone()
        #if df['count'].shape[0] == 0:
        if data is None:
            query = 'INSERT INTO {} (site_id, link_id, resp_id, count, file) VALUES({},{},{},{},{})'.format(fileDB,siteID,linkID,respID,1, '"'+filename+'"')
        else:
            #query = 'UPDATE {} SET count = {} WHERE site_id = {} and link_id = {} and resp_id = {}'.format(fileDB,df['count'][0] + 1,f[1],f[2],f[3])
            query = 'UPDATE {} SET count = {} WHERE site_id = {} and link_id = {} and resp_id = {}'.format(fileDB,data[0] + 1,f[1],f[2],f[3])
        #print query
        cur1.execute(query)
        t5 = timer()
       
    with open(os.path.join(hash_dir,'test4'),'a') as f4:
        f4.write(str(siteID) + ' ' + str(linkID) + ' ' + str(respID) + ' ' + str(t2-t1) + ' ' + str(t3-t2) + ' ')
        if t4 is None: 
            f4.write('None' + ' ')
        else:
            f4.write(str(t4-t3)  + ' ')
        if t5 is None: 
            f4.write('None' + '\n')
        else:
            f4.write(str(t5a-t3) +' '+ str(t5b-t5a) +' '+str(t5-t3) + '\n')  
          
       

def purge(directory, pattern):
    for f in os.listdir(directory):
        if re.search(pattern, f):
            #print "*************************** purge ****************************************", f
            os.remove(os.path.join(directory, f))

f1 = open(os.path.join(hash_dir,'test1'),'a')
f2 = open(os.path.join(hash_dir,'test2'),'a')
f3 = open(os.path.join(hash_dir,'test3'),'a')

ts = timer()

query = 'SELECT * FROM site_visits' 
df1 = pd.read_sql_query(query,conn)
query = 'SELECT * FROM http_responses' 
df2 = pd.read_sql_query(query,conn)


for i in range(no_db*100+1,no_db*100+no_sites+1):  #no_sites+1 
    print "site:", i
    t1 = timer()
    #query = 'SELECT * FROM site_visits WHERE site_id = {0}'.format(i,)
    #df3 = pd.read_sql_query(query,conn)
    file_dir = os.path.join(data_dir, 'httpResp','site-'+str(i))
    print file_dir
    if not os.path.exists(file_dir): continue 
    df3= df1.loc[df1['site_id']==i]
    print df3
    t2=timer()
    f1.write(str(i)+' ' + str(t2-t1) + ' ')  
    for index, row in df3.iterrows(): 
        t3 = timer()
        f2.write(str(row['site_id'])+" "+str(row['link_id'])+ ' ')             
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
        t4 = timer() 
        f2.write(str(t4-t3) + ' ')
        t4b = timer()
        #query = 'SELECT * FROM http_responses WHERE site_id = {0} AND link_id = {1}'.format(row['site_id'],row['link_id'])
        #df4 = pd.read_sql_query(query,conn)
        df4= df2.loc[(df2['site_id']==row['site_id']) & (df2['link_id']==row['link_id'])]
        t5 = timer() 
        f2.write(str(t5-t4b) + '\n')
        for index2, row2 in df4.iterrows():
            if pd.isnull(row2['file_name']): continue
            t6 = timer()
            checkFile(row2['site_id'],row2['link_id'],row2['response_id'],row2['file_name'],file_dir)
            t7 = timer()
            f3.write(str(row2['site_id'])+' '+str(row2['link_id'])+ ' '+str(row2['response_id'])+' ') 
            f3.write(str(t7-t6) + '\n')
    conn1.commit()
    t8 = timer()
    f1.write(str(t8-t1) + '\n')    
     
te = timer()
print "time: ", te-ts
f1.close()
f2.close()
f3.close()


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


