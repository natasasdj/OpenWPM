import os
import sqlite3
import pandas as pd
import numpy as np
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from statsmodels.distributions.empirical_distribution import ECDF

def thousands(x, pos):
    if x>=1e9:
        return '%dB' % (x*1e-9)
    elif x>=1e6:
        return '%dM' % (x*1e-6)
    elif x>=1e3:
        return '%dK' % (x*1e-3)
    else:
        return x

formatter = FuncFormatter(thousands)


def ecdf_for_plot(sample):
    #x = np.linspace(min(sample), max(sample))
    print "sample: ",type(sample)
    x = sample.sort_values(ascending = False)
    ecdf = ECDF(x)
    # print ecdf
    print "ecdf: ",type(ecdf)
    y = ecdf(x)
    #print y
    print "y: ", type(y)
    return (x,y)    
    

res_dir = '/home/nsarafij/project/OpenWPM/analysis/results/'
db = res_dir + 'images.sqlite'
conn = sqlite3.connect(db)
query = 'SELECT * FROM Images'
df = pd.read_sql_query(query,conn)
zeroes = df.ix[df['size']==0]

zeroes.shape[0]#2693959
df.shape[0]#31861758
zeroes.shape[0]/float(df.shape[0])#0.0845


fig_dir = '/home/nsarafij/project/OpenWPM/analysis/figs_10k_domains/'
        
### content-length
(x,y) = ecdf_for_plot(zeroes['cont_length'])

fig, ax = plt.subplots()
plt.step(x,y)
plt.ylabel('cdf')
plt.xlabel('content-length')
plt.grid(True)
ax.xaxis.set_major_formatter(formatter)
plt.savefig(os.path.join(fig_dir,'zeroes_cont_length_cdf.png'))
plt.show()

plt.figure()
plt.step(x,y)
plt.ylabel('cdf')
plt.xlabel('content-length')
plt.grid(True)
plt.xscale('symlog')
plt.savefig(os.path.join(fig_dir,'zeroes_cont_length_cdf_log.png'))
plt.show()

(zeroes['cont_length']==zeroes['size']).sum()/float(zeroes.shape[0]) #0.15947532980271786


### domains all
# first-party domains (with subdomain)
(zeroes['site_id']==zeroes['resp_domain']).sum()/float(zeroes.shape[0])*100
#23.3%
# third-party domains (with subdomain) 
(zeroes['site_id']!=zeroes['resp_domain']).sum()/float(zeroes.shape[0])*100
#76.6%

zeroes.columns = ['respDom_id' if x=='resp_domain' else x for x in zeroes.columns]

query = 'SELECT * FROM Domain_DomainTwoPart'
df_domdom2 = pd.read_sql_query(query,conn)
zeroes=zeroes.merge(df_domdom2, left_on = 'site_id', right_on = 'domain_id', how = 'left')
zeroes.drop('domain_id',inplace=True,axis=1)
zeroes.columns = ['site_id2' if x=='domainTwoPart_id' else x for x in zeroes.columns]
zeroes=zeroes.merge(df_domdom2, left_on = 'respDom_id', right_on = 'domain_id', how = 'left')
zeroes.drop('domain_id',inplace=True,axis=1)
zeroes.columns = ['respDom_id2' if x=='domainTwoPart_id' else x for x in zeroes.columns]

query = 'SELECT * FROM DomainsTwoPart'
df_dom2 = pd.read_sql_query(query,conn)
zeroes=zeroes.merge(df_dom2, left_on = 'site_id2', right_on = 'id', how = 'left')
zeroes.drop('id',inplace=True,axis=1)
zeroes.columns = ['site_domain2' if x=='domainTwoPart' else x for x in zeroes.columns]
zeroes=zeroes.merge(df_dom2, left_on = 'respDom_id2', right_on = 'id', how = 'left')
zeroes.drop('id',inplace=True,axis=1)
zeroes.columns = ['respDom_domain2' if x=='domainTwoPart' else x for x in zeroes.columns]

query = 'SELECT * FROM Domain2Company'
df_dom2com = pd.read_sql_query(query,conn)
zeroes=zeroes.merge(df_dom2com, left_on = 'respDom_id2', right_on = 'domainTwoPart_id', how = 'left')
zeroes.drop('domainTwoPart_id',inplace=True,axis=1)

query = 'SELECT * FROM Companies'
df_com = pd.read_sql_query(query,conn)
zeroes=zeroes.merge(df_com, left_on = 'company_id', right_on = 'id', how = 'left')
zeroes.drop('id',inplace=True,axis=1)



### domains all
# first-party domains 2  (without subdomain)
(zeroes['site_id2']==zeroes['respDom_id2']).sum()/float(zeroes.shape[0])*100
# 43%
# third-party domains 2 (without subdomain)
(zeroes['site_id2']!=zeroes['respDom_id2']).sum()/float(zeroes.shape[0])*100
# 56%


#zeroes['domain2']=zeroes['domain'].map(twoPart_domain)

### third-party domains    
zeroes_ = zeroes.loc[zeroes['site_id2']!=zeroes['respDom_id2']]

domains = zeroes_['respDom_domain2'].value_counts()
total = zeroes_.shape[0]
domains_cum = domains.cumsum()
dom_perc = domains/float(total)
dom_perc_cum = dom_perc.cumsum()




# cdf of number of zero images per third-party domains

(x,y) = ecdf_for_plot(domains)
plt.figure()
plt.step(x,y)
plt.ylabel('cdf')
plt.xlabel('no of zero images per domain')
plt.grid(True)
plt.xscale('log')
plt.savefig(os.path.join(fig_dir,'zeroes_third-domains_cdf.png'))
plt.show()

