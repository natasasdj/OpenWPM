import os
import sqlite3
#import re
import pandas as pd
#import matplotlib.pyplot as plt
#from matplotlib.colors import LogNorm
#import numpy as np
#from matplotlib.ticker import FuncFormatter
#from statsmodels.distributions.empirical_distribution import ECDF
'''
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
'''
main_dir = '/home/nsarafij/project/OpenWPM/analysis_parallel'
res_dir = os.path.join(main_dir,'results/')
db = os.path.join(res_dir,'imagesFirst.sqlite')
conn = sqlite3.connect(db)
db = os.path.join(res_dir,'domains.sqlite')
conn2 = sqlite3.connect(db)
cur2 = conn2.cursor()

query = 'SELECT * FROM Domain2Company'
dom2com = pd.read_sql_query(query,conn)

query = 'SELECT * FROM DomainsTwoPart'
dom2 = pd.read_sql_query(query,conn)

query = 'SELECT * FROM Companies'
com = pd.read_sql_query(query,conn)

dom2_com = dom2com.merge(dom2, left_on = 'domainTwoPart_id', right_on = 'id', how = 'left').merge(com,left_on='company_id',right_on='id', how = 'left')[['company_id','domainTwoPart']]

query = 'SELECT * FROM BaseDomains'
baseDom = pd.read_sql_query(query,conn2)

baseDom_com = dom2_com.merge(baseDom, left_on = 'domainTwoPart', right_on = 'baseDomain', how = 'left')[['company_id','id']]
baseDom_com.columns = ['baseDomain_id' if x=='id' else x for x in baseDom_com.columns]

x = cur2.execute('CREATE TABLE IF NOT EXISTS Companies (id INTEGER PRIMARY KEY AUTOINCREMENT, company TEXT UNIQUE, country CHARACTER(2))')
x = cur2.execute('CREATE TABLE IF NOT EXISTS BaseDomain_Company (baseDomain_id INTEGER, company_id INTEGER, \
            FOREIGN KEY (baseDomain_id) REFERENCES baseDomains(id), FOREIGN KEY (company_id) REFERENCES Companies(id))')
            
com.to_sql('Companies',conn2,if_exists='append',index=False)
baseDom_com.to_sql('BaseDomain_Company',conn2,if_exists='append',index=False)  


















query = 'SELECT * FROM Domain_BaseDomain'
df_domdom2 = pd.read_sql_query(query,conn2)

df=df.merge(df_domdom2,left_on='site_id',right_on='domain_id',how='left')
df.drop('domain_id',axis=1,inplace=True)
df.columns = ['site_id2' if x=='baseDomain_id' else x for x in df.columns]
df=df.merge(df_domdom2,left_on='respDom_id',right_on='domain_id',how='left')
df.drop('domain_id',axis=1,inplace=True)
df.columns = ['respDom_id2' if x=='baseDomain_id' else x for x in df.columns]

df3 = df[df['site_id2'] != df['respDom_id2']]


query = 'SELECT * FROM BaseDomains'
df_dom2 = pd.read_sql_query(query,conn2)

df=df.merge(df_dom2, left_on = 'site_id2', right_on = 'id', how = 'left')
df.drop('id',inplace=True,axis=1)
df.columns = ['site_domain2' if x=='baseDomain' else x for x in df.columns]
df=df.merge(df_dom2, left_on = 'respDom_id2', right_on = 'id', how = 'left')
df.drop('id',inplace=True,axis=1)
df.columns = ['respDom_domain2' if x=='baseDomain' else x for x in df.columns]

# number of images
df.shape[0]
#31861758 odf
#45865581 n
df3.shape[0] #45854592
df3.shape[0]/float(df.shape[0]) #0.999760408573043


# percent of images for which cont_length > 100K
df[df['cont_length']>100000].shape[0]/float(df.shape[0])
# 0.095 
# percent of images for which size > 100K
df[df['size']>100000].shape[0]/float(df.shape[0])
# 0.030
# percent of images for which cont_length > 100K and file size <= 100K
df[(df['cont_length']>100000) & (df['size']<=100000)].shape[0]/float(df.shape[0])
# 0.065
# percent of images for which file size > 100K and cont_length <= 100K
df[(df['size']>100000) & (df['cont_length']<=100000)].shape[0]/float(df.shape[0])
# 0.00015

