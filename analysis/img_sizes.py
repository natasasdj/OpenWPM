'''import os

for root, dirs, files in os.walk('/path/to/dir', topdown=False):
    for name in files:
        f = os.path.join(root, name)
        if os.path.getsize(f) == filesize:
            os.remove(f)

import os
for file in os.listdir("/mydir"):
    if file.endswith(".txt"):
        print(file)


import os
for root, dirs, files in os.walk("/mydir"):
    for file in files:
        if file.endswith(".txt"):
             print(os.path.join(root, file))

'''

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


#To ensure that *.png file are read
#ImageFile.LOAD_TRUNCATED_IMAGES = True

curr_dir = os.getcwd()
data_dir = '/home/nsarafij/project/data/output_1_100/'
data_img_dir = data_dir+'httpResp/'
res_dir = curr_dir + '/results2/'
#res_dir_img = res_dir + '/images/'
if not os.path.exists(res_dir):
    os.makedirs(res_dir)
#if not os.path.exists(res_dir_img):
#    os.makedirs(res_dir_img)

no_sites = 100
max_no_links = 300
db_file=data_dir+'crawl-data.sqlite'
conn = sqlite3.connect(db_file)
filename = res_dir +'no_links.txt'
f1 = open(filename,'a')
filename = res_dir +'img_sizes.txt'
f2 = open(filename,'a')
k=1
for i in range(1,no_sites+1):    
    succ = 0
    j = 0
    print i
    query = 'SELECT * FROM site_visits WHERE site_id = {0} AND link_id = {1}'.format(i, j)
    df = pd.read_sql_query(query,conn)
    if pd.isnull(df.loc[0,'resp_time_3']): continue   
    s = str(i) + ' ' + str(df.loc[0,'no_links']) + ' '       
    f1.write(s)

    #while 1;
   
    #filename = res_dir_img +'f-'+str(i)
    #f3 = open(filename,'a') 
    for j in range(0,max_no_links+1):
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
        #filename = res_dir_img +'f-'+str(i)+'-'+str(j)
        #f4 = open(filename,'a')
        for index, row in df.iterrows():
            if pd.isnull(row['file_name']): continue
            if '.' in row['file_name']:  continue
            header = row['headers']
            i1 = header.find('"Content-Length",') 
            i2 = header.find('"', i1+len('"Content-Length"'))
            i3 = header.find('"', i2+1) 
            length = header[i2+1:i3]
            #length2 = str(header[i2+1:i3])
            #length3 =header.encode('utf=8')[i2+1:i3]
            filename = data_img_dir +'site-' + str(i) + '/' + row['file_name']
            size = os.path.getsize(filename)
            try:
                img = Image.open(filename)
                width, height = img.size
                no_pixels =   width * height
                img_format = img.format
            except Exception as e:
                print e
                img_format = "None2"
                no_pixels = 0
            #img.format
            #print "Dimensions:", img.size, "Total pixels:", width * height
            m = magic.open(magic.MAGIC_MIME)
            m.load()
            print m.file(filename)
            img_type = imghdr.what(filename) 
            s1 = str(k) + ' ' + str(row['site_id'])+ ' ' + str(row['link_id'])+ ' ' + str(row['response_id'])+' ' + str(size) +' ' + str(length) + ' '
            s2 = str(no_pixels) + ' ' + str(img_type) + ' ' + img_format + ' ' +str(m) + '\n'
            k += 1
            f2.write(s1)
            f2.write(s2)
            #f3.write(s)
            #f4.write(s)
        
        #f4.close()
         
        # j += 1
    #f3.close()
    s=str(succ)+'\n'
    f1.write(s)     

f1.close()
f2.close()
    



                    
         
                
        

