import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from matplotlib.ticker import FuncFormatter

def thousands(x, pos):
    if x>=1000:
        'The two args are the value and tick position'
        return '%dK' % (x*1e-3)
    else:
        return x

formatter = FuncFormatter(thousands)

curr_dir = os.getcwd()
res_dir = curr_dir + '/results/'
db = res_dir + 'images.sqlite'
conn = sqlite3.connect(db)
query = 'SELECT * FROM Images'
df = pd.read_sql_query(query,conn)
s=df['size'][df['size']!=df['cont_length']]
l=s.tolist()


size_count = df[['size']].groupby(['size']).size()
size_count.sort_values(inplace = True,ascending=False) 
size_count_ = size_count/df.shape[0]*100
size_count_1 = size_count[size_count>0.001*df.shape[0]]
size_count_2 = size_count_[size_count_>0.1]



import numpy as np

data = [1.2, 14, 150 ]
bins = 10**(np.arange(0,4))
print "bins: ", bins
plt.xscale('log')
plt.hist(data,bins=bins)
 
logbins=np.max(xx)*(np.logspace(0, 1, num=1000) - 1)/9
hh,ee=np.histogram(xx, density=True, bins=logbins)
'''

'''
# Histogram of images sizes

fig = plt.figure()
bins=range(0,1000)
plt.hist(df['size'], bins=bins, color='lightblue',histtype = 'bar',label ='all')
plt.hist(l, bins=bins, color='red',label =r'size $\neq$ content-length')
plt.legend()
plt.xscale('symlog')
plt.yscale('log')
plt.title('Histogram of Images Sizes, no of sites = 100, max no of links = 300')
plt.xlabel('file size [bytes]')
plt.ylabel('no of images')
plt.show()
fig.savefig('figs/size_hist.png',format='png')
fig.savefig('figs/size_hist.eps',format='eps')


# Size counts of images


fig = plt.figure()
plt.scatter(size_count.index,size_count)
plt.xlabel('file size [bytes]')
plt.ylabel('count')
plt.xscale('symlog')
plt.yscale('log')
plt.xlim([-1,1000000])
plt.show()
fig.savefig('figs/size_count.png',format='png')
fig.savefig('figs/size_count.eps',format='eps')

# Size percentages of images

fig = plt.figure()
plt.scatter(size_count_.index,size_count_)
plt.xlabel('file size [bytes]')
plt.ylabel('percentage of total number of images')
plt.xscale('symlog')
plt.yscale('log')
plt.xlim([-1,1000000])
plt.ylim([0.0001,100])
plt.show()
fig.savefig('figs/size_perc.png',format='png')
fig.savefig('figs/size_perc.eps',format='eps')

# Size counts of images for counts greater than 0.1% of total counts
fig = plt.figure()

plt.scatter(size_count_1.index,size_count_1)
plt.xscale('symlog')
plt.yscale('log')
plt.xlabel('file size [bytes]')
plt.ylabel('count')
plt.xlim([-1,10000])
plt.show()
fig.savefig('figs/size_count_top01p.png',format='png')
fig.savefig('figs/size_count_top01p.eps',format='eps')

# Size percentages of images for percentages greater than 0.1
fig = plt.figure()

plt.scatter(size_count_2.index,size_count_2)
plt.xscale('symlog')
plt.yscale('log')
plt.xlim([-1,10000])
plt.xlabel('file size [bytes]')
plt.ylabel('percentage of total number of images')
plt.show()
fig.savefig('figs/size_perc_top01p.png',format='png')
fig.savefig('figs/size_perc_top01p.eps',format='eps')

# Top 20 size counts of images

x=range(1,21)
labels = map(str,list(size_count.index[0:20]))
s_=s.value_counts()
c = []
for size in size_count.index[0:20]:
    try:
        c.append(s_[size])
    except:
        c.append(0)


fig, ax = plt.subplots()
plt.bar(x,size_count[0:20],align='center', label ='all')
plt.xticks(x, labels,rotation=70)
plt.bar(x,c,color='red',align='center',label =r'size $\neq$ content-length')
plt.legend()
plt.xlabel('file size [bytes]')
ax.yaxis.set_major_formatter(formatter)
plt.show()
fig.savefig('figs/size_count_top20.png',format='png')
fig.savefig('figs/size_count_top20.eps',format='eps')

