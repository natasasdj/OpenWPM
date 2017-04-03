import sys
import os
import sqlite3
import pandas as pd
import numpy as np
from PIL import Image
#import os.path
import imghdr
import logging
#logging.basicConfig()
from PIL import ImageFile
import magic
from urlparse import urlparse
import rsvg
import cairo
#To ensure that *.png file are read
#ImageFile.LOAD_TRUNCATED_IMAGES = True

data_dir = sys.argv[1]
no_db = int(data_dir[data_dir.find("_")+1:-3])

curr_dir = os.getcwd()
data_img_dir = data_dir+'httpResp/'
res_dir = curr_dir + '/results/'
if not os.path.exists(res_dir):
    os.makedirs(res_dir)

db = res_dir + 'images.sqlite'
conn1 = sqlite3.connect(db)
cur1 = conn1.cursor()
#cur1.execute('DROP TABLE IF EXISTS Images')

cur1.execute('CREATE TABLE IF NOT EXISTS Images (site_id INTEGER NOT NULL, link_id INTEGER NOT NULL, resp_id INTEGER NOT NULL, \
                                  resp_domain INTEGER NOT NULL, size INTEGER NOT NULL, cont_length INTEGER NOT NULL, \
                                  type INTEGER,  cont_type INTEGER, pixels INTEGER,  \
                                  PRIMARY KEY (site_id, link_id, resp_id), \
                                  FOREIGN KEY (site_id) REFERENCES Domains(id),\
                                  FOREIGN KEY (resp_domain) REFERENCES Domains(id),\
                                  FOREIGN KEY (type) REFERENCES Types(id) )')


cur1.execute('DROP TABLE IF EXISTS Types')
cur1.execute('CREATE TABLE IF NOT EXISTS Types (id INTEGER PRIMARY KEY NOT NULL, type TEXT UNIQUE)')



no_sites = 100
max_no_links = 300
db_file=data_dir+'crawl-data.sqlite'
print db_file
conn = sqlite3.connect(db_file)

#filename = res_dir +'no_links.txt'
#f1 = open(filename,'a')
#filename = res_dir +'img_sizes.txt'
#f2 = open(filename,'a')
for i in range(no_db*100+1,no_db*100+no_sites+1):    
    succ = 0
    j = 0
    print i
    query = 'SELECT * FROM site_visits WHERE site_id = {0} AND link_id = {1}'.format(i, j)
    df = pd.read_sql_query(query,conn)
    if pd.isnull(df.loc[0,'resp_time_3']): continue   
    s = str(i) + ' ' + str(df.loc[0,'no_links']) + ' '       
    #f1.write(s)


    for j in range(0,max_no_links+1):
        #print i, j
        if j!=0:  
            query = 'SELECT * FROM site_visits WHERE site_id = {0} AND link_id = {1}'.format(i, j)
            df = pd.read_sql_query(query,conn)
        if len(df.index)==0: break
        if pd.isnull(df.loc[0,'resp_time_2']):
            # j += 1 
            continue
        succ += 1              
        query = 'SELECT * FROM http_responses WHERE site_id = {0} AND link_id = {1}'.format(i, j)
        df = pd.read_sql_query(query,conn)  

        #f4 = open(filename,'a')
        for index, row in df.iterrows():
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
            cont_type = header[i2+1:i3]
            url = row['url']
            domain = urlparse(url).hostname.strip('www.')
            
            filename = data_img_dir +'site-' + str(i) + '/' + row['file_name']
            img_type = magic.from_file(filename, mime=True)
            cur1.execute('SELECT id FROM Types WHERE type = ?',(img_type,))
            try:
               type_id = cur1.fetchone()[0]
            except:
               cur1.execute('INSERT INTO Types (id,type) VALUES (?,?)',(None,img_type))
               type_id = cur1.lastrowid
            if img_type in cont_type: cont_type = img_type
            cur1.execute('SELECT id FROM Types WHERE type = ?',(cont_type,))
            try:
               cont_type_id = cur1.fetchone()[0]
            except:
               cur1.execute('INSERT INTO Types (id,type) VALUES (?,?)',(None,cont_type))
               cont_type_id = cur1.lastrowid
            cur1.execute('SELECT id FROM Domains WHERE domain = ?',(domain,))  
            try:
               domain_id = cur1.fetchone()[0]
            except:
               cur1.execute('INSERT INTO Domains (id,domain) VALUES (?,?)',(None,domain))
               domain_id = cur1.lastrowid
            size = os.path.getsize(filename)
            #print i,j, cont_length, size, cont_type, img_type  
            #print url, domain
            #print type_id, domain_id
            # if img_type not in cont_type: print img_type, cont_type
            no_pixels = None
            try: 
                img = Image.open(filename)
                width, height = img.size
                no_pixels = width*height
            except:           
               try:
                  svg = rsvg.Handle(file=filename)
                  width = svg.props.width
                  height = svg.props.height
                  no_pixels = width * height
               except: 
                  pass
                    
            #print (row['site_id'], row['link_id'], row['response_id'], domain_id, size, cont_length, type_id, cont_type_id, no_pixels)
            #cur1.execute('INSERT IF NOT EXISTS INTO Images (site_id, link_id, resp_id) VALUES (?, ?, ?)', (row['site_id'], row['link_id'], row['response_id'])) 
            cur1.execute('INSERT INTO Images (site_id, link_id, resp_id, resp_domain, size, cont_length, type, cont_type, pixels) \
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)', (row['site_id'], row['link_id'], row['response_id'], domain_id, size, cont_length, type_id, cont_type_id, no_pixels)) 
    conn1.commit()
conn1.close()
conn.close()    
'''
            
            
            filename = data_img_dir +'site-' + str(i) + '/' + row['file_name']
            
         
                
            
                           
            s1 = str(k) + ' ' + str(row['site_id'])+ ' ' + str(row['link_id'])+ ' ' + str(row['response_id'])+' ' + str(size) +' ' + str(length) + ' '
            s2 = str(no_pixels) + ' ' + str(img_type) + ' ' + img_format + ' ' + str() + '\n'
            print s1,s2
            
            curr


            #f2.write(s1)
            #f2.write(s2)
            #f3.write(s)
            #f4.write(s)
        
        #f4.close()
         
        # j += 1
    #f3.close()
    s=str(succ)+'\n'
    #f1.write(s)     

#f1.close()
#f2.close()
    
'''


                    
         
                
        

