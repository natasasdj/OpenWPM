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
res_dir = sys.argv[2]
if not os.path.exists(res_dir):
    os.makedirs(res_dir)
print res_dir

db = os.path.join(res_dir,sys.argv[3]) #sys.argv[1]
print db
conn1 = sqlite3.connect(db)
cur1 = conn1.cursor()

cur1.execute('CREATE TABLE IF NOT EXISTS Images (site_id INTEGER NOT NULL, link_id INTEGER NOT NULL, resp_id INTEGER NOT NULL, \
                                  resp_domain INTEGER NOT NULL, size INTEGER, cont_length INTEGER, \
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

query = 'SELECT * FROM site_visits WHERE (link_id = 0 AND resp_time_3 IS NOT NULL) OR (link_id != 0 AND resp_time_2 IS NOT NULL)'
df1 = pd.read_sql_query(query,conn)

query = "SELECT * FROM http_responses WHERE (file_name IS NOT NULL) AND (NOT instr(file_name, 'html') > 0);"
df2 = pd.read_sql_query(query,conn)

df = df1.merge(df2, on = ('site_id','link_id'),how='inner').sort_values(['site_id','link_id','response_id'])

t1 = timer()
print "time for getting data:", t1 - ts

k = 0 
for index, row in df.iterrows():
    # print row['site_id'],row['link_id'], row['response_id'] 
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
    cur1.execute('SELECT id FROM Types WHERE type = ?',(cont_type,))
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
        img_type = re.sub("[,;].*","",img_type)      
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

        
   
    except:
        pass

    cur1.execute('INSERT INTO Images (site_id, link_id, resp_id, resp_domain, size, cont_length, type, cont_type, pixels) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)', (row['site_id'], row['link_id'], row['response_id'], domain_id, size, cont_length, type_id, cont_type_id, no_pixels)) 
                 
    k += 1
    if k % 100:
        print row['site_id']
        conn1.commit()

conn1.commit()

   
te = timer()
print "time:", te - ts

conn1.close()
conn2.close()
conn.close()  


                    
                   
         
                
        

