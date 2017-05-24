import sqlite3
import os
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
        return get_tld('http://'+domain)
    except:
        return domain

res_dir = '/home/nsarafij/project/OpenWPM/analysis/results/'
db = os.path.join(res_dir,'imagesFirst.sqlite')
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS DomainsTwoPart')
cur.execute('DROP TABLE IF EXISTS Domain_DomainTwoPart')
cur.execute('CREATE TABLE IF NOT EXISTS DomainsTwoPart (id INTEGER PRIMARY KEY AUTOINCREMENT, domainTwoPart TEXT UNIQUE)')
cur.execute('CREATE TABLE IF NOT EXISTS Domain_DomainTwoPart (domain_id INTEGER, domainTwoPart_id INTEGER, \
            FOREIGN KEY (domain_id) REFERENCES Domains(id), FOREIGN KEY (domainTwoPart_id) REFERENCES DomainsTwoPart(id))')
            
cur.execute('SELECT * FROM Domains')
domains=cur.fetchall()
i = 0
for row in domains:    
    i+=1
    #if i>10: break
    domain_id = row[0]; domain = row[1]
    domainTwoPart = domain2(domain)
    print domain_id, domain, domainTwoPart
    cur.execute('SELECT id FROM DomainsTwoPart WHERE domainTwoPart = ?',(domainTwoPart,))       
    data=cur.fetchone()
    if data is not None: 
        domainTwoPart_id=data[0]       
    else:
        cur.execute('INSERT INTO DomainsTwoPart (domainTwoPart) VALUES (?)',(domainTwoPart,))
        domainTwoPart_id = cur.lastrowid
    cur.execute('INSERT INTO Domain_DomainTwoPart (domain_id,domainTwoPart_id) VALUES (?,?)',(domain_id,domainTwoPart_id))
    if i % 100 == 0: conn.commit()


conn.commit()
conn.close()
 



