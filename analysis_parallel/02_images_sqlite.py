import sys
import os
import sqlite3
import pandas as pd
from urlparse import urlparse
from magic import from_file as magic_from_file
import re
import xml.etree.ElementTree as ET
from PIL import Image
from timeit import default_timer as timer


data_dir = sys.argv[1]
print data_dir
start_site = data_dir.split("_")[1]
data_img_dir = os.path.join(data_dir,'httpResp')
print data_img_dir
res_dir = sys.argv[2]
if not os.path.exists(res_dir):
    os.makedirs(res_dir)
print res_dir

db = os.path.join(res_dir,'images_' + start_site + '.sqlite') #sys.argv[1]
print db
conn1 = sqlite3.connect(db)
cur1 = conn1.cursor()
#cur1.execute('DROP TABLE IF EXISTS Images')

cur1.execute('CREATE TABLE IF NOT EXISTS Images (site_id INTEGER NOT NULL, link_id INTEGER NOT NULL, resp_id INTEGER NOT NULL, \
                                  resp_domain INTEGER NOT NULL, size INTEGER NOT NULL, cont_length INTEGER NOT NULL, \
                                  type INTEGER,  cont_type INTEGER, pixels INTEGER,  \
                                  PRIMARY KEY (site_id, link_id, resp_id), \
                                  FOREIGN KEY (type) REFERENCES Types(id))')


cur1.execute('CREATE TABLE IF NOT EXISTS Types (id INTEGER PRIMARY KEY NOT NULL, type TEXT UNIQUE)')

db = res_dir + 'domains.sqlite'
conn2 = sqlite3.connect(db)
cur2 = conn2.cursor()

db= os.path.join(data_dir,'crawl-data.sqlite')
conn = sqlite3.connect(db)



ts = timer()

query = 'SELECT * FROM site_visits WHERE (link_id = 0 AND resp_time_2 IS NOT NULL) OR (link_id != 0 AND resp_time_3 IS NOT NULL) ORDER BY site_id ASC, link_id ASC'
df1 = pd.read_sql_query(query,conn)
print "start 2"
query = 'SELECT * FROM http_responses'
df2 = pd.read_sql_query(query,conn)
print "start 3"
df = df1.merge(df2, on = ('site_id','link_id'),how='left')

