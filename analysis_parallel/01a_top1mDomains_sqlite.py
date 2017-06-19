import sys
import sqlite3
import os

data_dir = sys.argv[1]
print data_dir
filename = os.path.join(data_dir,'top-1m.csv')
fhand = open(filename)

res_dir = sys.argv[2]
print res_dir
if not os.path.exists(res_dir):
    os.makedirs(res_dir)
    
db = os.path.join(res_dir,'domains.sqlite')
print db
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
    if did % 100000 == 0: 
        conn.commit()
        print did

conn.close()
fhand.close()
    
