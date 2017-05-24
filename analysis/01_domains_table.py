import sys
import sqlite3
import os

openWPMdir = sys.argv[1]
filename = os.path.join(openWPMdir,'data/input/top-1m.csv')
res_dir = os.path.join(openWPMdir,'analysis/results/')
if not os.path.exists(res_dir):
    os.makedirs(res_dir)
db = res_dir + 'images.sqlite'
fhand = open(filename)
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Domains')

    
cur.execute('CREATE TABLE IF NOT EXISTS Domains (id INTEGER PRIMARY KEY AUTOINCREMENT, domain TEXT UNIQUE)')

for line in fhand:
    line = line.strip()
    [did,domain] = line.split(',')
    did = int(did)
    #print did, domain
    cur.execute('INSERT INTO Domains (id, domain) VALUES (?, ?)',(did,domain))
    #cur.execute('INSERT OR IGNORE INTO DomainsTwoPart (domainTwoPart) VALUES (?)',(twoPartDomain(domain),))
    if did % 100000 == 0: 
        conn.commit()
        print did

conn.close()
fhand.close()
    
