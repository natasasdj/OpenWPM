import sqlite3
conn = sqlite3.connect('/home/nsarafij/project/OpenWPM/file_hashing/db2/DBwithPK.sqlite')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS Images \
		(site_id INTEGER NOT NULL, link_id INTEGER NOT NULL, resp_id INTEGER NOT NULL, \
		 count INTEGER, file TEXT, PRIMARY KEY (site_id, link_id, resp_id) )')
cur.execute('CREATE TABLE IF NOT EXISTS Htmls \
		(site_id INTEGER NOT NULL, link_id INTEGER NOT NULL, resp_id INTEGER NOT NULL, \
		 count INTEGER, file TEXT, PRIMARY KEY (site_id, link_id, resp_id))')
		 
conn1 = sqlite3.connect('/home/nsarafij/project/OpenWPM/file_hashing/db2/fileHashing.sqlite')
cur1 = conn1.cursor()

cur1.execute('SELECT * FROM Images')

k=0
for row in cur1:
    k += 1
    cur.execute('''INSERT INTO Images (site_id, link_id, resp_id, count, file) VALUES (?,?,?,?,?)''', row)
    if (k % 100) == 0 :
        conn.commit()
        print k
    

cur1.execute('SELECT * FROM Htmls')

k=0
for row in cur1:
    k += 1
    cur.execute('''INSERT INTO Htmls (site_id, link_id, resp_id, count, file) VALUES (?,?,?,?,?)''',row)
    if (k % 100) == 0: 
        conn.commit()
        print row[0]
        

conn.close()
conn1.close()

        