# cumulative percentages per domain rank
fig = plt.figure()
plt.plot(range(1,dom_perc_cum.size+1),dom_perc_cum*100,marker='.')
plt.xscale('log')
plt.title('Cumulative Percentage Counts')
plt.xlabel('domain rank')
plt.ylabel('percentage of zero images')
plt.grid(True)
fig.savefig(fig_dir + 'zeroes_third-domain2_perc_cum.png',format='png')
plt.show()

# cumulative percentages per number of zero images coming from a domain

domains_counts = domains.value_counts().sort_index()
domains_counts_cum = domains_counts.multiply(domains_counts.index).cumsum()
domains_perc_cum=domains_counts_cum/float(domains_counts_cum.iloc[-1])

fig = plt.figure()
plt.plot(domains_perc_cum.index,domains_perc_cum*100,marker='.')
plt.xscale('log')
plt.title('Cumulative Percentages')
plt.xlabel('number of zero images coming from a domain')
plt.ylabel('percentage of zero images')
plt.grid(True)
fig.savefig(fig_dir + 'zeroes_third-domain2No_perc_cum.png',format='png')
plt.show()

# third-party domain ranks and corresponding percentages of zero images

fig = plt.figure()
plt.plot(range(1,domains.size+1),dom_perc*100,marker='.')
plt.xscale('log')
plt.xlabel('domain rank')
plt.ylabel('percentage of zero images')
plt.xlim([1,domains.size+1])
plt.grid(True)
fig.savefig(fig_dir + 'zeroes_third-domain2_perc.png',format='png')
plt.show()



# top 30 third-party domains - percentages
n=30
x=np.arange(0.5,n)
fig = plt.figure()
plt.bar(x,dom_perc[0:n]*100,align='center')
plt.xlabel('domains')
plt.ylabel('percentage of zero images')
labels = list(domains.index[0:n])
plt.xticks(x, labels, rotation=80)
fig.tight_layout()
plt.grid(True)
fig.savefig(fig_dir + 'zeroes_third-domain2_perc_top30.png',format='png')
plt.show()

### table domains - companies
domcom = zeroes_[['respDom_domain2','company']].groupby(['respDom_domain2','company']).size().reset_index(name='img_perc').sort_values('img_perc',ascending=False)
domcom['img_perc']=domcom['img_perc']/float(zeroes_.shape[0])*100
table_dir = '/home/nsarafij/project/OpenWPM/analysis/tables_10k'
fhand = open(os.path.join(table_dir,'third-domain2company_zero_perc_top30.txt'),'w+')

for i in range(0,n):
    dom = domcom.iloc[i,0]
    comp =  domcom.iloc[i,1]
    perc = domcom.iloc[i,2]
    s = str(i+1) + ' & ' + dom  +  ' & ' + comp + ' & ' + '%.2f' % perc + '\\\\ \\hline'
    #print s
    s = s.encode('UTF-8')
    print s
    fhand.write(s + '\n')  
           
fhand.close()

### companies

companies = zeroes_['company'].value_counts()
total = zeroes_.shape[0]
companies_cum = companies.cumsum()
com_perc = companies/float(total)
com_perc_cum = com_perc.cumsum()

companies.size #854

# third-party company ranks and corresponding percentages of zero images

fig = plt.figure()
plt.plot(range(1,companies.size+1),com_perc*100,marker='.')
plt.xscale('log')
plt.xlabel('company rank')
plt.ylabel('percentage of zero images')
plt.xlim([1,companies.size+1])
plt.grid(True)
fig.savefig(fig_dir + 'third-company_zero_perc.png',format='png')
plt.show()

#cumulative

fig = plt.figure()
plt.plot(range(1,com_perc_cum.size+1),com_perc_cum*100,marker='.')
plt.xscale('log')
#plt.title('Cumulative Percentages')
plt.xlabel('domain rank')
plt.ylabel('percentage of zero images')
plt.grid(True)
fig.savefig(fig_dir + 'third-company_zero_perc_cum.png',format='png')
plt.show()


# top 30 third-party companies - percentages
n=30
x=np.arange(0.5,n)
fig = plt.figure()
plt.bar(x,com_perc[0:n]*100,align='center')
plt.xlabel('companies')
plt.ylabel('percentage of zero images')
labels = list(companies.index[0:n])
plt.xticks(x, labels, rotation=90)
fig.tight_layout()
plt.grid(True)
fig.savefig(fig_dir + 'third-company_zero_perc_top30.png',format='png')
plt.show()

### table: top 30 companies
table_dir = '/home/nsarafij/project/OpenWPM/analysis/tables_10k'
fhand = open(os.path.join(table_dir,'third-company_zero_perc_top30.txt'),'w+')

for i in range(0,n):
    com = com_perc.index[i]
    perc = com_perc[i]*100
    s = str(i+1) +  ' & ' + com + ' & ' + '%.3f' % perc + '\\\\ \\hline'
    print s
    s = s.encode('UTF-8')
    print s
    fhand.write(s + '\n')      
       
fhand.close()


# table in latex

# None company

zeroes_.loc[zeroes_['company_id']==4].shape[0]/float(zeroes_.shape[0])
# 0.03896522119492128
### put this into results as well
zeroes_['company'].isnull().sum()/float(zeroes_.shape[0])
# 0.00049804140653672828




### type of zero images

zeroes.loc[zeroes['type']==zeroes['cont_type']]
(zeroes['type']==zeroes['cont_type']).sum()
# 0 

zeroes.groupby('type').size()
zeroes.groupby('cont_type').size()

zeroes








