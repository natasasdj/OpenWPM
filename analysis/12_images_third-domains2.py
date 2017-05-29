import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF
from matplotlib.ticker import FuncFormatter

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
df.columns = ['respDom_id' if x=='resp_domain' else x for x in df.columns]

query = 'SELECT * FROM Domain_DomainTwoPart'
df_domdom2 = pd.read_sql_query(query,conn)
df=df.merge(df_domdom2,left_on='site_id',right_on='domain_id',how='left')
df.drop('domain_id',axis=1,inplace=True)
df.columns = ['site_id2' if x=='domainTwoPart_id' else x for x in df.columns]
df=df.merge(df_domdom2,left_on='respDom_id',right_on='domain_id',how='left')
df.drop('domain_id',axis=1,inplace=True)
df.columns = ['respDom_id2' if x=='domainTwoPart_id' else x for x in df.columns]

query = 'SELECT * FROM DomainsTwoPart'
df_dom2 = pd.read_sql_query(query,conn)
df=df.merge(df_dom2, left_on = 'site_id2', right_on = 'id', how = 'left')
df.drop('id',inplace=True,axis=1)
df.columns = ['site_domain2' if x=='domainTwoPart' else x for x in df.columns]
df=df.merge(df_dom2, left_on = 'respDom_id2', right_on = 'id', how = 'left')
df.drop('id',inplace=True,axis=1)
df.columns = ['respDom_domain2' if x=='domainTwoPart' else x for x in df.columns]

query = 'SELECT * FROM Domain2Company'
df_dom2com = pd.read_sql_query(query,conn)
df=df.merge(df_dom2com,left_on='respDom_id2',right_on='domainTwoPart_id',how='left')
df.drop('domainTwoPart_id',axis=1,inplace=True)

query = 'SELECT * FROM Companies'
df_com = pd.read_sql_query(query,conn)
df=df.merge(df_com,left_on='company_id',right_on='id',how='left')
df.drop('id',axis=1,inplace=True)


conn.close()

df1=df.loc[df['site_id2']==df['respDom_id2']]
df2=df.loc[df['site_id2']!=df['respDom_id2']]
df2.shape[0]/float(df.shape[0]) #0.6757349672921374


# how many sites and links have third-party images
sites = []
links = 0 
for site_id in range(1,10001):
    if site_id % 100 == 0: print site_id
    df3=df2.loc[df2['site_id']==site_id]
    df3_size = df3['link_id'].unique().shape[0]
    links += df3_size
    if df3_size: sites.append(site_id)
    
len(sites) #8343
8343/8965 = 0.9306190741773563
links #912363
912363/964315.

