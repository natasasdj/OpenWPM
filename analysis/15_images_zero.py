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


fig_dir = '/home/nsarafij/project/OpenWPM/analysis/figs_10k/'
        
### content-length
(x,y) = ecdf_for_plot(zeroes['cont_length'])

plt.figure()
plt.step(x,y)
plt.ylabel('cdf')
plt.xlabel('content-length')
plt.grid(True)
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

(zeroes['cont_length']==zeroes['size']).sum()/float(zeroes.shape[0])


### domains all
# first-party domains (with subdomain)
(zeroes['site_id']==zeroes['resp_domain']).sum()/float(zeroes.shape[0])*100
#23.3%
# third-party domains (with subdomain) 
(zeroes['site_id']!=zeroes['resp_domain']).sum()/float(zeroes.shape[0])*100
#76.6%
zeroes.columns = ['respDom_id' if x=='resp_dom' else x for x in zeroes.columns]

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

query = 'SELECT * FROM DomainCompany'
df_domcom = pd.read_sql_query(query,conn)
zeroes=zeroes.merge(df_domcom, left_on = 'respDom_id', right_on = 'domain_id', how = 'left')
zeroes.drop('domain_id',inplace=True,axis=1)
zeroes.columns = ['respDomCompany_id' if x=='company_id' else x for x in zeroes.columns]

query = 'SELECT * FROM Companies'
df_com = pd.read_sql_query(query,conn)
zeroes=zeroes.merge(df_com, left_on = 'respDomCompany_id', right_on = 'id', how = 'left')
zeroes.drop('id',inplace=True,axis=1)
zeroes.rename('company':'respDom_company', inplace= True)
zeroes.columns = ['respDom_company' if x=='company' else x for x in zeroes.columns]
zeroes.columns = ['respDom_country' if x=='country' else x for x in zeroes.columns]

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


domcom = zeroes_.groupby(['domainTwoPart','company']).size().reset_index(name='count').sort('count',ascending=False)

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
plt.ylabel('percentage of the zero images')
plt.grid(True)
fig.savefig(fig_dir + 'zeroes_third-domains_perc_cum.png',format='png')
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
plt.ylabel('percentage of the zero images')
plt.grid(True)
fig.savefig(fig_dir + 'zeroes_third-domainsNo_perc_cum.png',format='png')
plt.show()

# third-party domain ranks and corresponding percentages of zero images

fig = plt.figure()
plt.plot(range(1,domains.size+1),dom_perc*100,marker='.')
plt.xscale('log')
plt.xlabel('domain rank')
plt.ylabel('percentage of the zero images')
plt.xlim([1,domains.size+1])
plt.grid(True)
fig.savefig(fig_dir + 'zeroes_third-domains_perc.png',format='png')
plt.show()


# top 20 third-party domains - percentages
n=20
x=np.arange(0.5,n)
fig = plt.figure()
plt.bar(x,dom_perc[0:n]*100,align='center')
plt.xlabel('domains')
plt.ylabel('percentage of zero images')
labels = list(domains.index[0:n])
plt.xticks(x, labels, rotation=80)
fig.tight_layout()
plt.grid(True)
fig.savefig(fig_dir + 'zeroes_third-domains_perc_top20.png',format='png')
plt.show()


companies = zeroes_['respDom_company'].value_counts()
total = zeroes_.shape[0]
companies_cum = companies.cumsum()
com_perc = companies/float(total)
com_perc_cum = com_perc.cumsum()


# third-party company ranks and corresponding percentages of zero images

fig = plt.figure()
plt.plot(range(1,companies.size+1),com_perc*100,marker='.')
#plt.xscale('log')
plt.xlabel('company rank')
plt.ylabel('percentage of the zero images')
plt.xlim([1,companies.size+1])
plt.grid(True)
fig.savefig(fig_dir + 'zeroes_third-domainCompanies_perc.png',format='png')
plt.show()

# top 20 third-party companies - percentages
n=20
x=np.arange(0.5,n)
fig = plt.figure()
plt.bar(x,com_perc[0:n]*100,align='center')
plt.xlabel('companies')
plt.ylabel('percentage of zero images')
labels = list(companies.index[0:n])
plt.xticks(x, labels, rotation=80)
fig.tight_layout()
plt.grid(True)
fig.savefig(fig_dir + 'zeroes_third-domainCompanies_perc_top20.png',format='png')
plt.show()

# table in latex

# None company

zeroes_.loc[zeroes_['respDom_id2']==4][['respDom_id2','respDom_domain2']]

### put this into results as well
zeroes_['respDomCompany_id'].isnull().sum()/float(zeroes_.shape[0])
# 2.6%



### type of zero images

zeroes.loc[zeroes['type']==zeroes['cont_type']]
(zeroes['type']==zeroes['cont_type']).sum()
# 0 

zeroes.groupby('type').size()
zeroes.groupby('cont_type').size()

zeroes