fig = plt.figure()
plt.bar(x,size_count[0:20],align='center', label ='all')
plt.xticks(x, labels,rotation=70)
plt.bar(x,c,color='red',align='center',label =r'size $\neq$ content-length')
plt.legend()
plt.xlabel('file size [bytes]')
plt.yscale('log')
plt.show()
fig.savefig('figs/size_count_top20_ylog.png',format='png')
fig.savefig('figs/size_count_top20_ylog.eps',format='eps')

# Top 20 size percentages of images

c_=np.array(c)/float(df.shape[0])*100
fig = plt.figure()
plt.bar(x,size_count_[0:20],align='center',label ='all')
plt.xticks(x, labels,rotation=70)
plt.bar(x,c_,color='red',align='center',label =r'size $\neq$ content-length')
plt.xlabel('file size [bytes]')
plt.ylabel('percentage')
plt.legend()
plt.show()
fig.savefig('figs/size_perc_top20.png',format='png')
fig.savefig('figs/size_perc_top20.eps',format='eps')

fig = plt.figure()
plt.bar(x,size_count_[0:20],align='center',label ='all')
plt.xticks(x, labels,rotation=70)
plt.bar(x,c_,color='red',align='center',label =r'size $\neq$ content-length')
plt.xlabel('file size [bytes]')
plt.ylabel('percentage')
plt.legend()
plt.yscale('log')
plt.show()
fig.savefig('figs/size_perc_top20_ylog.png',format='png')
fig.savefig('figs/size_perc_top20_ylog.eps',format='eps')



# Scatter plot of content-length vs file size
    
size_length = df[['size','cont_length']].groupby(['size','cont_length']).size()
size_length.sort_values(inplace = True)
#print size_length.head()
size = size_length.index.get_level_values(level='size')
length = size_length.index.get_level_values(level='cont_length')
size_length_ = size_length[size_length > 0.001*df.shape[0]]
size_ = size_length_.index.get_level_values(level='size')
length_ = size_length_.index.get_level_values(level='cont_length')

fig = plt.figure()
#plt.scatter(size, length,c=size_length,cmap='RdPu', norm=LogNorm(), edgecolors='none',marker='.')
#plt.scatter(size_, length_,c=size_length_,cmap='coolwarm', norm=LogNorm(), edgecolors='none',marker='o',s=50)
plt.scatter(size, length,c=size_length,cmap='Reds', norm=LogNorm(), edgecolors='none', s= 40)
#plt.scatter(size_, length_,c=size_length_,cmap='Blues', norm=LogNorm(), edgecolors='none',marker='o',s=50)
#plt.pcolor(size, length, size_length, norm=LogNorm(vmin=size_length.min(), vmax=size_length.max()), cmap='coolwarm')
plt.xscale('symlog')
plt.yscale('symlog')
plt.xlim([-1,1000000])
plt.ylim([-1,1000000])
plt.xlabel('file size [bytes]')
plt.ylabel('content-length [bytes]')
cbar = plt.colorbar()
cbar.set_label('count of images',rotation = 270)
fig.tight_layout()
#cbar.ax.set_title('count of images')
plt.show()
fig.savefig('figs/size_length.png',format='png')
fig.savefig('figs/size_length.eps',format='eps')

size_length.sort_values(inplace = True,ascending=False)
x=range(1,31)
labels = map(str,size_length.index)
fig,ax = plt.subplots()
plt.bar(x,size_length[0:30],align='center', label ='all')
#plt.yscale('log')
plt.xticks(x, labels,rotation=70)
plt.ylabel('count')
plt.xlabel('file size,content-length [bytes]')
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.show()
fig.savefig('figs/size_length_top20.png',format='png')
fig.savefig('figs/size_length_top20.eps',format='eps')

size = size_length.index.get_level_values(level='size')
length = size_length.index.get_level_values(level='cont_length')
size_diff_length = size_length[size!=length]

x=range(1,31)
labels = map(str,size_diff_length.index)
fig,ax = plt.subplots()
plt.bar(x,size_diff_length[0:30],align='center', label ='all')
#plt.yscale('log')
plt.xticks(x, labels,rotation=70)
plt.xlabel('file size,content-length [bytes]')
plt.ylabel('count')
#ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.show()
fig.savefig('figs/size_length_diff_top20.png',format='png')
fig.savefig('figs/size_length_diff_top20.eps',format='eps')
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


