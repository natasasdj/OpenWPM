import os
import sqlite3
import pandas as pd
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
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

#main_dir = '/home/nsarafij/project/nsdjWPM/analysis/'
#main_dir = '/home/nsarafij/project/OpenWPM/analysis_parallel/'
main_dir = '/root/OpenWPM/analysis_parallel/'
res_dir = os.path.join(main_dir,'results')
db = os.path.join(res_dir,'images.sqlite')
conn = sqlite3.connect(db)
db = os.path.join(res_dir,'domains.sqlite')
conn2 = sqlite3.connect(db)

query = 'SELECT * FROM Images'
#query = 'SELECT site_id, resp_domain, size,cont_length FROM Images'
df = pd.read_sql_query(query,conn)
df.columns = ['respDom_id' if x=='resp_domain' else x for x in df.columns]

query = 'SELECT * FROM Domain_BaseDomain'
df_domdom2 = pd.read_sql_query(query,conn2)

df=df.merge(df_domdom2,left_on='site_id',right_on='domain_id',how='left')
df.drop('domain_id',axis=1,inplace=True)
df.columns = ['site_id2' if x=='baseDomain_id' else x for x in df.columns]
df=df.merge(df_domdom2,left_on='respDom_id',right_on='domain_id',how='left')
df.drop('domain_id',axis=1,inplace=True)
df.columns = ['respDom_id2' if x=='baseDomain_id' else x for x in df.columns]

query = 'SELECT * FROM BaseDomains'
df_dom2 = pd.read_sql_query(query,conn2)

df=df.merge(df_dom2, left_on = 'site_id2', right_on = 'id', how = 'left')
df.drop('id',inplace=True,axis=1)
df.columns = ['site_domain2' if x=='baseDomain' else x for x in df.columns]
df=df.merge(df_dom2, left_on = 'respDom_id2', right_on = 'id', how = 'left')
df.drop('id',inplace=True,axis=1)
df.columns = ['respDom_domain2' if x=='baseDomain' else x for x in df.columns]


db = os.path.join(res_dir,'imagesMerged.sqlite')
conn1 = sqlite3.connect(db)
cur1=conn.cursor()
cur1.execute('CREATE TABLE IF NOT EXISTS Df (site_id INTEGER NOT NULL, link_id INTEGER NOT NULL, resp_id INTEGER NOT NULL, \
                                                 respDom_id INTEGER, size INTEGER, cont_length INTEGER, type INTEGER, cont_type INTEGER, pixels INTEGER, \
                                                 site_id2 INTEGER, respDom_id2 INTEGER, site_domain2 TEXT, respDom_domain2 TEXT, \
                                                 PRIMARY KEY (site_id, link_id, resp_id))')

df.to_sql('Df', conn1, if_exists = 'append', index = False)

# query = 'SELECT * FROM df'
# df = pd.read_sql_query(query,conn)


df3 = df[df['site_id2'] != df['respDom_id2']]

db = os.path.join(res_dir,'images3.sqlite')
conn3 = sqlite3.connect(db)
cur3=conn.cursor()
cur3.execute('CREATE TABLE IF NOT EXISTS Images3 (site_id INTEGER NOT NULL, link_id INTEGER NOT NULL, resp_id INTEGER NOT NULL, \
                                                 respDom_id INTEGER, size INTEGER, cont_length INTEGER, type INTEGER, cont_type INTEGER, pixels INTEGER, \
                                                 site_id2 INTEGER, respDom_id2 INTEGER, site_domain2 TEXT, respDom_domain2 TEXT, \
                                                 PRIMARY KEY (site_id, link_id, resp_id))')

df3.to_sql('Images3', conn3, if_exists = 'append', index = False)


# number of images
df.shape[0] #31861758 odf #45865581 n #132348177
df3.shape[0] #45854592 #98160638
df3.shape[0]/float(df.shape[0]) #0.999760408573043  #0.7416848514656912




# df grouped by size 
size_count = df3[['size']].groupby(['size']).size()
size_count.sort_values(inplace = True,ascending=False) 
size_count_ = size_count/float(df3.shape[0])*100
#size_count_1 = size_count[size_count>0.001*df.shape[0]]
#size_count_2 = size_count_[size_count_>0.1]

df3['cont_length'] = pd.to_numeric(df3['cont_length'],errors='coerce',downcast='integer')



s = df3[df3['size']!=df3['cont_length']]
s['size'] 
#l=s.tolist()
sc = s[['size']].groupby(['size']).size()
sc.sort_values(inplace = True,ascending=False) 
sc_ = sc/float(s.shape[0])*100

fig_dir = os.path.join(main_dir,'figs')

'''
# Histogram of images sizes



fig = plt.figure()
binwidth = 100
bins = range(df3['size'].min(), df3['size'].max() + binwidth, binwidth)
plt.hist(df3['size'], bins=bins, color='lightblue', histtype = 'bar',label ='all')
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
bins = range(df3['size'].min(), df3['size'].max() + binwidth, binwidth)
plt.hist(df3['size'], bins=bins, color='lightblue', histtype = 'bar',label ='all')
plt.hist(l, color='red', bins=bins, label =r'size $\neq$ content-length')
plt.legend()
plt.xscale('symlog')
plt.yscale('log')
plt.title('Histogram of Images Sizes, no of sites = 100, max no of links = 300')
plt.xlabel('file size [bytes]')
plt.ylabel('no of images')
fig.savefig(os.path.join(fig_dir,'01a_size_hist_log.png'),format='png')
plt.show()
'''

# Cumulative distribution of images sizes


def ecdf_for_plot(sample):
    x = sample.sort_values(ascending = False)
    ecdf = ECDF(x)
    y = ecdf(x)
    return (x,y)    
    
(x,y) = ecdf_for_plot(df3['size'])
(x2,y2) = ecdf_for_plot(s['size'])

plt.figure()
plt.step(x,y,color='blue', label ='all')
plt.step(x2,y2 * float(s.shape[0])/float(df3.shape[0]),color = 'red', label =r'size $\neq$ content-length')
plt.legend(loc='upper left')
plt.xlabel('file size [bytes]')
plt.xlabel('cdf')
plt.grid(True)
plt.xscale('symlog')
plt.xlim([0,1e9])
plt.savefig(os.path.join(fig_dir,'01b_size_cdf.png'))
#plt.show()

'''
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
c_=np.array(c)/float(df3.shape[0])*100
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

'''

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

sl = df3[['size','cont_length']].copy()
sl['cont_length'].isnull().sum() #0 n
#sl['cont_length'] = pd.to_numeric(sl['cont_length'],'coerce')
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
plt.xlim([-1,1e5])
plt.ylim([-1,1e5])
plt.xlabel('file size [bytes]')
plt.ylabel('content-length [bytes]')
cbar = plt.colorbar()
cbar.set_label('count of images')
fig.tight_layout()
#cbar.ax.set_title('count of images')
fig.savefig(os.path.join(fig_dir,'01a_size_length_perc.png'),format='png')
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
fig.savefig(os.path.join(fig_dir,'01_size_length_perc.png'),format='png')
#plt.show()

'''
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



