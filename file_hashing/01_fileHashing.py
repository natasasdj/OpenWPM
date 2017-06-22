import os
import sqlite3
import pandas as pd
import plyvel
import hashlib
import bz2
import re
import sys
from timeit import default_timer as timer

main_data_dir = sys.argv[1]
data_output = sys.argv[2]
data_dir = os.path.join(main_data_dir,data_output) 
hash_dir = sys.argv[3]
if not os.path.exists(hash_dir):
    os.makedirs(hash_dir)
start_site = data_dir.split("_")[1]
hash_dir = os.path.join(hash_dir, 'db_'+start_site)
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
		 count INTEGER, PRIMARY KEY (site_id, link_id, resp_id))')
cur1.execute('CREATE TABLE IF NOT EXISTS Htmls \
		(site_id INTEGER NOT NULL, link_id INTEGER NOT NULL, resp_id INTEGER NOT NULL, \
		 count INTEGER, file TEXT, PRIMARY KEY (site_id, link_id, resp_id))')


db_file = os.path.join(data_dir, 'crawl-data.sqlite')
print db_file
conn = sqlite3.connect(db_file)

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
    #print siteID, linkID, respID, filename, filedir
    filepath = os.path.join(filedir,filename)
    zipped = False
    if os.path.islink(filepath): return
    if not os.path.exists(filepath):
        if ("html" in filename) and os.path.exists(filepath+'.bz2'):
            #print "*** file is already zipped ***"
            zipped = True
        if not zipped: 
            print "there is no file", filename
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
    fname = hashDB.get(filehash.encode('utf8'))
    if fname is None:
        # put hash into hashHtml or hashImage level db
        hashDB.put(filehash.encode('utf8'),filename.encode('utf8'))
        query = 'INSERT INTO {} (site_id, link_id, resp_id, count) VALUES({},{},{},{})'.format(fileDB,siteID,linkID,respID,1)
        cur1.execute(query)
        if ("html" in filename): 
            if not zipped: bzip2(filepath)
            if not os.path.exists(filepath): print "filepath 1:", filepath
            os.remove(filepath)
    elif fname == filename:
        return
    else:       
        # create symlink        
        f = fname.rstrip(".html").split("-")
        fpath = os.path.join(data_dir, 'output_' + str((int(f[1])-1)/100) + '01','httpResp/site-' + f[1], fname)
        if not os.path.exists(filepath): print "filepath 2:", filepath        
        os.remove(filepath)        
        if ("html" in filename): 
            os.symlink(fpath+'.bz2',filepath)
        else:
            os.symlink(fpath,filepath)  
        cur1.execute('SELECT count FROM {} WHERE site_id = {} and link_id = {} and resp_id = {}'.format(fileDB,f[1],f[2],f[3]))
        data=cur1.fetchone()
        if data is None:
            query = 'INSERT INTO {} (site_id, link_id, resp_id, count) VALUES({},{},{},{})'.format(fileDB,siteID,linkID,respID,1)
        else:
            query = 'UPDATE {} SET count = {} WHERE site_id = {} and link_id = {} and resp_id = {}'.format(fileDB,data[0] + 1,f[1],f[2],f[3])
        cur1.execute(query)
              

def purge(directory, pattern):
    for f in os.listdir(directory):
        if re.search(pattern, f):
            #print "*************************** purge ****************************************", f
            os.remove(os.path.join(directory, f))


ts = timer()

t0 = timer()
query = 'SELECT site_id, link_id FROM site_visits WHERE ((link_id = 0 AND resp_time_3 IS NOT NULL) OR (link_id != 0 AND resp_time_2 IS NOT NULL))'
df1 = pd.read_sql_query(query,conn)

query = 'SELECT site_id,link_id FROM site_visits WHERE ((link_id = 0 AND resp_time_3 IS NULL) OR (link_id != 0 AND resp_time_2 IS NULL))'
df1b = pd.read_sql_query(query,conn)

#t = timer()
query = 'SELECT site_id,link_id,response_id,file_name FROM http_responses WHERE (file_name IS NOT NULL)'
df2 = pd.read_sql_query(query,conn)
#t_ = timer()
#print "time ", t_ - t

df = df1.merge(df2, on = ('site_id','link_id'),how='inner').sort_values(['site_id','link_id','response_id'])
df3 = df1b.merge(df2, on = ('site_id','link_id'),how='inner').sort_values(['site_id','link_id','response_id'])

t1 = timer()
print "time for getting data:", t1 - t0

t1=timer()
for index, row in df3.iterrows():
    file_dir = os.path.join(data_dir, 'httpResp','site-'+ str(row['site_id']))
    if not os.path.exists(file_dir): continue
    filepath = "file-"+str(row['site_id'])+"-"+str(row['link_id'])+"-\d+"
    if row['link_id'] == 0:
        purge(file_dir,filepath) 
        os.rmdir(file_dir) 
    else:
        purge(file_dir,filepath)
        
t2 = timer()
print "deleting time: ", t2 - t1

t2=timer()
k=0
for index, row in df.iterrows():      
    file_dir = os.path.join(data_dir, 'httpResp','site-'+ str(row['site_id'])) 
    if not os.path.exists(file_dir): continue
    checkFile(row['site_id'],row['link_id'],row['response_id'],row['file_name'],file_dir)
    k =+ 1
    if k % 1000 == 0:
        print row['site_id'] 
        conn1.commit()  

conn1.commit() 

t3 = timer()
print "hashing time: ", t3 - t2     
     
     
te = timer()
print "time: ", te-ts



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


