import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
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

query = 'SELECT * FROM Types'
types = pd.read_sql_query(query,conn)

# icon images
icon_type = []
for i in range(0,types.shape[0]):
    if ('icon' in types.iloc[i]['type']):
        icon_type.append(types.iloc[i]['id'])

icon_type
# [6, 15]

icon = df[df['type'].isin(icon_type)]
icon.shape[0]
# 1,932,013
sum(icon['pixels'].isnull())
# 535744
icon['pixels'].isnull().sum()/float(icon.shape[0])*100
# 27.73 % number of corrupted files


# icon images - pixel count  

pix_count = icon.groupby(['pixels']).size()
pix_count.sort_values(inplace = True)

fig_dir = '/home/nsarafij/project/OpenWPM/analysis/figs/'
fig,ax=plt.subplots()
plt.scatter(pix_count.index, pix_count, marker='.',color='darkblue')
plt.xscale('symlog')
plt.yscale('symlog')
plt.xlim([-1,1e8])
plt.ylim([0, 1e6])
plt.xlabel('total no of pixels')
plt.ylabel('count')
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'icon_pix_count.png',format='png')
fig.savefig(fig_dir + 'icon_pix_count.eps',format='eps')

fig,ax=plt.subplots()
plt.scatter(pix_count.index, pix_count/float(icon.shape[0])*100, marker='.',color='darkblue')
plt.xscale('symlog')
plt.yscale('log')
plt.xlim([-1,1e8])
plt.ylim([5*1e-6,100])
plt.xlabel('total no of pixels')
plt.ylabel('percentage of icon images')
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'icon_pix_perc.png',format='png')
fig.savefig(fig_dir + 'icon_pix_perc.eps',format='eps')

# top 20 

pix_count.sort_values(ascending = False,inplace = True)
x=range(1,21)
labels = map(str,[int(a) for a in pix_count.index[0:20]])
fig, ax = plt.subplots()
plt.bar(x,pix_count.iloc[0:20],align='center', label ='all')
plt.xticks(x, labels,rotation=70)
plt.ylabel('count')
plt.xlabel('total number of pixels,')
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'icon_pix_count_top20.png',format='png')
fig.savefig(fig_dir + 'icon_pix_count_top20.eps',format='eps')

fig, ax = plt.subplots()
plt.bar(x,pix_count.iloc[0:20]/float(icon.shape[0])*100,align='center', label ='all')
plt.xticks(x, labels,rotation=70)
plt.ylabel('percentage of icon images')
plt.xlabel('total number of pixels')
#ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'icon_pix_perc_top20.png',format='png')
fig.savefig(fig_dir + 'icon_pix_perc_top20.eps',format='eps')

# icon images - (pix,size)  count

pix_size_count = icon[['pixels','size']].groupby(['pixels','size']).size()
pix_size_count.sort_values(inplace = True)
pixels = pix_size_count.index.get_level_values(level='pixels')
size = pix_size_count.index.get_level_values(level='size')

fig,ax=plt.subplots()
plt.scatter(pixels,size,c=pix_size_count,cmap="Reds", norm=LogNorm(),edgecolors='none')
cbar = plt.colorbar()
cbar.set_label('count')
plt.xscale('symlog')
plt.yscale('log')
plt.xlim([-1,1e8])
plt.ylim([1,1e6])
plt.xlabel('total no of pixels')
plt.ylabel('file size [bytes]')
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'icon_pix_size_count.png',format='png')
fig.savefig(fig_dir + 'icon_pix_size_count.eps',format='eps')

fig,ax=plt.subplots()
plt.scatter(pixels,size,c=pix_size_count/float(icon.shape[0])*100,cmap="Reds", norm=LogNorm(),edgecolors='none')
cbar = plt.colorbar()
cbar.set_label('percentage of the icon images')
plt.xscale('symlog')
plt.yscale('log')
plt.xlim([-1,1e8])
plt.ylim([1,1e6])
plt.xlabel('total no of pixels')
plt.ylabel('file size [bytes]')
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'icon_pix_size_perc.png',format='png')
fig.savefig(fig_dir + 'icon_pix_size_perc.eps',format='eps')

# top 20 

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
fig.savefig(fig_dir + 'icon_pix_size_count_top20.png',format='png')
fig.savefig(fig_dir + 'icon_pix_size_count_top20.eps',format='eps')

fig, ax = plt.subplots()
plt.bar(x,pix_size_count.iloc[0:20]/float(icon.shape[0])*100,align='center', label ='all')
plt.xticks(x, labels,rotation=70)
plt.ylabel('percentage of the icon images')
plt.xlabel('total number of pixels, file size [bytes]')
#ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
plt.grid(True)
plt.show()
fig.savefig(fig_dir + 'icon_pix_size_perc_top20.png',format='png')
fig.savefig(fig_dir + 'icon_pix_size_perc_top20.eps',format='eps')
fig.savefig(fig_dir + 'icon_pix_size_perc_top20.jpeg',format='jpeg')


# size - length with color no of pixels - 3D


