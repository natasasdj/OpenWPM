import os
import sqlite3
import pandas as pd
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

res_dir = res_dir = '/home/nsarafij/project/OpenWPM/analysis/results/'
db = res_dir + 'images.sqlite'
conn = sqlite3.connect(db)
query = 'SELECT * FROM Images'
df = pd.read_sql_query(query,conn)
df['pixels']=map(int,df['pixels'])

df['pixels'].max() #178,560,000

df['pixels'].isnull().sum() #2,797,214
df['pixels'].isnull().sum()/float(df.shape[0])*100 #8.8%
pixels = df['pixels'].fillna(-1).map(int)

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

fig_dir = '/home/nsarafij/project/OpenWPM/analysis/figs_10k/'
    
(x,y) = ecdf_for_plot(pixels)

plt.figure()
plt.step(x,y)
plt.title('CDF of the total number of pixels')
plt.xlabel('total number of pixels')
plt.grid(True)
plt.xscale('symlog')
plt.savefig(os.path.join(fig_dir,'04a_pix_distr.png'))
plt.show()




grouped = df.groupby('pixels')
s_pix_count = grouped.size()
s_pix_count_=s_pix_count/float(df.shape[0])*100

df_pix_count = pd.DataFrame(s_pix_count,columns=['count'])

# count of total number of pixels


fig,ax=plt.subplots()
plt.scatter(s_pix_count.index,s_pix_count,marker='.',color='darkblue')
#s_pix_count_lim = s_pix_count[s_pix_count > 0.0001*df.shape[0]]
#plt.scatter(s_pix_count_lim.index,s_pix_count_lim, marker='.',color='lightblue')
plt.xscale('symlog')
plt.yscale('log')
plt.xlabel('total number of pixels')
plt.ylabel('number of images')
plt.xlim([-1,1e8])
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'pix_count.png',format='png')
fig.savefig(fig_dir + 'pix_count.eps',format='eps')


fig,ax=plt.subplots()
plt.scatter(s_pix_count_.index,s_pix_count_,marker='.',color='darkblue')
plt.xlabel('total number of pixels')
plt.ylabel('percentage of total number of images')
plt.xscale('symlog')
plt.yscale('log')
plt.xlim([-1,1e8])
plt.ylim([1e-6,1e2])
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'pix_perc.png',format='png')
fig.savefig(fig_dir + 'pix_perc.eps',format='eps')

# Top 20 size counts of images

s_pix_count_sort = s_pix_count.sort_values(ascending=False)
s_pix_perc_sort = s_pix_count_sort/float(df.shape[0])*100
 
x=range(1,21)
labels = map(str,[ int(a) for a in list(s_pix_count_sort.index[0:20]) ])
fig, ax = plt.subplots()
plt.bar(x,s_pix_count_sort.iloc[0:20],align='center', label ='all')
plt.xticks(x, labels,rotation=70)
plt.ylabel('count')
plt.xlabel('total number of pixels')
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'pix_count_top20.png',format='png')
fig.savefig(fig_dir + 'pix_count_top20.eps',format='eps')

x=range(1,21)
labels = map(str,[ int(a) for a in list(s_pix_perc_sort.index[0:20]) ])
fig, ax = plt.subplots()
plt.bar(x,s_pix_perc_sort.iloc[0:20],align='center', label ='all')
plt.xticks(x, labels,rotation=70)
plt.ylabel('percentage of total number of images')
plt.xlabel('total number of pixels')
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'pix_perc_top20.png',format='png')
fig.savefig(fig_dir + 'pix_perc_top20.eps',format='eps')


#s=df['size'][df['size']!=df['cont_length']]
#l=s.tolist()
#df['pixels'].fillna(value=-100,inplace=True)

'''
grouped = df.groupby(['pixels','type'])
s_pix_type_count = grouped.size()
df_pix_type_count = pd.DataFrame(s_type_count,columns=['count'])
'''

# scatter plot no of pixels vs size with the color showing count of a pixel-size pair

grouped = df.groupby(['pixels','size'])
pix_size_count = grouped.size().sort_values()
pixels = pix_size_count.index.get_level_values(level='pixels')
size = pix_size_count.index.get_level_values(level='size')

fig,ax=plt.subplots()
plt.scatter(pixels,size,c=pix_size_count,cmap="Reds", norm=LogNorm(),edgecolors='none')
cbar = plt.colorbar()
cbar.set_label('count of images')
plt.grid(True)
plt.xscale('symlog')
plt.yscale('symlog')
plt.xlim([-1,1e8])
plt.ylim([-1,1e8])
plt.xlabel('total no of pixels')
plt.ylabel('file size [bytes]')
#plt.show()
fig.savefig(fig_dir + 'pix_size_count.png',format='png')
fig.savefig(fig_dir + 'pix_size_count.eps',format='eps')

fig,ax=plt.subplots()
plt.scatter(pixels,size,c=pix_size_count/float(df.shape[0])*100,cmap="Reds", norm=LogNorm(),edgecolors='none')
cbar = plt.colorbar()
cbar.set_label('percentage of total number of images')
plt.grid(True)
plt.xscale('symlog')
plt.yscale('symlog')
plt.xlim([-1,1e8])
plt.ylim([-1,1e8])
plt.xlabel('total no of pixels')
plt.ylabel('file size [bytes]')
#plt.show()
fig.savefig(fig_dir + 'pix_size_perc.png',format='png')
fig.savefig(fig_dir + 'pix_size_perc.eps',format='eps')

# top 20 pixel size count

pix_size_count.sort_values(ascending = False,inplace = True)
x=range(1,21)
labels = map(str,[(int(a),int(b)) for (a,b) in pix_size_count.index[0:20]])
fig, ax = plt.subplots()
plt.bar(x,pix_size_count.iloc[0:20],align='center', label ='all')
plt.xticks(x, labels,rotation=70)
plt.ylabel('count')
plt.xlabel('total number of pixels, file size [bytes]')
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'pix_size_count_top20.png',format='png')
fig.savefig(fig_dir + 'pix_size_count_top20.eps',format='eps')


fig, ax = plt.subplots()
plt.bar(x,pix_size_count.iloc[0:20]/float(df.shape[0])*100,align='center', label ='all')
plt.xticks(x, labels,rotation=70)
plt.ylabel('percentage of total number of images')
plt.xlabel('total number of pixels, file size [bytes]')
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'pix_size_perc_top20.png',format='png')
fig.savefig(fig_dir + 'pix_size_perc_top20.eps',format='eps')
