df[(df['size']==0) & (df['cont_length']>100000)].shape[0]/float(df.shape[0])
# 0.0184
df[(df['size']==0) & (df['cont_length']>100000)].shape[0]/float(df[df['size']==0].shape[0])
# 0.1826

s=df['size'][df['size']!=df['cont_length']]
l=s.tolist()

# df grouped by size 
size_count = df[['size']].groupby(['size']).size()
size_count.sort_values(inplace = True,ascending=False) 
size_count_ = size_count/df.shape[0]*100
size_count_1 = size_count[size_count>0.001*df.shape[0]]
size_count_2 = size_count_[size_count_>0.1]


# Histogram of images sizes

fig_dir = os.path.join(main_dir,'figs_10k/')

fig = plt.figure()
binwidth = 100
bins = range(df['size'].min(), df['size'].max() + binwidth, binwidth)
plt.hist(df['size'], bins=bins, color='lightblue', histtype = 'bar',label ='all')
plt.hist(l, color='red', bins=bins, label =r'size $\neq$ content-length')
plt.legend()
plt.xscale('symlog')
#plt.yscale('log')
plt.title('Histogram of Images Sizes, no of sites = 100, max no of links = 300')
plt.xlabel('file size [bytes]')
plt.ylabel('no of images')
fig.savefig(os.path.join(fig_dir,'01a_size_hist.png'),format='png')
plt.show()

fig = plt.figure()
binwidth = 100
bins = range(df['size'].min(), df['size'].max() + binwidth, binwidth)
plt.hist(df['size'], bins=bins, color='lightblue', histtype = 'bar',label ='all')
plt.hist(l, color='red', bins=bins, label =r'size $\neq$ content-length')
plt.legend()
plt.xscale('symlog')
plt.yscale('log')
plt.title('Histogram of Images Sizes, no of sites = 100, max no of links = 300')
plt.xlabel('file size [bytes]')
plt.ylabel('no of images')
fig.savefig(os.path.join(fig_dir,'01a_size_hist_log.png'),format='png')
plt.show()

# Cumulative distribution of images sizes


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
    
(x,y) = ecdf_for_plot(df['size'])

plt.figure()
plt.step(x,y)
plt.title('CDF of the file size of images')
plt.xlabel('size [bytes]')
plt.grid(True)
plt.xscale('symlog')
plt.savefig(os.path.join(fig_dir,'01b_size_cdf.png'))
plt.show()

fig, ax = plt.subplots()
plt.step(x,y)
plt.title('CDF of the file size of images')
plt.xlabel('size [bytes]')
plt.grid(True)
plt.xlim([0,1e5])
ax.yaxis.set_major_formatter(formatter)
plt.savefig(os.path.join(fig_dir,'01b_size_cdf_lin.png'))
plt.show()

# Size counts of images

fig = plt.figure()
plt.scatter(size_count.index,size_count,marker='.',color = 'blue', alpha=0.5)
#plt.scatter(size_count_1.index,size_count_1,marker='.',color = 'blue')
plt.xlabel('file size [bytes]')
plt.ylabel('count')
plt.xscale('symlog')
plt.yscale('log')
plt.xlim([-0.5,1e7])
plt.grid(True)
#plt.show()
fig.savefig(os.path.join(fig_dir,'01c_size_count.png'),format='png')

fig = plt.figure()
plt.scatter(size_count.index,size_count,marker='.',color = 'blue', alpha=0.5)
plt.xlabel('file size [bytes]')
plt.ylabel('count')
plt.xlim([-1000,6*1e4])
plt.ylim([0,1e3])
plt.grid(True)
#plt.show()
fig.savefig(os.path.join(fig_dir,'01c_size_count_lin.png'),format='png')

