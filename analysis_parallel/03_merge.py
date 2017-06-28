db1=sys.argv[1]
db2=sys.argv[2]

conn1 = sqlite3.connect(db1)
cur1 = conn1.cursor()
conn2 = sqlite3.connect(db2)
cur2 = conn2.cursor()

k=0
for row in cur2:
    print row
    cur1.execute('INSERT INTO Images (site_id, link_id, resp_id, resp_domain, size, cont_length, type, cont_type, pixels) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)',row)
    k += 1
    if k>10:break
    if k % 1000 == 0:
        print k
        conn1.commit()
conn1.commit()

    
    



