import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF


curr_dir = os.getcwd()
res_dir = curr_dir + '/results3/'
db = res_dir + 'images.sqlite'
conn = sqlite3.connect(db)
query = 'SELECT * FROM Images'
df = pd.read_sql_query(query,conn)
#s=df['size'][df['size']!=df['cont_length']]
#l=s.tolist()
#df['pixels'].fillna(value=-1000,inplace=True)
#print df.describe()
domains = df['resp_domain'].value_counts()
#print type('domains')
total = df.shape[0]
#print domains.head(n=20)
print domains.shape[0]
dom_perc = domains/float(total)
#print dom_perc.head(n=20)
dom_perc_cum = dom_perc.cumsum()
#print dom_perc_cum.head(n=20)


fig1 = plt.figure(1)
plt.plot(dom_perc,marker='o')
plt.title('Image Counts for Response Domains, no of sites = 100, max no of links = 300')
plt.xlabel('domains')
plt.ylabel('percentage of images')
#plt.ylim([10,30000])
#plt.xlim([0,500])

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

fig4 = plt.figure(4)
plt.plot(dom_perc_cum,marker='o')
plt.title('Image Cumulative Percentage Counts for Response Domains \n no of sites = 100, max no of links = 300')
plt.xlabel('domains')
plt.ylabel('percentage of images')
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
'''