fig = plt.figure()
plt.scatter(size_count.index,size_count,marker='.',color = 'blue', alpha=0.5)
plt.xlabel('file size [bytes]')
plt.ylabel('count')
#plt.yscale('log')
plt.xlim([0,3000])
plt.ylim([0,2000])
plt.grid(True)
#plt.show()
fig.savefig(os.path.join(fig_dir,'01c_size_count_lin2.png'),format='png')



# Size percentages of images

fig = plt.figure()
plt.scatter(size_count_.index,size_count_,marker='.',color = 'blue', alpha=0.5)
plt.xlabel('file size [bytes]')
plt.ylabel('percentage of total number of images')
plt.xscale('symlog')
plt.yscale('log')
plt.xlim([-1,1e7])
plt.ylim([1e-6,100])
plt.grid(True)
#plt.show()
fig.savefig(os.path.join(fig_dir,'01d_size_perc.png'),format='png')

# Size counts of images for counts greater than 0.1% of total counts
fig = plt.figure()
plt.scatter(size_count_1.index,size_count_1)
plt.xscale('symlog')
plt.yscale('log')
plt.xlabel('file size [bytes]')
plt.ylabel('count')
plt.xlim([-1,1e4])
plt.grid(True)
plt.show()
fig.savefig(os.path.join(fig_dir,'01c_size_count_top01p.png'),format='png')


# Size percentages of images for percentages greater than 0.1
fig = plt.figure()
plt.scatter(size_count_2.index,size_count_2)
plt.xscale('symlog')
plt.yscale('log')
plt.xlim([-1,1e4])
plt.ylim([0.05,20])
plt.grid(True)
plt.xlabel('file size [bytes]')
plt.ylabel('percentage of total number of images')
plt.show()
fig.savefig(os.path.join(fig_dir,'01d_size_perc_top01p.png'),format='png')

# Top 20 size counts of images

s_=s.value_counts()
c = []
for size in size_count.index[0:20]:
    try:
        c.append(s_[size])
    except:
        c.append(0)

x=range(1,21)
labels = map(str,list(size_count.index[0:20]))
fig, ax = plt.subplots()
plt.bar(x,size_count[0:20],align='center', label ='all')
plt.xticks(x, labels,rotation=70)
plt.bar(x,c,color='red',align='center',label =r'size $\neq$ content-length')
plt.legend()
plt.xlabel('file size [bytes]')
plt.ylabel('count')
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.grid(True)
#plt.show()
fig.savefig(os.path.join(fig_dir,'01c_size_count_top20.png'),format='png')

fig, ax = plt.subplots()
plt.bar(x,size_count[0:20],align='center', label ='all')
plt.xticks(x, labels,rotation=70)
plt.bar(x,c,color='red',align='center',label =r'size $\neq$ content-length')
plt.legend()
plt.xlabel('file size [bytes]')
plt.ylabel('count')
ax.yaxis.set_major_formatter(formatter)
plt.ylim([0,0.8*1e5])
fig.tight_layout()
plt.grid(True)
plt.show()
fig.savefig('figs/01c_size_count_top20_zoom.png',format='png')
fig.savefig('figs/01c_size_count_top20_zoom.eps',format='eps')


fig = plt.figure()
plt.bar(x,size_count[0:20],align='center', label ='all')
plt.xticks(x, labels,rotation=70)
plt.bar(x,c,color='red',align='center',label =r'size $\neq$ content-length')
plt.legend()
plt.xlabel('file size [bytes]')
plt.ylabel('count')
plt.yscale('log')
fig.tight_layout()
plt.grid(True) 
plt.show()
fig.savefig('figs/01c_size_count_top20_ylog.png',format='png')
fig.savefig('figs/01c_size_count_top20_ylog.eps',format='eps')

# Top 20 size percentages of images
fig_dir = '/home/nsarafij/project/OpenWPM/analysis/figs/'
c_=np.array(c)/float(df.shape[0])*100
fig = plt.figure()
plt.bar(x,size_count_[0:20],align='center',label ='all')
plt.xticks(x, labels,rotation=70)
plt.bar(x,c_,color='red',align='center',label =r'size $\neq$ content-length')
plt.xlabel('file size [bytes]')
plt.ylabel('percentage of total number of images')
plt.legend()
fig.tight_layout()
plt.show()
fig.savefig(os.path.join(fig_dir,'01c_size_perc_top20.png'),format='png')

