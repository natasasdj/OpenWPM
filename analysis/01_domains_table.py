import sys
import sqlite3
openWPMdir = sys.argv[1]
file = openWPMdir + 'data/input/top-1m.csv'
res_dir = openWPMdir + 'analysis/results/'
if not os.path.exists(res_dir):
    os.makedirs(res_dir)
db = res_dir + 'images.sqlite'
fhand = open(file)
conn = sqlite3.connect(db)
cur = conn.cursor()
#cur.execute('DROP TABLE IF EXISTS Domains')
cur.execute('CREATE TABLE IF NOT EXISTS Domains (id INTEGER PRIMARY KEY NOT NULL, domain TEXT UNIQUE)')
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
    
