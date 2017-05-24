import sqlite3
import os

import time
#import socket
import pandas as pd
import pythonwhois as pywhois

    
res_dir = '/home/nsarafij/project/OpenWPM/analysis/results/'
filename=os.path.join(res_dir,'third-domains2_owners')

fhand=open(filename)
#with open(filename) as fhand:
db = os.path.join(res_dir,'imagesFirst.sqlite')
print db
#with sqlite3.connect(db) as conn:
conn = sqlite3.connect(db)
cur = conn.cursor()
#cur.execute('DROP TABLE IF EXISTS Companies')
#cur.execute('DROP TABLE IF EXISTS Domain2Company')
cur.execute('CREATE TABLE IF NOT EXISTS Companies (id INTEGER PRIMARY KEY AUTOINCREMENT, company TEXT UNIQUE, country CHARACTER(2))')
cur.execute('CREATE TABLE IF NOT EXISTS Domain2Company (domainTwoPart_id INTEGER, company_id INTEGER, \
            FOREIGN KEY (domainTwoPart_id) REFERENCES DomainsTwoPart(id), FOREIGN KEY (company_id) REFERENCES Companies(id))')
            
            


# do once again the domain_id for which company = None, i.e., company_id = 4

query='SELECT domainTwoPart_id FROM Domain2Company where company_id=4'
d1=pd.read_sql_query(query,conn)
query='SELECT * FROM DomainsTwoPart'
d2=pd.read_sql_query(query,conn)
domains=d1.merge(d2,left_on = 'domainTwoPart_id',right_on='id',how='left')
domains.drop('id', axis=1, inplace=True)
print domains.shape[0]


i=0
for index, row in domains.iterrows():
    domain_id=row['domainTwoPart_id']; domain = row['domainTwoPart']
    i+=1; 
    print i, domain_id, domain
    if i % 100 == 0: 
        time.sleep(30)
        conn.commit()
    #if i>30: break
    time.sleep(5)
    company = None
    country = None       
    try:
        w=pywhois.get_whois(domain)
        print "i: ", i, " domain_id: ", domain_id, " domain: ", domain
        if (w['contacts']['admin'] is not None) and ('organization' in w['contacts']['admin']): 
            company = w['contacts']['admin']['organization']
            if 'country' in w['contacts']['admin']: country = w['contacts']['admin']['country']
        elif (w['contacts']['tech'] is not None) and ('organization' in w['contacts']['tech']): 
            company = w['contacts']['tech']['organization']
            if 'country' in w['contacts']['tech']: country = w['contacts']['tech']['country']
        elif (w['contacts']['admin'] is not None) and ('name' in w['contacts']['admin']): 
            company = w['contacts']['admin']['name']
            if 'country' in w['contacts']['admin']: country = w['contacts']['admin']['country']
        elif (w['contacts']['tech'] is not None) and ('name' in w['contacts']['tech']): 
            company = w['contacts']['tech']['name']
            if 'country' in w['contacts']['tech']: country = w['contacts']['tech']['country']   
        elif (w['contacts']['registrant'] is not None) and ('organization' in w['contacts']['registrant']): 
            company = w['contacts']['registrant']['organization']
            if 'country' in w['contacts']['registrant']: country = w['contacts']['registrant']['country']
        elif (w['contacts']['registrant'] is not None) and ('name' in w['contacts']['registrant']): 
            company = w['contacts']['registrant']['name'] 
            if 'country' in w['contacts']['registrant']: country = w['contacts']['registrant']['country']
        elif re.search('Registrant Organization: (.+)?\n',w['raw'][0]):
            company = re.search('Registrant Organization: (.+)?\n',w['raw'][0]).group(1)
        elif re.search('Registrant Name: (.+)?\n',w['raw'][0]):
            company = re.search('Registrant Organization: (.+)?\n',w['raw'][0]).group(1)
        if (country is not None) and (company is None):
            if 'country' in w['contacts']['admin']: country = w['contacts']['admin']['country']
            elif 'country' in w['contacts']['tech']: country = w['contacts']['tech']['country'] 
            elif 'country' in w['contacts']['registrant']: country = w['contacts']['registrant']['country']               
        print "********** Company: ", company, " Country: ", country
    except Exception as e:
        print "Exception: ", e     
    if company is None: continue
    if 'Google' in company: company = 'Google Inc.'
    cur.execute('SELECT id FROM Companies WHERE company = ?',(company,))       
    data=cur.fetchone()
    if data is not None: 
        company_id=data[0]
        cur.execute('UPDATE Domain2Company  SET company_id = ? WHERE  domainTwoPart_id = ?',(company_id,domain_id))
        print "update Domain2Company: ",company_id,domain_id
    else:
        cur.execute('INSERT INTO Companies (company,country) VALUES (?,?)',(company,country))
        print "insert into  Domain2Company: ",company_id, domain_id
        company_id = cur.lastrowid
        cur.execute('UPDATE Domain2Company SET company_id = ? WHERE  domainTwoPart_id = ?',(company_id,domain_id))
        print "update Domain2Company: ", company_id, domain_id
   

cur.execute('SELECT count(domainTwoPart_id) FROM Domain2Company')
last_id = cur.fetchone()[0]
print last_id

max_id = 2000
firstLine = True
i=0
for line in fhand:
    if firstLine:
        firstLine = False 
        continue
    i+=1; print i
    if i>max_id: break
    if i<=last_id: continue
    splits = line.rstrip().split(",")
    domain_id = splits[0]; domain = splits[1]; count = splits[2]
    company = None
    country = None       
    try:
        w=pywhois.get_whois(domain)
        company = w['contacts']['admin']['organization']
        country = w['contacts']['admin']['country']
    except Exception as e:
            print "Exception: ", e     
    if company is None: 
        company = 'None'
        country = None
    cur.execute('SELECT id FROM Companies WHERE company = ?',(company,))       
    data=cur.fetchone()
    if data is not None: 
        company_id=data[0]
        cur.execute('INSERT INTO Domain2Company (domainTwoPart_id,company_id) VALUES (?,?)',(domain_id,company_id))
    else:
        cur.execute('INSERT INTO Companies (company,country) VALUES (?,?)',(company,country))
        company_id = cur.lastrowid
        cur.execute('INSERT INTO Domain2Company (domainTwoPart_id,company_id) VALUES (?,?)',(domain_id,company_id))
    if i % 100 == 0: conn.commit()
    time.sleep(6)

conn.commit()
conn.close()
fhand.close()
    
#conn = sqlite3.connect(db)
query='SELECT domainTwoPart_id FROM Domain2Company where company_id=4'
d1=pd.read_sql_query(query,conn)
query='SELECT * FROM DomainsTwoPart'
d2=pd.read_sql_query(query,conn)
domains=d1.merge(d2,left_on = 'domainTwoPart_id',right_on='id',how='left')
domains.drop('id', axis=1, inplace=True)

j=0
for index,row in domains.iterrows():
    j += 1
    print row['domainTwoPart_id'], row['domainTwoPart']
    if j>10: break
    





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
        
        