fig = plt.figure()
plt.bar(x,size_count_[0:20],align='center',label ='all')
plt.xticks(x, labels,rotation=70)
plt.bar(x,c_,color='red',align='center',label =r'size $\neq$ content-length')
plt.xlabel('file size [bytes]')
plt.ylabel('percentage of total number of images')
plt.legend()
plt.yscale('log')
plt.show()
fig.savefig('figs/01c_size_perc_top20_ylog.png',format='png')



# Scatter plot of content-length vs file size
'''    
i=0
for l in df['cont_length']:
    try:
        li=int(l)
    except:
        l
        df['cont_length'][i]= re.findall(r'\d+', l)[0]
    i+=1
'''

sl = df[['size','cont_length']].copy()
sl['cont_length'].isnull().sum() #0 n
sl['cont_length'] = pd.to_numeric(sl['cont_length'],'coerce')
sl.dropna(inplace = True)
size_length = sl.groupby(['size','cont_length']).size()
size_length.sort_values(inplace = True)
#print size_length.head()
size = size_length.index.get_level_values(level='size')
length = size_length.index.get_level_values(level='cont_length')

size_length_ = size_length[size_length > 0.001*df.shape[0]]
size_ = size_length_.index.get_level_values(level='size')
length_ = size_length_.index.get_level_values(level='cont_length')


fig_dir = os.path.join(main_dir,'figs')
fig = plt.figure()
#plt.scatter(size, length,c=size_length,cmap='RdPu', norm=LogNorm(), edgecolors='none',marker='.')
#plt.scatter(size_, length_,c=size_length_,cmap='coolwarm', norm=LogNorm(), edgecolors='none',marker='o',s=50)
plt.scatter(size, length, c=size_length, cmap='Reds', norm=LogNorm(), edgecolors='none', s= 40)
#plt.scatter(size_, length_,c=size_length_,cmap='Blues', norm=LogNorm(), edgecolors='none',marker='o',s=50)
plt.xscale('symlog')
plt.yscale('symlog')
plt.xlim([-1,1e7])
plt.ylim([-1,1e6])
plt.xlabel('file size [bytes]')
plt.ylabel('content-length [bytes]')
cbar = plt.colorbar()
cbar.set_label('count of images')
fig.tight_layout()
#cbar.ax.set_title('count of images')
fig.savefig(fig_dir+'size_length.png',format='png')
#fig.savefig(fig_dir+'size_length.eps',format='eps')
plt.show()


fig = plt.figure()
plt.scatter(size, length,c=size_length/float(sl.shape[0]),cmap='Reds', norm=LogNorm(), edgecolors='none', s= 40)
plt.xscale('symlog')
plt.yscale('symlog')
plt.xlim([-1,1e9])
plt.ylim([-1,1e9])
plt.xlabel('file size [bytes]')
plt.ylabel('content-length [bytes]')
cbar = plt.colorbar()
cbar.set_label('percentage of total number of images')
fig.tight_layout()
fig.savefig(fig_dir+'size_length_perc.png',format='png')
plt.show()


# top 20 size-length pairs

size_length.sort_values(inplace = True,ascending=False)
x=range(1,21)
labels = map(str,size_length.index)
fig,ax = plt.subplots()
plt.bar(x,size_length[0:20]/,align='center', label ='all')
#plt.yscale('log')
plt.xticks(x, labels,rotation=60)
plt.ylabel('count')
plt.xlabel('file size,content-length [bytes]')
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.show()
fig.savefig(fig_dir+'size_length_top20.png',format='png')
fig.savefig(fig_dir+'size_length_top20.eps',format='eps')

fig,ax = plt.subplots()
plt.bar(x,size_length[0:20],align='center', label ='all')
plt.yscale('log')
plt.xticks(x, labels,rotation=60)
plt.ylabel('count')
plt.xlabel('file size,content-length [bytes]')
#ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.show()
fig.savefig(fig_dir+'size_length_top20_ylog.png',format='png')
fig.savefig(fig_dir+'size_length_top20_ylog.eps',format='eps')


