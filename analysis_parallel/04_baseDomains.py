import sqlite3
import os
import sys
import pandas as pd
from tld import get_tld
from tld.utils import update_tld_names
update_tld_names()

'''
def findAll(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]
    
def twoPart_domain(domain):
    points=findAll(domain,'.')
    if len(points)<2: return domain
    return domain[points[-2]+1:]
'''

def domain2(domain):
    try:
        return get_tld(domain, fix_protocol=True)
    except:
        return domain

#res_dir = '/home/nsarafij/project/OpenWPM/analysis/results/'
#res_dir = '/home/nsarafij/project/nsdjWPM/analysis/results/'
res_dir = sys.argv[1]
db = os.path.join(res_dir,'domains.sqlite')
conn = sqlite3.connect(db)
cur = conn.cursor()
x=cur.execute('DROP TABLE IF EXISTS BaseDomains')
x=cur.execute('DROP TABLE IF EXISTS Domain_BaseDomain')
x=cur.execute('CREATE TABLE IF NOT EXISTS BaseDomains (id INTEGER PRIMARY KEY AUTOINCREMENT, baseDomain TEXT UNIQUE)')
x=cur.execute('CREATE TABLE IF NOT EXISTS Domain_BaseDomain (domain_id INTEGER UNIQUE, baseDomain_id INTEGER, \
            FOREIGN KEY (domain_id) REFERENCES Domains(id), FOREIGN KEY (baseDomain_id) REFERENCES BaseDomains(id))')
            
domains = pd.read_sql_query('SELECT * FROM Domains',conn)

i = 0
for index,row in domains.iterrows(): 
    i += 1   
    baseDomain = domain2(row['domain'])    
    x=cur.execute('SELECT id FROM BaseDomains WHERE baseDomain = ?',(baseDomain,))       
    data=cur.fetchone()
    if data is not None: 
        baseDomain_id=data[0]       
    else:
        x=cur.execute('INSERT INTO BaseDomains (baseDomain) VALUES (?)',(baseDomain,))
        baseDomain_id = cur.lastrowid
    x=cur.execute('INSERT INTO Domain_BaseDomain (domain_id,baseDomain_id) VALUES (?,?)',(row['id'],baseDomain_id))
    if i % 10000 == 0: 
        print row['id'], row['domain'], baseDomain, baseDomain_id
        conn.commit()


conn.commit()
conn.close()
 



