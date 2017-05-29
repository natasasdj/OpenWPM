import sqlite3
import os
import time
#import socket
import pandas as pd
import pythonwhois as pywhois
import signal
import re

def handler(signum, frame):
    print "Forever is over!"
    raise Exception("end of time")
        
signal.signal(signal.SIGALRM, handler)

def get_company(domain):
    company = None
    country = None      
    try:
        
        signal.alarm(10)
        w=pywhois.get_whois(domain)
        signal.alarm(0)
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
        if (company is not None) and (country is None):
            if 'country' in w['contacts']['admin']: country = w['contacts']['admin']['country']
            elif 'country' in w['contacts']['tech']: country = w['contacts']['tech']['country'] 
            elif 'country' in w['contacts']['registrant']: country = w['contacts']['registrant']['country']   
    except Exception as e:
        print "Exception: ", e 
    return (company,country)      



    
res_dir = '/home/nsarafij/project/OpenWPM/analysis/results/'
db = os.path.join(res_dir,'imagesFirst.sqlite')
filename=os.path.join(res_dir,'third-domains2_owners')

fhand=open(filename)
#with open(filename) as fhand:

print db
#with sqlite3.connect(db) as conn:
conn = sqlite3.connect(db)
cur = conn.cursor()
#cur.execute('DROP TABLE IF EXISTS Companies')
#cur.execute('DROP TABLE IF EXISTS Domain2Company')
cur.execute('CREATE TABLE IF NOT EXISTS Companies (id INTEGER PRIMARY KEY AUTOINCREMENT, company TEXT UNIQUE, country CHARACTER(2))')
cur.execute('CREATE TABLE IF NOT EXISTS Domain2Company (domainTwoPart_id INTEGER, company_id INTEGER, \
            FOREIGN KEY (domainTwoPart_id) REFERENCES DomainsTwoPart(id), FOREIGN KEY (company_id) REFERENCES Companies(id))')

cur.execute('SELECT count(domainTwoPart_id) FROM Domain2Company')
last_id = cur.fetchone()[0]
print last_id



#max_id = 2000
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
    domain_id = splits[0]; domain = splits[1]; count = splits[2]
    if count == 1: break
    print "***** ***** i: ", i, " domain_id: ", domain_id, " domain: ", domain
    domain_parts = domain.split('.')
    for i in range(0, len(domain_parts)-1):
        sliced_domain = '.'.join(domain_parts[i:])
        company,country = get_company(sliced_domain)
        if company is not None: break 
    if company is None: 
        company = 'None'
        country = None
    elif 'Google' in company: 
        company = 'Google Inc.'
        country = 'US'
    print "Company: ", company, " Country: ", country
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
    time.sleep(1)

conn.commit()
conn.close()
fhand.close()


# do once again the domain_id for which company = None, i.e., company_id = 4

conn = sqlite3.connect(db)
cur = conn.cursor()

query='SELECT domainTwoPart_id FROM Domain2Company where company_id=4'
d1=pd.read_sql_query(query,conn)
query='SELECT * FROM DomainsTwoPart'
d2=pd.read_sql_query(query,conn)
domains=d1.merge(d2,left_on = 'domainTwoPart_id',right_on='id',how='left')
domains.drop('id', axis=1, inplace=True)
print domains.shape[0]
i=0
#start_id = 357
for index, row in domains.iterrows():
    domain_id=row['domainTwoPart_id']; domain = row['domainTwoPart']
    i+=1; 
    #if i < start_id: continue
    print "***** ***** i: ", i, " domain_id: ", domain_id, " domain: ", domain
    if i % 100 == 0: 
        #time.sleep(30)
        conn.commit()
    #if i>30: break
    time.sleep(1)
    domain_parts = domain.split('.')
    for k in range(0, len(domain_parts)-1):
        sliced_domain = '.'.join(domain_parts[k:])
        company,country = get_company(sliced_domain)
        if company is not None: break   
    if company is None: continue
    if 'Google' in company: company = 'Google Inc.'
    print "Company: ", company, " Country: ", country
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
   
    

conn.commit()
conn.close()




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
        
        