fig,ax = plt.subplots()
plt.bar(x,size_length[0:20]/float(df.shape[0]),align='center', label ='all')
#plt.yscale('log')
plt.xticks(x, labels,rotation=60)
plt.ylabel('percentage of total number of images')
plt.xlabel('file size,content-length [bytes]')
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.show()
fig.savefig(fig_dir+'size_length_top20_perc.png',format='png')
fig.savefig(fig_dir+'size_length_top20_perc.eps',format='eps')



# top 20 size-length pairs where file size is different from content-length

size = size_length.index.get_level_values(level='size')
length = size_length.index.get_level_values(level='cont_length')
size_diff_length = size_length[size!=length]

x=range(1,21)
labels = map(str,size_diff_length.index)
fig,ax = plt.subplots()
plt.bar(x,size_diff_length[0:20],align='center', label ='all')
#plt.yscale('log')
plt.xticks(x, labels,rotation=60)
plt.xlabel('file size,content-length [bytes]')
plt.ylabel('count')
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.show()
fig.savefig(fig_dir+'size_length_diff_top20.png',format='png')
fig.savefig(fig_dir+'size_length_diff_top20.eps',format='eps')

fig,ax = plt.subplots()
plt.bar(x,size_diff_length[0:20]/float(df.shape[0]),align='center', label ='all')
#plt.yscale('log')
plt.xticks(x, labels,rotation=60)
plt.xlabel('file size,content-length [bytes]')
plt.ylabel('count')
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.show()
fig.savefig(fig_dir+'size_length_diff_top20_perc.png',format='png')
fig.savefig(fig_dir+'size_length_diff_top20_perc.eps',format='eps')

# Images with file size equal to 0

sl.loc[sl['size']==0].shape[0] #3853119
sl.loc[sl['size']==0].shape[0]/float(sl.shape[0]) #0.08981866165282819 
sl.loc[(sl['size']==0) & (sl['cont_length']>100000)].shape[0] #74838 
74838/3853119. #0.019422706643630782 

sl.loc[sl['cont_length']>100000].shape[0] 
#1379818
sl.loc[sl['cont_length']>100000].shape[0] / float(sl.shape[0])
#0.03216443771512951




'''
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
plt.legend()

fig = plt.figure(2)
plt.hist(l, bins=100, range=(0,50000), color='red',label =r'size $\neq$ content-length')
plt.legend()

fig = plt.figure(3)
plt.hist(l, bins=100, range=(0,100), color='red',label =r'size $\neq$ content-length')
plt.legend()

fig4 = plt.figure(4)
plt.scatter(df['size'], df['cont_length'],alpha=0.01)
plt.title(' Size vs Content-Length, no of sites = 100, max no of links = 300')
plt.xlabel('size [bytes]')
plt.ylabel('content-length [bytes]')
plt.xlim(-1000, 100000)
plt.ylim(-1000, 100000)

fig5 = plt.figure(5)
plt.scatter(df['size'], df['cont_length'],alpha=0.01)
plt.title(' Size vs Content-Length, no of sites = 100, max no of links = 300')
plt.xlabel('size [bytes]')
plt.ylabel('content-length [bytes]')
plt.xlim(-100, 1000)
plt.ylim(-100, 1000)

fig6 = plt.figure(6)
plt.scatter(df['size'], df['cont_length'],alpha=0.01)
plt.title(' Size vs Content-Length, no of sites = 100, max no of links = 300')
plt.xlabel('size [bytes]')
plt.ylabel('content-length [bytes]')
plt.xlim(-10, 200)
plt.ylim(-10, 200)

#plt.show()

for i in range(1,7):
    fig_file = 'figs/img_sizes_' + str(i) +'.eps'
    s = "fig{}.savefig('".format(i) + fig_file + "',format='eps')"
    print s
    exec s

for i in range(1,7):
    fig_file = 'figs/img_sizes/img_sizes_' + str(i) +'.png'
    s = "fig{}.savefig('".format(i) + fig_file + "',format='png')"
    print s
    exec s

'''


