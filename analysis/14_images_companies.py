import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF
from matplotlib.ticker import FuncFormatter
import numpy as np

def thousands(x, pos):
    if x>=1e9:
        return '%.1fB' % (x*1e-9)
    elif x>=1e6:
        return '%.1fM' % (x*1e-6)
    elif x>=1e3:
        return '%.1fK' % (x*1e-3)
    else:
        return x

formatter = FuncFormatter(thousands)


###### third-party domains
res_dir = '/home/nsarafij/project/OpenWPM/analysis/results/'
db = res_dir + 'images.sqlite'
conn = sqlite3.connect(db)
query = 'SELECT * FROM Images where site_id!=resp_domain'
df = pd.read_sql_query(query,conn)
query = 'SELECT * FROM Domains'
df_dom = pd.read_sql_query(query,conn)
query = 'SELECT * FROM Companies'
df_comp = pd.read_sql_query(query,conn)
query = 'SELECT * FROM DomainCompany'
df_domComp = pd.read_sql_query(query,conn)
dfCompId=df.merge(df_domComp,left_on='resp_domain',right_on='domain_id',how='left')
dfComp=dfCompId.merge(df_comp,left_on='company_id',right_on='id',how='left')

companies = dfComp['company'].value_counts(dropna=False)
companies_perc = companies/float(df.shape[0])
dfComp_pix1 = dfComp.ix[dfComp['pixels']==1]
companies_pix1 = dfComp_pix1['company'].value_counts(dropna=False)
companies_pix1_perc = companies_pix1/float(dfComp_pix1.shape[0])

# all images: counts per each response domain
domains = df['resp_domain'].value_counts()
total = df.shape[0]
domains_cum = domains.cumsum()
dom_perc = domains/float(total)
dom_perc_cum = dom_perc.cumsum()
domains_=pd.merge(pd.DataFrame(domains), df_dom, left_index=True, right_on='id')
domains_=pd.merge(pd.DataFrame(domains_), df_domComp, left_on='id', right_on='domain_id',how='left')
domains_=pd.merge(pd.DataFrame(domains_), df_comp, left_on='company_id', right_on='id',how='left')

# 1-pixel images: counts per each response domain
dom_pix1 = df.ix[df['pixels']==1]['resp_domain'].value_counts()
dom_pix1_cum = dom_pix1.cumsum()
dom_pix1_perc = dom_pix1/float(df.shape[0])
dom_pix1_perc_ = dom_pix1/float(dom_pix1_cum[dom_pix1_cum.size-1:dom_pix1_cum.size])
dom_pix1_perc_cum = dom_pix1_perc_.cumsum()
dom_pix1_=pd.merge(pd.DataFrame(dom_pix1), df_dom, left_index=True, right_on='id')
dom_pix1_=pd.merge(pd.DataFrame(dom_pix1_), df_domComp, left_on='id', right_on='domain_id',how='left')
dom_pix1_=pd.merge(pd.DataFrame(dom_pix1_), df_comp, left_on='company_id', right_on='id',how='left')

# all images: top 20 domains - companies, percentages
n=20
x=np.arange(0.5,n)
fig = plt.figure()
plt.bar(x,dom_perc[0:n]*100,align='center')
plt.xlabel('company')
plt.ylabel('percentage of total number of third-party images')
labels = list(domains_['company'][0:n])
plt.xticks(x, labels, rotation=80)
plt.grid(True)
plt.title('All third-party images')
fig.tight_layout()
fig.savefig(fig_dir + 'third-domain_company_perc_top20.png',format='png')



# 1-pixel images: top 20 domains - companies, percentage
n=20
x=np.arange(0.5,n)
fig = plt.figure()
plt.bar(x,dom_pix1_perc[0:n]*100,align='center')
plt.xlabel('company')
plt.ylabel('percentage of 1-pixel third-party images')
labels = list(dom_pix1_['company'][0:n])
plt.xticks(x, labels, rotation=80)
plt.title('1-pixel images')
plt.grid(True)
fig.tight_layout()
fig.savefig(fig_dir + 'third-domain_company_pix1_perc_top20.png',format='png')

# percentage of companies that owns third-party domains from which images come
n=20
x=np.arange(0.5,n)
fig = plt.figure()
plt.bar(x,companies_perc[0:n]*100,align='center')
labels = list(companies_perc.index[0:n])
print labels
plt.xticks(x, labels, rotation=80)              
plt.grid(True)
plt.show()

# percentage of companies that owns third-party domains from which 1-pixel images come
n=20
x=np.arange(0.5,n)
fig = plt.figure()
plt.bar(x,companies_pix1_perc[0:n]*100,align='center')
labels = list(companies_perc.index[0:n])
print labels
plt.xticks(x, labels, rotation=80)
plt.grid(True)
plt.show()