k = 0 
for index, row in df.iterrows():
    # print row['site_id'],row['link_id'], row['response_id'] 
    if pd.isnull(row['file_name']): continue
    if 'html' in row['file_name']:  continue
    header = row['headers']
    i1 = header.find('"Content-Length",') 
    i2 = header.find('"', i1+len('"Content-Length"'))
    i3 = header.find('"', i2+1) 
    cont_length = header[i2+1:i3]
    i1 = header.find('"Content-Type",') 
    i2 = header.find('"', i1+len('"Content-Type"'))
    i3 = header.find('"', i2+1) 
    cont_type = header[i2+1:i3].lower()
    cont_type = re.sub("[,;].*","",cont_type)
    try:
        cont_type_id = cur1.fetchone()[0]
    except:
        cur1.execute('INSERT INTO Types (id,type) VALUES (?,?)',(None,cont_type))
        cont_type_id = cur1.lastrowid
    url = row['url']
    domain = urlparse(url).hostname.strip('www.')
    cur2.execute('SELECT id FROM Domains WHERE domain = ?',(domain,)) 
    try:
       domain_id = cur2.fetchone()[0]
    except:
       domain_id = None
   
    filename = os.path.join(data_img_dir,'site-' + str(row['site_id']),row['file_name'])
    no_pixels = None; size = None; type_id = None
    try:
        size = os.path.getsize(filename)
        img_type = magic_from_file(filename, mime=True).lower()
        img_type = re.sub("[,;].*","",img_type      
        try: 
            img = Image.open(filename)
            width, height = img.size
            no_pixels = width*height
        except:           
            try:
                height = ET. parse(filename).getroot().attrib["height"]
                height = int(re.sub("[^0-9]", "", height))
                width = ET.parse(filename).getroot().attrib["width"] 
                width = int(re.sub("[^0-9]", "", width))
                no_pixels = height * width
            except:
                pass

        if img_type in cont_type: cont_type = img_type
        if 'jpg' in cont_type: cont_type = 'image/jpeg'
        if 'bmp' in cont_type: cont_type = 'image/bmp'
        if 'bitmap' in cont_type: cont_type = 'image/bmp'
        if 'bmp' in img_type: img_type = 'image/bmp'
        if 'bitmap' in img_type: img_type = 'image/bmp'           
        if 'icon' in cont_type: cont_type = 'image/x-icon'
        if 'icon' in img_type: img_type = 'image/x-icon'           
        
        cur1.execute('SELECT id FROM Types WHERE type = ?',(img_type,))
        try:
            type_id = cur1.fetchone()[0]
        except:
            cur1.execute('INSERT INTO Types (id,type) VALUES (?,?)',(None,img_type))
            type_id = cur1.lastrowid

        cur1.execute('SELECT id FROM Types WHERE type = ?',(cont_type,))
   
     except:
        pass
    cur1.execute('INSERT INTO Images (site_id, link_id, resp_id, resp_domain, size, cont_length, type, cont_type, pixels) \        
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)', (row['site_id'], row['link_id'], row['response_id'], domain_id, size, cont_length, type_id, cont_type_id, no_pixels)) 
                 
    k += 1
    if k % 100:
        print row['site_id']
        conn1.commit()

conn1.commit()





'''
for index, row in df.iterrows():
    print row['site_id'],row['link_id']
    t1 = timer()
    #if row['site_id']>2: break    
    if row['link_id'] ==0:
        if pd.isnull(row['resp_time_3']): continue
    else:
        if pd.isnull(row['resp_time_2']): continue
    #s = str(row['site_id']) + ' ' + str(df.loc[0,'no_links']) + ' '               
    df2 = df1.loc[(df1['site_id'] == row['site_id']) & (df1['link_id'] == row['link_id'])]
    #print df2 
    t2 = timer()
    for index2, row2 in df2.iterrows():
        #print row2
        t3 = timer()
        if pd.isnull(row2['file_name']): continue
        if 'html' in row2['file_name']:  continue
        header = row2['headers']
        i1 = header.find('"Content-Length",') 
        i2 = header.find('"', i1+len('"Content-Length"'))
        i3 = header.find('"', i2+1) 
        cont_length = header[i2+1:i3]
        i1 = header.find('"Content-Type",') 
        i2 = header.find('"', i1+len('"Content-Type"'))
        i3 = header.find('"', i2+1) 
        cont_type = header[i2+1:i3].lower()
        cont_type = re.sub("[,;].*","",cont_type)
        url = row2['url']
        domain = urlparse(url).hostname.strip('www.')
        filename = os.path.join(data_img_dir,'site-' + str(row2['site_id']),row2['file_name'])
        img_type = magic_from_file(filename, mime=True).lower()
        img_type = re.sub("[,;].*","",img_type)
        #if img_type != cont_type and ('svg' not in cont_type):
            #print img_type, cont_type
        no_pixels = None
        try: 
            img = Image.open(filename)
            width, height = img.size
            no_pixels = width*height
        except: 
            #if 'svg' in img_type: print 10*"svg"             
            try:
                height = ET. parse(filename).getroot().attrib["height"]
                height = int(re.sub("[^0-9]", "", height))
                width = ET.parse(filename).getroot().attrib["width"] 
                width = int(re.sub("[^0-9]", "", width))
                no_pixels = height * width
            except:
                pass
            #print row2['site_id'],row2['link_id'], row2['response_id'], 'no_pixels:', no_pixels, img_type, cont_type, t
        
        #print img_type
        if img_type in cont_type: cont_type = img_type
        if 'jpg' in cont_type: cont_type = 'image/jpeg'
        if 'bmp' in cont_type: cont_type = 'image/bmp'
        if 'bitmap' in cont_type: cont_type = 'image/bmp'
        if 'bmp' in img_type: img_type = 'image/bmp'
        if 'bitmap' in img_type: img_type = 'image/bmp'           
        if 'icon' in cont_type: cont_type = 'image/x-icon'
        if 'icon' in img_type: img_type = 'image/x-icon'           
        
        t4 = timer()
        
        cur1.execute('SELECT id FROM Types WHERE type = ?',(img_type,))
        try:
            type_id = cur1.fetchone()[0]
        except:
            cur1.execute('INSERT INTO Types (id,type) VALUES (?,?)',(None,img_type))
            type_id = cur1.lastrowid

        cur1.execute('SELECT id FROM Types WHERE type = ?',(cont_type,))
        try:
            cont_type_id = cur1.fetchone()[0]
        except:
            cur1.execute('INSERT INTO Types (id,type) VALUES (?,?)',(None,cont_type))
            cont_type_id = cur1.lastrowid
        cur2.execute('SELECT id FROM Domains WHERE domain = ?',(domain,)) 
        try:
           domain_id = cur2.fetchone()[0]
        except:
           domain_id = None
        size = os.path.getsize(filename)

        cur1.execute('INSERT INTO Images (site_id, link_id, resp_id, resp_domain, size, cont_length, type, cont_type, pixels) \
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)', (row2['site_id'], row2['link_id'], row2['response_id'], domain_id, size, cont_length, type_id, cont_type_id, no_pixels)) 
        t5 = timer()
        f2.write(str(row2['site_id']) + ' ' + str(row2['link_id']) + ' ' + str(row2['response_id']) + ' '  + str(t3-t2) + ' '  + str(t4-t3) + ' '   + str(t5-t4) + '\n'   )
    f1.write(str(row['site_id']) + ' '  + str(row['link_id']) + ' '  + str(t2-t1) + '\n'  )           
    conn1.commit()
    conn2.commit()
    
'''    
te = timer()
print "time:", te - ts

conn1.close()
conn2.close()
conn.close()  


                    
                   
         
                
        

