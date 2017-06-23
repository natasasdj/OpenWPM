import os
import sys
import plyvel
import sqlite3
from shutil import copytree
from timeit import default_timer as timer



data_dir = sys.argv[1]
hash_dir = sys.argv[2]

db1 = os.path.join(hash_dir,sys.argv[3])
split = db1.split("_")
first = split[1]
db2 = os.path.join(hash_dir,sys.argv[4])
split = db2.split("_")
second = split[-1]
db = os.path.join(hash_dir,'db_' + first + '_' + second)
if not os.path.exists(db): copytree(db1,db)

db_path = os.path.join(db, 'hashImage.ldb')
hashImage = plyvel.DB(db_path)
db_path = os.path.join(db, 'hashHtml.ldb')
hashHtml = plyvel.DB(db_path)


db_path = os.path.join(db2, 'hashImage.ldb')
hash2Image = plyvel.DB(db_path)
db_path = os.path.join(db2, 'hashHtml.ldb')
hash2Html = plyvel.DB(db_path)

db_name = os.path.join(db,'fileHashing.sqlite')
conn = sqlite3.connect(db_name)
cur = conn.cursor()


for key2, value2 in hash2Image:
    value = hashImage.get(key2)
    if value:
        if value2 == value: continue
        f=value.rstrip(".html").split('-')
        print f
        f2=value2.rstrip(".html").split('-')
        print f2
        fpath = os.path.join(data_dir,'output_' + str((int(f[1])-1)/100) + '01', 'httpResp','site-'+f[1],value)
        if not os.path.exists(fpath): print "fpath Image", fpath
        f2path = os.path.join(data_dir, 'output_' + str((int(f2[1])-1)/100) + '01', 'httpResp','site-'+f2[1],value2)
        if not os.path.exists(f2path): print "f2path Image", f2path
        os.remove(f2path)        
        os.symlink(fpath,f2path)  
        cur.execute('SELECT count FROM Images WHERE site_id = {} and link_id = {} and resp_id = {}'.format(f[1],f[2],f[3]))
        cur.execute('UPDATE Images SET count = {3} WHERE site_id = {0} and link_id = {1} and resp_id = {2}'.format(f[1],f[2],f[3],cur.fetchone()[0] + 1))
    else:
        hashImage.put(key2,value2)
        f2=value2.rstrip(".html").split('-')
        cur.execute('INSERT INTO Images (site_id, link_id, resp_id, count) VALUES({},{},{},{})'.format(f2[1],f2[2],f2[3],1))     
conn.commit()

for key2, value2 in hash2Html:
    value = hashHtml.get(key2)
    if value:
        if value2 == value: continue
        f=value.rstrip(".html").split('-')
        print f
        f2=value2.rstrip(".html").split('-')
        print f2
        fpath = os.path.join(data_dir, 'output_' + str((int(f[1])-1)/100) + '01', 'httpResp','site-'+f[1], value + '.bz2')
        if not os.path.exists(fpath): print "fpath Html", fpath 
        f2path = os.path.join(data_dir, 'output_' + str((int(f2[1])-1)/100) + '01', 'httpResp','site-'+f2[1], value2)
        if not os.path.exists(f2path): print "f2path Html", f2path
        os.remove(f2path  + '.bz2')        
        os.symlink(fpath, f2path)  
        cur.execute('SELECT count FROM Htmls WHERE site_id = {} and link_id = {} and resp_id = {}'.format(f[1],f[2],f[3]))
        cur.execute('UPDATE Htmls SET count = {3} WHERE site_id = {0} and link_id = {1} and resp_id = {2}'.format(f[1],f[2],f[3],cur.fetchone()[0] + 1))
    else:
        hashHtml.put(key2,value2)
        f2=value2.rstrip(".html").split('-')
        print f2
        cur.execute('INSERT INTO Htmls (site_id, link_id, resp_id, count) VALUES({},{},{},{})'.format(f2[1],f2[2],f2[3],1))            
conn.commit()

conn.close()
#rm -rf db2_dir   


