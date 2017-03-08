import sqlite3
file = '/home/nsarafij/project/OpenWPM/data/input/top-1m.csv'
db = '/home/nsarafij/project/OpenWPM/analysis/results/images.sqlite'
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
    
