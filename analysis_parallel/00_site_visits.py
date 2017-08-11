import pandas as pd
import numpy as np
import sqlite3
import os
import sys


# write all site_visits tables into one table OpenWPM/analysis/results/site_visits.sqlite

#main_dir = '/home/nsarafij/project'

data_dir = sys.argv[1]
res_dir = sys.argv[2]

conn = sqlite3.connect(os.path.join(res_dir,'site_visits.sqlite'))
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS site_visits')
cur.execute('CREATE TABLE IF NOT EXISTS site_visits (site_id INTEGER NOT NULL, link_id INTEGER NOT NULL, success INTEGER NOT NULL CHECK (success IN (0,1)), no_links INTEGER,  \
    PRIMARY KEY (site_id, link_id))') 

k = 0
for i in range(0,1):
    db = os.path.join(data_dir,'output_'+str(i)+'01','crawl-data.sqlite')
    print db
    conn2 = sqlite3.connect(os.path.join(data_dir,'output_'+str(i)+'01','crawl-data.sqlite'))
    query = 'SELECT * FROM site_visits ORDER BY site_id, link_id ASC'
    df = pd.read_sql_query(query,conn2)
    conn2.close()
    for index,row in df.iterrows():
        success = 1
        if (row['link_id'] == 0 and pd.isnull(row['resp_time_3'])) or (row['link_id']!= 0 and pd.isnull(['resp_time_2'])) : 
            success = 0
        cur.execute('INSERT INTO site_visits (site_id, link_id, success, no_links) VALUES (?,?,?,?)',(row['link_id'],row['site_id'],success,row['no_links'])    
    conn.commit() 
       
conn.close()
