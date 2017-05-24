import sqlite3
import pandas as pd
from shutil import copyfile
import os

data_dir = '/home/nsarafij/project/data/'
out_dir = '/home/nsarafij/project/OpenWPM/analysis/nonregular/0-pixel_images/'
db = '/home/nsarafij/project/OpenWPM/analysis/results/images.sqlite'
conn= sqlite3.connect(db)

query = 'SELECT * FROM Images JOIN Types ON Images.type = Types.id WHERE pixels=0 AND site_id > 4700'
df = pd.read_sql_query(query,conn)

for ind, row in df.iterrows():
    print row['site_id']
    if 4701<=row['site_id']<=4800:
        ddir = 'output_4701'
    elif 4701<=row['site_id']<=4800:
        ddir = 'output_4801'
    else: 
        break
    site_dir = os.path.join(data_dir,ddir+'/httpResp/site-'+str(row['site_id']))
    if not os.path.exists(site_dir):
        print "does not exists: ", site_dir
        continue
    filename = 'file-' + str(row['site_id']) + '-' + str(row['link_id']) + '-' + str(row['resp_id'])
    src = os.path.join(site_dir, filename)
    print src
    dst = os.path.join(out_dir, filename)
    print dst 
    copyfile(src, dst)
    
 



