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

query = 'SELECT * FROM site_visits WHERE (link_id = 0 AND resp_time_3 IS NOT NULL) OR (link_id != 0 AND resp_time_2 IS NOT NULL)'
df1 = pd.read_sql_query(query,conn)

query = "SELECT * FROM http_responses WHERE (file_name IS NOT NULL) AND (NOT instr(file_name, 'html') > 0);"
df2 = pd.read_sql_query(query,conn)

df = df1.merge(df2, on = ('site_id','link_id'),how='inner').sort_values(['site_id','link_id','response_id'])
print df.shape[0]

t1 = timer()
print "time for getting data:", t1 - ts


k = 0
for index, row in df.iterrows():
    k += 1
    if k % 1000 == 0:
        print row['site_id']
        conn1.commit()
    if pd.isnull(row['file_name']): continue
    if 'html' in row['file_name']:  continue
    url = row['url']
    domain = urlparse(url).hostname.strip('www.')
    cur1.execute('SELECT id FROM Domains WHERE domain = ?',(domain,)) 
    try:
        domain_id = cur1.fetchone()[0]
    except:
        cur1.execute('INSERT INTO Domains (id,domain) VALUES (?,?)',(None,domain))

conn1.commit()
    
te = timer()
print "time:", te - ts


conn1.close()
conn.close()  

