import os
import sqlite3
import pandas as pd
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


res_dir = '/home/nsarafij/project/OpenWPM/analysis/results/'
db = res_dir + 'images.sqlite'
conn = sqlite3.connect(db)
query = 'SELECT * FROM Images'
df = pd.read_sql_query(query,conn)
query = 'SELECT * FROM Domains'
df_dom = pd.read_sql_query(query,conn)

# all images: counts per each response domain
domains = df['resp_domain'].value_counts()
total = df.shape[0]
domains_cum = domains.cumsum()
dom_perc = domains/float(total)
dom_perc_cum = dom_perc.cumsum()
domains_=pd.merge(pd.DataFrame(domains), df_dom, left_index=True, right_on='id')

# 1-pixel images: counts per each response domain
dom_pix1 = df.ix[df['pixels']==1]['resp_domain'].value_counts()
dom_pix1_cum = dom_pix1.cumsum()
dom_pix1_perc = dom_pix1/float(df.shape[0])
dom_pix1_perc_ = dom_pix1/float(dom_pix1_cum[dom_pix1_cum.size-1:dom_pix1_cum.size])
dom_pix1_perc_cum = dom_pix1_perc_.cumsum()
dom_pix1_=pd.merge(pd.DataFrame(dom_pix1), df_dom, left_index=True, right_on='id')

# all images
# counts
fig_dir = '/home/nsarafij/project/OpenWPM/analysis/figs/'
fig, ax = plt.subplots()
plt.plot(range(1,domains.shape[0]+1),domains,marker='.')
plt.xscale('log')
plt.xlabel('domain rank')
plt.ylabel('count of images')
plt.xlim([1,domains.size])
ax.yaxis.set_major_formatter(formatter)
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'domain_count.png',format='png')
fig.savefig(fig_dir + 'domain_count.eps',format='eps')
# percentages
fig = plt.figure()
plt.plot(range(1,domains.shape[0]+1),dom_perc*100,marker='.')
plt.xscale('log')
plt.xlabel('domain rank')
plt.ylabel('percentage of total number of images')
plt.xlim([1,domains.size])
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'domain_perc.png',format='png')
fig.savefig(fig_dir + 'domain_perc.eps',format='eps')

# cumulative counts
fig, ax = plt.subplots()
plt.plot(domains_cum,marker='.')
plt.xscale('log')
plt.title('Cumulative Counts')
plt.xlabel('domain rank')
plt.ylabel('count of all images')
ax.yaxis.set_major_formatter(formatter)
plt.grid(True)
fig.tight_layout()
plt.show()
fig.savefig(fig_dir + 'domain_count_cum.png',format='png')
fig.savefig(fig_dir + 'domain_count_cum.eps',format='eps')
# cumulative percentages
fig = plt.figure()
plt.plot(range(1,dom_perc_cum.shape*100,marker='.')
plt.xscale('log')
plt.title('Cumulative Percentage Counts')
plt.xlabel('domain rank')
plt.ylabel('percentage of total number of images')
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'domain_perc_cum.png',format='png')
fig.savefig(fig_dir + 'domain_perc_cum.eps',format='eps')

# top 20 domains - counts
n=20
x=range(0,n)
fig, ax = plt.subplots()
plt.bar(x,domains[0:n])
plt.xlabel('domains')
plt.ylabel('count of images')
labels = list(domains_['domain'][0:n])
plt.xticks(x, labels, rotation=80)
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'domain_count_top20.png',format='png')
fig.savefig(fig_dir + 'domain_count_top20.eps',format='eps')
# top 20 domains - percentages
fig = plt.figure()
plt.bar(x,dom_perc[0:n]*100)
plt.xlabel('domains')
plt.ylabel('percentage of total number of images')
labels = list(domains_['domain'][0:n])
plt.xticks(x, labels, rotation=80)
fig.tight_layout()
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'domain_perc_top20.png',format='png')
fig.savefig(fig_dir + 'domain_perc_top20.eps',format='eps')

# 1-pixel images
# counts
fig, ax = plt.subplots()
plt.plot(dom_pix1,marker='.')
plt.xscale('log')
ax.yaxis.set_major_formatter(formatter)
plt.xlabel('domain rank')
plt.ylabel('count of images')
plt.title('1-pixel Images')
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'domain_pix1_count.png',format='png')
fig.savefig(fig_dir + 'domain_pix1_count.eps',format='eps')
# percentages
fig = plt.figure()
plt.plot(range(1,dom_pix1_perc.shape[0]+1),dom_pix1_perc*100,marker='.')
plt.xscale('symlog')
plt.xlabel('domain rank')
plt.ylabel('percentage of total number of images')
plt.title('1-pixel Images')
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'domain_pix1_perc.png',format='png')
fig.savefig(fig_dir + 'domain_pix1_perc.eps',format='eps')

# cumulative counts
fig, ax = plt.subplots()
plt.plot(dom_pix1_cum,marker='.')
ax.yaxis.set_major_formatter(formatter)
plt.xscale('log')
plt.title('Cumulative Counts for 1-pixel Images')
plt.xlabel('domain rank')
plt.ylabel('count')
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'domain_pix1_count_cum.png',format='png')
fig.savefig(fig_dir + 'domain_pix1_count_cum.eps',format='eps')
# cumulative percentages
fig = plt.figure()
plt.plot(dom_pix1_perc_cum*100,marker='.')
plt.xscale('log')
plt.title('Cumulative Percentage Counts for 1-pixel Images')
plt.xlabel('domain rank')
plt.ylabel('percentage of 1-pixel images')
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'domain_pix1_perc_cum.png',format='png')
fig.savefig(fig_dir + 'domain_pix1_perc_cum.eps',format='eps')


# top 20 domains - counts
n=20
x=range(0,n)
fig, ax = plt.subplots()
plt.bar(x,dom_pix1[0:n])
ax.yaxis.set_major_formatter(formatter)
plt.xlabel('domains')
plt.ylabel('count of images')
labels = list(dom_pix1_['domain'][0:n])
plt.xticks(x, labels, rotation=80)
plt.title('1-pixel Images')
plt.grid(True)
fig.tight_layout()
plt.show()
fig.savefig(fig_dir + 'domain_pix1_count_top20.png',format='png')
fig.savefig(fig_dir + 'domain_pix1_count_top20.eps',format='eps')
# top 20 domains - percentages
fig = plt.figure()
plt.bar(x,dom_pix1_perc[0:n]*100)
plt.xlabel('domains')
plt.ylabel('percentage of 1-pixel images')
labels = list(dom_pix1_['domain'][0:n])
plt.xticks(x, labels, rotation=80)
plt.title('1-pixel Images')
plt.grid(True)
fig.tight_layout()
plt.show()
fig.savefig(fig_dir + 'domain_pix1_perc_top20.png',format='png')
fig.savefig(fig_dir + 'domain_pix1_perc_top20.eps',format='eps')

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






