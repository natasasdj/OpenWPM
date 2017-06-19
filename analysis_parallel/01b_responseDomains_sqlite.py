import sys
import sqlite3
import os
import pandas as pd
from urlparse import urlparse

from timeit import default_timer as timer

data_dir = sys.argv[1]
db = os.path.join(data_dir,'crawl-data.sqlite')
print db
conn = sqlite3.connect(db)

res_dir = sys.argv[2]

db = os.path.join(res_dir,'domains.sqlite')
print db
conn1 = sqlite3.connect(db)
cur1 = conn1.cursor()

ts = timer()

print "start 1"
query = 'SELECT * FROM site_visits ORDER BY site_id ASC, link_id ASC'
df = pd.read_sql_query(query,conn)
print "start 2"
query = 'SELECT * FROM http_responses'
df1 = pd.read_sql_query(query,conn)
print "start 3"

for index, row in df.iterrows():
    print row['site_id'],row['link_id']   
    if row['link_id'] ==0:
        if pd.isnull(row['resp_time_3']): continue
    else:
        if pd.isnull(row['resp_time_2']): continue              
    df2 = df1.loc[(df1['site_id'] == row['site_id']) & (df1['link_id'] == row['link_id'])]
    for index2, row2 in df2.iterrows():
        if pd.isnull(row2['file_name']): continue
        if 'html' in row2['file_name']:  continue
        url = row2['url']
        domain = urlparse(url).hostname.strip('www.')
        cur1.execute('SELECT id FROM Domains WHERE domain = ?',(domain,)) 
        try:
           domain_id = cur1.fetchone()[0]
        except:
           cur1.execute('INSERT INTO Domains (id,domain) VALUES (?,?)',(None,domain))
           domain_id = cur1.lastrowid
    conn1.commit()
    
te = timer()
print "time:", te - ts

conn1.close()
conn.close()  

