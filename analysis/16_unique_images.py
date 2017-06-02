import os
import sqlite3
db_dir = '/root/OpenWPM/file_hashing/db'
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
    
db=os.path.join(db_dir,'uniqueFiles.sqlite')
conn=sqlite3.connect(db)
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Images')
cur.execute('CREATE TABLE IF NOT EXISTS Images (site_id INTEGER NOT NULL, link_id INTEGER NOT NULL, resp_id INTEGER NOT NULL, count INTEGER, PRIMARY KEY (site_id,link_id,resp_id))')
db2='/root/OpenWPM/analysis/results/images.sqlite'
conn2 = sqlite3.connect(db2)
cur2 = conn2.cursor()
cur2.execute('SELECT * FROM Images')
k=0
for row in cur2:
    k+=1
    print row
    site_id = row[0]; link_id = row[1]; resp_id = row[2]
    j = (site_id -1) / 100
    filedir = '/root/data/output_'+str(j) +'01' + '/httpResp/site-'+ str(site_id)
    filename = 'file-' + str(site_id) + '-' + str(link_id) + '-' + str(resp_id)
    filepath = os.path.join(filedir,filename)
    #f=filename.split('-')
    #site_id = f[1]; link_id = f[2]; resp_id = f[3]
    print "********************** filename", filename, site_id, link_id, resp_id
    cur.execute('SELECT * FROM Images WHERE site_id = ? and link_id = ? and resp_id = ?',(site_id,link_id,resp_id))       
    data=cur.fetchone()
    if data is not None:
        print "***** file already exists" 
        continue
    if not os.path.islink(filepath):
        print "***** no symlink" 
        cur.execute('INSERT INTO Images (site_id,link_id,resp_id,count) VALUES (?,?,?,1)',(site_id,link_id,resp_id))
    else:
        print "***** symlink"
        freal = os.readlink(filepath)
        print freal
        fname = freal.split('/')[-1]
        print fname  
        f=fname.split('-')
        site_id = f[1]; link_id = f[2]; resp_id = f[3]
        print "symlink", site_id, link_id, resp_id
        cur.execute('SELECT * FROM Images WHERE site_id = ? and link_id = ? and resp_id = ?',(site_id,link_id,resp_id))       
        data=cur.fetchone()
        print data
        if data is None:
            cur.execute('INSERT INTO Images (site_id,link_id,resp_id,count) VALUES (?,?,?,2)',(site_id,link_id,resp_id))
        else:
            cur.execute('UPDATE Images SET count = ? WHERE site_id = ? and link_id = ? and resp_id = ?',(data[3]+1, site_id,link_id,resp_id))              
    if k%100 == 0:
        conn.commit() 
        
        
conn.commit()
conn.close()
conn2.close()
    
    
'''        

for i in range(0,1):
    j = i / 100
    site_dir = '/root/data/output_'+str(j) +'01' + '/httpResp/site-'+ str(i+1)
    for (dirpath, dirnames, filenames) in os.walk(site_dir):
        for filename in filenames:
            if 'html' in filename: continue
            filepath= os.path.join(dirpath,filename)
            f=filename.split('-')
            site_id = f[1]; link_id = f[2]; resp_id = f[3]
            print "********************** filename", filename, site_id, link_id, resp_id
            cur.execute('SELECT * FROM Images WHERE site_id = ? and link_id = ? and resp_id = ?',(site_id,link_id,resp_id))       
            data=cur.fetchone()
            if data is not None:
                print "***** file already exists" 
                continue
            if not os.path.islink(filepath):
                print "***** no symlink" 
                cur.execute('INSERT INTO Images (site_id,link_id,resp_id,count) VALUES (?,?,?,1)',(site_id,link_id,resp_id))
            else:
                print "***** symlink"
                freal = os.readlink(filepath)
                print freal
                fname = freal.split('/')[-1]
                print fname  
                f=fname.split('-')
                site_id = f[1]; link_id = f[2]; resp_id = f[3]
                print "symlink", site_id, link_id, resp_id
                cur.execute('SELECT * FROM Images WHERE site_id = ? and link_id = ? and resp_id = ?',(site_id,link_id,resp_id))       
                data=cur.fetchone()
                print data
                if data is None:
                    cur.execute('INSERT INTO Images (site_id,link_id,resp_id,count) VALUES (?,?,?,2)',(site_id,link_id,resp_id))
                else:
                    cur.execute('UPDATE Images SET count = ? WHERE site_id = ? and link_id = ? and resp_id = ?',(data[3]+1, site_id,link_id,resp_id))    
                
    conn.commit()

'''            
     
    
     
