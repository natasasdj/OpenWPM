import sqlite3
import os

import time
import socket
import pythonwhois as pywhois

def findAll(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]
    
    
res_dir = '/home/nsarafij/project/OpenWPM/analysis/results/'
filename=os.path.join(res_dir,'domains_owners')

fhand=open(filename)
#with open(filename) as fhand:
db = os.path.join(res_dir,'imagesFirst.sqlite')
print db
#with sqlite3.connect(db) as conn:
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Companies')
cur.execute('DROP TABLE IF EXISTS DomainCompany')
cur.execute('CREATE TABLE IF NOT EXISTS Companies (id INTEGER PRIMARY KEY AUTOINCREMENT, company TEXT UNIQUE, country CHARACTER(2))')
cur.execute('CREATE TABLE IF NOT EXISTS Domain2Company (domainTwoPart_id INTEGER, company_id INTEGER, \
            FOREIGN KEY (domainTwoPart_id) REFERENCES DomainsTwoPart(id), FOREIGN KEY (company_id) REFERENCES Companies(id))')
            
            
cur.execute('SELECT count(domain_id) FROM DomainCompany')
last_id = cur.fetchone()[0]
print last_id
#max_id = 20
firstLine = True
i=0
for line in fhand:
    if firstLine:
        firstLine = False 
        continue
    i+=1; print i
    #if i>max_id: break
    if i<=last_id: continue
    splits = line.rstrip().split(",")
    count = splits[0]; domain = splits[1]; domain_id = splits[2]
    if count == 1: break
    company = None
    country = None       
    while True:
        try:
            w=pywhois.get_whois(domain)
            try:
                company = w['contacts']['tech']['organization']
                country = w['contacts']['tech']['country']
                break
            except:
                points = findAll(domain,'.')
                no_points = len(points)
                if no_points<2: break
                point = points[0]
                domain = domain[point+1:]      
        except Exception as e:
            print "Exception: ", e
            break   
    time.sleep(5)
    if company is None: company = 'None'
    cur.execute('SELECT id FROM Companies WHERE company = ?',(company,))       
    data=cur.fetchone()
    if data is not None: 
        company_id=data[0]
        cur.execute('INSERT INTO DomainCompany (domain_id,company_id) VALUES (?,?)',(domain_id,company_id))
    else:
        cur.execute('INSERT INTO Companies (company,country) VALUES (?,?)',(company,country))
        company_id = cur.lastrowid
        cur.execute('INSERT INTO DomainCompany (domain_id,company_id) VALUES (?,?)',(domain_id,company_id))
    if i % 100 == 0: conn.commit()
    
 
    
conn.commit()
conn.close()
fhand.close()


'''
import whois
import socket
domain = 'hm.baidu.com'
while True:
    print domain
    try:
        print 1
        w=whois.whois(domain)
    except whois.parser.PywhoisError:
        print 2
        points = findAll(domain,'.')
        no_points = len(points)
        print 'no_points:',no_points
        if no_points<2: break
        point = points[0]
        domain = domain[point+1:]
    except socket.error:
        print 3
        w={}
        break

with open(filename) as fhand:
    db = os.path.join(res_dir,'images.sqlite')    	
    conn = sqlite3.connect(db)
    with conn:
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS Companies')
        cur.execute('DROP TABLE IF EXISTS DomainCompany')
        cur.execute('CREATE TABLE IF NOT EXISTS Companies (id INTEGER PRIMARY KEY AUTOINCREMENT, company TEXT UNIQUE, country CHARACTER(2))')
        cur.execute('CREATE TABLE IF NOT EXISTS DomainCompany (domain_id INTEGER, company_id INTEGER, \
                    FOREIGN KEY (domain_id) REFERENCES Domains(id), FOREIGN KEY (company_id) REFERENCES Companies(id))')
        firstLine = True
        for line in fhand:
            if firstLine:
                firstLine = False 
                continue
            splits = line.split(",")
            if len(splits)<4: continue
            domain_id = splits[2]
            company = splits[3].split(' - ')[-1]
            country = splits[4]
            print company
            cur.execute('SELECT id FROM Companies WHERE company = ?',(company,))
            data=cur.fetchone()
            if data is not None: 
                company_id=data[0]
                print company_id
                cur.execute('INSERT INTO DomainCompany (domain_id,company_id) VALUES (?,?)',(domain_id,company_id))
                continue
            else:
                print company, country
                cur.execute('INSERT INTO Companies (company,country) VALUES (?,?)',(company,country))
                company_id = cur.lastrowid
                cur.execute('INSERT INTO DomainCompany (domain_id,company_id) VALUES (?,?)',(domain_id,company_id))
'''
        
        