# distinct response domains
df['respDom_id2'].unique(().size #29009
df1['respDom_id2'].unique(().size #7863
df2['respDom_id2'].unique(().size #23235


domains2 = df2[['respDom_id2','respDom_domain2']].groupby(['respDom_id2','respDom_domain2']).size().sort_values(ascending = False).reset_index()
domains2.to_csv('/home/nsarafij/project/OpenWPM/analysis/results/third-domains2_owners',index=False,encoding='utf-8')

# companies



############## considering third-party domains only

# all images: counts per each response domain
domains = df2['respDom_domain2'].value_counts()
total = df2.shape[0]
domains_cum = domains.cumsum()
dom_perc = domains/float(total)
dom_perc_cum = dom_perc.cumsum()

# all images: counts per each company
com = df2['company'].value_counts()
com_cum = com.cumsum()
com_perc = com/df2.shape[0]
com_perc_cum = com_perc.cumsum()

# all images - response domains

fig_dir = '/home/nsarafij/project/OpenWPM/analysis/figs_10k_domains/'

# cdf of number of third-party images per third-party domains

(x,y) = ecdf_for_plot(domains)
plt.figure()
plt.step(x,y)
plt.ylabel('cdf')
plt.xlabel('no of zero images per domain')
plt.grid(True)
plt.xscale('symlog')
plt.savefig(os.path.join(fig_dir,'third-domains2_cdf.png'))
plt.show()

# counts
fig, ax = plt.subplots()
plt.plot(range(1,domains.shape[0]+1),domains,marker='.')
plt.xscale('log')
plt.xlabel('domain rank')
plt.ylabel('count of images')
plt.xlim([1,domains.size])
ax.yaxis.set_major_formatter(formatter)
plt.grid(True)
fig.savefig(fig_dir + 'third-domain2_count.png',format='png')
# percentages
fig = plt.figure()
plt.plot(range(1,domains.shape[0]+1),dom_perc*100,marker='.')
plt.xscale('log')
plt.xlabel('domain rank')
plt.ylabel('percentage of total number of images')
plt.xlim([1,domains.size])
plt.grid(True)
fig.savefig(fig_dir + 'third-domain2_perc.png',format='png')

# cumulative counts
fig, ax = plt.subplots()
plt.plot(range(1,domains.shape[0]+1),domains_cum,marker='.')
plt.xscale('log')
plt.title('Cumulative Counts')
plt.xlabel('domain rank')
plt.ylabel('count of all images')
ax.yaxis.set_major_formatter(formatter)
plt.grid(True)
#fig.tight_layout()
fig.savefig(fig_dir + 'third-domain2_count_cum.png',format='png')
# cumulative percentages
fig = plt.figure()
plt.plot(range(1,domains.shape[0]+1),dom_perc_cum*100,marker='.')
plt.xscale('log')
plt.ylim([0,100])
plt.title('Cumulative Percentage Counts')
plt.xlabel('domain rank')
plt.ylabel('percentage of total number of images')
plt.grid(True)
#fig.tight_layout()
fig.savefig(fig_dir + 'third-domain2_perc_cum.png',format='png')

# top 30 domains - counts
n=30
x=np.arange(0.5,n)
fig, ax = plt.subplots()
plt.bar(x,domains[0:n],align='center')
plt.xlabel('domains')
plt.ylabel('count of images')
labels = list(domains.index[0:n])
plt.xticks(x, labels, rotation=80)
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.grid(True)
fig.savefig(fig_dir + 'third-domain2_count_top30.png',format='png')

# top 30 domains - percentages
fig = plt.figure()
plt.bar(x,dom_perc[0:n]*100,align='center')
plt.xlabel('domains')
plt.ylabel('percentage of total number of images')
labels = list(domains.index[0:n])
plt.xticks(x, labels, rotation=80)
fig.tight_layout()
plt.grid(True)
fig.savefig(fig_dir + 'third-domain2_perc_top30.png',format='png')

domcom = df2[['respDom_domain2','company']].groupby(['respDom_domain2','company']).size().reset_index(name='img_perc').sort_values('img_perc',ascending=False)
domcom['img_perc']=domcom['img_perc']/float(df2.shape[0])*100
table_dir = '/home/nsarafij/project/OpenWPM/analysis/tables_10k'
fhand = open(os.path.join(table_dir,'third-domain2company_perc_top30.txt'),'w+')
### table domains - companies
for i in range(0,n):
    dom = domcom.iloc[i,0]
    com =  domcom.iloc[i,1]
    perc = domcom.iloc[i,2]
    s = str(i+1) + ' & ' + dom  +  ' & ' + com + ' & ' + '%.2f' % perc + '\\\\ \\hline'
    print s
    s = s.encode('UTF-8')
    print s
    fhand.write(s + '\n')  
    
       
fhand.close()
    

### companies
# counts
fig_dir = '/home/nsarafij/project/OpenWPM/analysis/figs_10k_domains/'
fig, ax = plt.subplots()
plt.plot(range(1,com.shape[0]+1),com,marker='.')
plt.xscale('log')
plt.xlabel('company rank')
plt.ylabel('count of third-party images')
plt.xlim([1,com.size])
ax.yaxis.set_major_formatter(formatter)
plt.grid(True)
fig.savefig(fig_dir + 'third-company_count.png',format='png')
# percentages
fig = plt.figure()
plt.plot(range(1,com.shape[0]+1),com_perc*100,marker='.')
plt.xscale('log')
plt.xlabel('company rank')
plt.ylabel('percentage of third-party images')
plt.xlim([1,com.size])
plt.grid(True)
fig.savefig(fig_dir + 'third-company_perc.png',format='png')

# cumulative counts
fig, ax = plt.subplots()
plt.plot(range(1,com.shape[0]+1),com_cum,marker='.')
plt.xscale('log')
plt.title('Cumulative Counts')
plt.xlabel('company rank')
plt.ylabel('count of third-party images')
ax.yaxis.set_major_formatter(formatter)
plt.grid(True)
#fig.tight_layout()
fig.savefig(fig_dir + 'third-company_count_cum.png',format='png')
# cumulative percentages
fig = plt.figure()
plt.plot(range(1,com.shape[0]+1),com_perc_cum*100,marker='.')
plt.xscale('log')
plt.ylim([0,100])
plt.title('Cumulative Percentage Counts')
plt.xlabel('company rank')
plt.ylabel('percentage of third-party images')
plt.grid(True)
#fig.tight_layout()
fig.savefig(fig_dir + 'third-company_perc_cum.png',format='png')

# top 30 companies - counts
n=30
x=np.arange(0.5,n)
fig, ax = plt.subplots()
plt.bar(x,com[0:n],align='center')
plt.xlabel('company')
plt.ylabel('count of third-party images')
labels = list(com.index[0:n])
plt.xticks(x, labels, rotation=90)
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.grid(True)
fig.savefig(fig_dir + 'third-company_count_top30.png',format='png')

# top 30 companies - percentages
fig = plt.figure()
plt.bar(x,com_perc[0:n]*100,align='center')
plt.xlabel('company')
plt.ylabel('percentage of third-party images')
labels = list(com.index[0:n])
plt.xticks(x, labels, rotation=90)
fig.tight_layout()
plt.grid(True)
fig.savefig(fig_dir + 'third-company_perc_top30.png',format='png')



############################## 1-pixel images

df3=df2.ix[df2['pixels']==1]

# 1-pixel images: counts per each response domain
dom_pix1 = df3['respDom_domain2'].value_counts()
dom_pix1_cum = dom_pix1.cumsum()
dom_pix1_perc = dom_pix1/float(total)
dom_pix1_perc_ = dom_pix1/float(dom_pix1_cum[dom_pix1_cum.size-1:dom_pix1_cum.size])
dom_pix1_perc_cum = dom_pix1_perc_.cumsum()
#dom_pix1_=pd.merge(pd.DataFrame(dom_pix1), df_dom, left_index=True, right_on='id')

# 1-pixel images: counts per each company
com_pix1 = df3['company'].value_counts()
com_pix1_cum = com_pix1.cumsum()
com_pix1_perc = com_pix1/float(total)
com_pix1_perc_ = com_pix1/float(com_pix1_cum[com_pix1_cum.size-1:com_pix1_cum.size])
com_pix1_perc_cum = com_pix1_perc_.cumsum()

# cdf of no of 
(x,y) = ecdf_for_plot(dom_pix1)
plt.figure()
plt.step(x,y)
plt.ylabel('cdf')
plt.xlabel('no of 1-pixel third-party images per domain')
plt.grid(True)
plt.xscale('symlog')
plt.savefig(os.path.join(fig_dir,'third-domains2_cdf.png'))

# counts
fig, ax = plt.subplots()
plt.plot(dom_pix1,marker='.')
plt.xscale('log')
ax.yaxis.set_major_formatter(formatter)
plt.xlabel('domain rank')
plt.ylabel('count of images')
plt.title('1-pixel Images')
plt.grid(True)
fig.savefig(fig_dir + 'third-domain2_pix1_count.png',format='png')

# percentages
fig = plt.figure()
plt.plot(range(1,dom_pix1_perc.shape[0]+1),dom_pix1_perc*100,marker='.')
plt.xscale('symlog')
plt.xlabel('domain rank')
plt.ylabel('percentage of total number of images')
plt.title('1-pixel Images')
plt.grid(True)
fig.savefig(fig_dir + 'third-domain2_pix1_perc.png',format='png')


# cumulative counts
fig, ax = plt.subplots()
plt.plot(range(1,dom_pix1_perc.shape[0]+1),dom_pix1_cum,marker='.')
ax.yaxis.set_major_formatter(formatter)
plt.xscale('log')
plt.title('Cumulative Counts for 1-pixel Images')
plt.xlabel('domain rank')
plt.ylabel('count')
plt.grid(True)
fig.savefig(fig_dir + 'third-domain2_pix1_count_cum.png',format='png')

# cumulative percentages
fig = plt.figure()
plt.plot(range(1,dom_pix1_perc.shape[0]+1),dom_pix1_perc_cum*100,marker='.')
plt.xscale('log')
plt.title('Cumulative Percentage Counts for 1-pixel Images')
plt.xlabel('domain rank')
plt.ylabel('percentage of 1-pixel images')
plt.grid(True)
fig.savefig(fig_dir + 'third-domain2_pix1_perc_cum.png',format='png')

# top 30 domains - counts
n=30
x=np.arange(0.5,n)
fig, ax = plt.subplots()
plt.bar(x,dom_pix1[0:n],align='center')
ax.yaxis.set_major_formatter(formatter)
plt.xlabel('domains')
plt.ylabel('count of images')
labels = list(dom_pix1.index[0:n])
plt.xticks(x, labels, rotation=80)
plt.title('1-pixel Images')
plt.grid(True)
fig.tight_layout()
fig.savefig(fig_dir + 'third-domain2_pix1_count_top30.png',format='png')

# top 20 domains - percentages
fig = plt.figure()
plt.bar(x,dom_pix1_perc[0:n]*100,align='center')
plt.xlabel('domains')
plt.ylabel('percentage of 1-pixel images')
labels = list(dom_pix1.index[0:n])
plt.xticks(x, labels, rotation=80)
plt.title('1-pixel Images')
plt.grid(True)
fig.tight_layout()
fig.savefig(fig_dir + 'third-domain2_pix1_perc_top30.png',format='png')

plt.show()

### table domains - companies
domcom = df3[['respDom_domain2','company']].groupby(['respDom_domain2','company']).size().reset_index(name='img_perc').sort_values('img_perc',ascending=False)
domcom['img_perc']=domcom['img_perc']/float(df2.shape[0])*100
table_dir = '/home/nsarafij/project/OpenWPM/analysis/tables_10k'
fhand = open(os.path.join(table_dir,'third-domain2company_pix1_perc_top30.txt'),'w+')

for i in range(0,n):
    dom = domcom.iloc[i,0]
    com =  domcom.iloc[i,1]
    perc = domcom.iloc[i,2]
    s = str(i+1) + ' & ' + dom  +  ' & ' + com + ' & ' + '%.2f' % perc + '\\\\ \\hline'
    print s
    s = s.encode('UTF-8')
    print s
    fhand.write(s + '\n')  
    
       
fhand.close()

### companies
# counts
fig_dir = '/home/nsarafij/project/OpenWPM/analysis/figs_10k_domains/'
fig, ax = plt.subplots()
plt.plot(range(1,com_pix1.shape[0]+1),com_pix1,marker='.')
plt.xscale('log')
plt.xlabel('company rank')
plt.ylabel('count of third-party images')
plt.xlim([1,com_pix1.size])
ax.yaxis.set_major_formatter(formatter)
plt.grid(True)
fig.savefig(fig_dir + 'third-company_pix1_count.png',format='png')
# percentages
fig = plt.figure()
plt.plot(range(1,com_pix1.shape[0]+1),com_pix1_perc*100,marker='.')
plt.xscale('log')
plt.xlabel('company rank')
plt.ylabel('percentage of third-party images')
plt.xlim([1,com_pix1.size])
plt.grid(True)
fig.savefig(fig_dir + 'third-company_pix1_perc.png',format='png')

# cumulative counts
fig, ax = plt.subplots()
plt.plot(range(1,com_pix1.shape[0]+1),com_pix1_cum,marker='.')
plt.xscale('log')
plt.title('Cumulative Counts')
plt.xlabel('company rank')
plt.ylabel('count of third-party images')
ax.yaxis.set_major_formatter(formatter)
plt.grid(True)
#fig.tight_layout()
fig.savefig(fig_dir + 'third-company_pix1_count_cum.png',format='png')
# cumulative percentages
fig = plt.figure()
plt.plot(range(1,com_pix1.shape[0]+1),com_pix1_perc_cum*100,marker='.')
plt.xscale('log')
plt.ylim([0,100])
plt.title('Cumulative Percentage Counts')
plt.xlabel('company rank')
plt.ylabel('percentage of third-party images')
plt.grid(True)
#fig.tight_layout()
fig.savefig(fig_dir + 'third-company_pix1_perc_cum.png',format='png')

# top 30 companies - counts
n=30
x=np.arange(0.5,n)
fig, ax = plt.subplots()
plt.bar(x,com_pix1[0:n],align='center')
plt.xlabel('company')
plt.ylabel('count of third-party images')
labels = list(com_pix1.index[0:n])
plt.xticks(x, labels, rotation=90)
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.grid(True)
fig.savefig(fig_dir + 'third-company_pix1_count_top30.png',format='png')

# top 30 companies - percentages
fig = plt.figure()
plt.bar(x,com_pix1_perc[0:n]*100,align='center')
plt.xlabel('company')
plt.ylabel('percentage of third-party images')
labels = list(com_pix1.index[0:n])
plt.xticks(x, labels, rotation=90)
fig.tight_layout()
plt.grid(True)
fig.savefig(fig_dir + 'third-company_pix1_perc_top30.png',format='png')
plt.show()

### table companies
table_dir = '/home/nsarafij/project/OpenWPM/analysis/tables_10k'
fhand = open(os.path.join(table_dir,'third-company_pix1_perc_top30.txt'),'w+')


for i in range(0,n):
    com = com_pix1_perc.index[i]
    perc = com_pix1_perc[i]*100
    s = str(i+1) +  ' & ' + com + ' & ' + '%.3f' % perc + '\\\\ \\hline'
    print s
    s = s.encode('UTF-8')
    print s
    fhand.write(s + '\n')  
    
       
fhand.close()


'''
fig1 = plt.figure(1)
plt.hist(df['size'], bins=100, color='lightblue',label ='all')
plt.title('Histogram of Images Sizes, no of sites = 100, max no of links = 300')
plt.xlabel('size [bytes]')
plt.ylabel('no of images')

fig2 = plt.figure(2)
plt.hist(df['size'], bins=100, range=(0,50000), color='lightblue',label ='all')
plt.title('Histogram of Images Sizes, no of sites = 100, max no of links = 300')
plt.xlabel('size [bytes]')
plt.ylabel('no of images')

fig3 = plt.figure(3)
plt.hist(df['size'], bins=100, range=(0,100), color='lightblue',label='all')
plt.title('Histogram of Images Sizes, no of sites = 100, max no of links = 300')
plt.xlabel('size [bytes]')
plt.ylabel('no of images')

fig = plt.figure(1)
plt.hist(l, bins=100, color='red',label =r'size $\neq$ content-length')
#plt.title('Histogram of Images Sizes (size != content-length), no of sites = 100, max no of links = 300')
#plt.xlabel('size [bytes]')
#plt.ylabel('no of images')
#fig.savefig('img_sizes_hist4.eps',format='eps')
plt.legend()

fig = plt.figure(2)
plt.hist(l, bins=100, range=(0,50000), color='red',label =r'size $\neq$ content-length')
#plt.title('Histogram of Images Sizes (size != content-length), no of sites = 100, max no of links = 300')
#plt.xlabel('size [bytes]')
#plt.ylabel('no of images')
#fig.savefig('img_sizes_hist5.eps',format='eps')
plt.legend()

fig = plt.figure(3)
plt.hist(l, bins=100, range=(0,100), color='red',label =r'size $\neq$ content-length')
#plt.title('Histogram of Images Sizes (size != content-length), no of sites = 100, max no of links = 300')
#plt.xlabel('size [bytes]')
#plt.ylabel('no of images')
#fig.savefig('img_sizes_hist6.eps',format='eps')
plt.legend()
#plt.show()
fig1.savefig('figs/img_sizes_hist1.eps',format='eps')
fig2.savefig('figs/img_sizes_hist2.eps',format='eps')
fig3.savefig('figs/img_sizes_hist3.eps',format='eps')

fig1 = plt.figure(1)
plt.plot(dom_perc,marker='o')
plt.title('Image Counts for Response Domains, no of sites = 100, max no of links = 300')
plt.xlabel('domains')
plt.ylabel('percentage of images')

fig2 = plt.figure(2)
plt.plot(dom_perc,marker='o')
plt.title('Image Counts for Response Domains, no of sites = 100, max no of links = 300')
plt.xlabel('domains')
plt.ylabel('percentage of images')
#plt.ylim([10,30000])
plt.xlim([0,100])

fig3 = plt.figure(3)
plt.plot(domains,marker='o')
plt.title('Image Counts for Response Domains, no of sites = 100, max no of links = 300')
plt.xlabel('domains')
plt.ylabel('percentage of images')
#plt.ylim([10,30000])
plt.xlim([0,10])


#plt.ylim([10,30000])
#plt.xlim([0,10])

fig5 = plt.figure(5)
plt.plot(dom_perc_cum,marker='o')
plt.title('Image Cumulative Percentage Counts for Response Domains \n no of sites = 100, max no of links = 300')
plt.xlabel('domains')
plt.ylabel('percentage of images')
#plt.ylim([10,30000])
plt.xlim([0,100])


fig6 = plt.figure(6)
plt.plot(dom_perc_cum,marker='o')
plt.title('Image Cumulative Percentage Counts for Response Domains \n no of sites = 100, max no of links = 300')
plt.xlabel('domains')
plt.ylabel('percentage of images')
#plt.ylim([10,30000])
plt.xlim([0,10])
#plt.show()

for i in range(1,7):
    fig_file = 'figs/img_domains_' + str(i) +'.eps'
    s = "fig{}.savefig('".format(i) + fig_file + "',format='eps')"
    print s
    exec s
'''






