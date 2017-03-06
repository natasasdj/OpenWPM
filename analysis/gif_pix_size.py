import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def thousands(x, pos):
    if x>=1000:
        'The two args are the value and tick position'
        return '%dK' % (x*1e-3)
    else:
        return x
formatter = FuncFormatter(thousands)

curr_dir = os.getcwd()
res_dir = curr_dir + '/results3/'
db = res_dir + 'images.sqlite'
conn = sqlite3.connect(db)
query = 'SELECT * FROM Images'
df = pd.read_sql_query(query,conn)

gif = df[df['type'] == 5]
pix_size_count = gif[['pixels','size']].groupby(['pixels','size']).size()
pix_size_count.sort_values(inplace = True)
print pix_size_count
print type(pix_size_count)
pixels = pix_size_count.index.get_level_values(level='pixels')
size = pix_size_count.index.get_level_values(level='size')
pix_size_count_ = pix_size_count[pix_size_count > 0.001*df.shape[0]]
pixels_ = pix_size_count_.index.get_level_values(level='pixels')
size_ = pix_size_count_.index.get_level_values(level='size')

fig,ax=plt.subplots()
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
plt.scatter(pixels,size,c=pix_size_count,cmap="coolwarm", edgecolors='none',marker='.')
plt.scatter(pixels_,size_,c=pix_size_count_,cmap="coolwarm", edgecolors='none',s=50)
#plt.scatter(pixels,size,c=pix_size_count,cmap="Blues", s=50)
plt.colorbar()
plt.grid(True)
plt.xlim([-1000,100000])
plt.ylim([-1000,100000])
plt.xlabel('total no of pixels')
plt.ylabel('size')
fig.savefig('figs/gif_pixels_size_0-100k.png',format='png')
fig.savefig('figs/gif_pixels_size_0-100k.eps',format='eps')

fig,ax=plt.subplots()
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
plt.scatter(pixels,size,c=pix_size_count/float(df.shape[0]),cmap="coolwarm", edgecolors='none',marker='.')
plt.scatter(pixels_,size_,c=pix_size_count_/float(df.shape[0]),cmap="coolwarm", edgecolors='none',s=50)
#plt.scatter(pixels,size,c=pix_size_count,cmap="Blues", s=50)
plt.colorbar()
plt.grid(True)
plt.xlim([-1000,100000])
plt.ylim([-1000,100000])
plt.xlabel('total no of pixels')
plt.ylabel('size')
fig.savefig('figs/gif_pixels_size_perc_0-100k.png',format='png')
fig.savefig('figs/gif_pixels_size_perc_0-100k.eps',format='eps')

fig,ax=plt.subplots()
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
plt.scatter(pixels,size,c=pix_size_count,cmap="coolwarm", edgecolors='none', marker = '.')
plt.scatter(pixels_,size_,c=pix_size_count_,cmap="coolwarm", edgecolors='none',s= 50)
#plt.scatter(pixels,size,c=pix_size_count,cmap="Blues", s=50)
plt.colorbar()
plt.grid(True)
plt.xlim([-10,1000])
plt.ylim([-100,10000])
plt.xlabel('total no of pixels')
plt.ylabel('size')
fig.savefig('figs/gif_pixels_size_0-1k.png',format='png')
fig.savefig('figs/gif_pixels_size_0-1k.eps',format='eps')


fig,ax=plt.subplots()
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
plt.scatter(pixels,size,c=pix_size_count/float(df.shape[0]),cmap="coolwarm", edgecolors='none', marker = '.')
plt.scatter(pixels_,size_,c=pix_size_count_/float(df.shape[0]),cmap="coolwarm", edgecolors='none',s= 50)
#plt.scatter(pixels,size,c=pix_size_count,cmap="Blues", s=50)
plt.colorbar()
plt.grid(True)
plt.xlim([-10,1000])
plt.ylim([-100,10000])
plt.xlabel('total no of pixels')
plt.ylabel('size')
fig.savefig('figs/gif_pixels_size_perc_0-1k.png',format='png')
fig.savefig('figs/gif_pixels_size_perc_0-1k.eps',format='eps')

fig,ax=plt.subplots()
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
plt.scatter(pixels,size,c=pix_size_count,cmap="coolwarm", edgecolors='none', marker = '.')
plt.scatter(pixels_,size_,c=pix_size_count_,cmap="coolwarm", edgecolors='none',s= 50)
#plt.scatter(pixels,size,c=pix_size_count,cmap="Blues", s=50)
plt.colorbar()
plt.grid(True)
plt.xlim([-10,100])
plt.ylim([-100,2000])
plt.xlabel('total no of pixels')
plt.ylabel('size')
fig.savefig('figs/gif_pixels_size_0-100.png',format='png')
fig.savefig('figs/gif_pixels_size_0-100.eps',format='eps')


fig,ax=plt.subplots()
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
plt.scatter(pixels,size,c=pix_size_count/float(df.shape[0]),cmap="coolwarm", edgecolors='none', marker = '.')
plt.scatter(pixels_,size_,c=pix_size_count_/float(df.shape[0]),cmap="coolwarm", edgecolors='none',s= 50)
#plt.scatter(pixels,size,c=pix_size_count,cmap="Blues", s=50)
plt.colorbar()
plt.grid(True)
plt.xlim([-10,100])
plt.ylim([-100,2000])
plt.xlabel('total no of pixels')
plt.ylabel('size')
fig.savefig('figs/gif_pixels_size_perc_0-100.png',format='png')
fig.savefig('figs/gif_pixels_size_perc_0-100.eps',format='eps')

fig,ax=plt.subplots()
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
plt.scatter(pixels,size,c=pix_size_count,cmap="coolwarm", edgecolors='none', marker = '.')
plt.scatter(pixels_,size_,c=pix_size_count_,cmap="coolwarm", edgecolors='none', s= 50)
#plt.scatter(pixels,size,c=pix_size_count,cmap="Blues", s=50)
plt.colorbar()
plt.grid(True)
plt.xlim([0,10])
plt.ylim([0,1000])
plt.xlabel('total no of pixels')
plt.ylabel('size')
fig.savefig('figs/gif_pixels_size_0-10_1.png',format='png')
fig.savefig('figs/gif_pixels_size_0-10_1.eps',format='eps')


fig,ax=plt.subplots()
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
plt.scatter(pixels,size,c=pix_size_count/float(df.shape[0]),cmap="coolwarm", edgecolors='none', marker = '.')
plt.scatter(pixels_,size_,c=pix_size_count_/float(df.shape[0]),cmap="coolwarm", edgecolors='none', s= 50)
#plt.scatter(pixels,size,c=pix_size_count,cmap="Blues", s=50)
plt.colorbar()
plt.grid(True)
plt.xlim([0,10])
plt.ylim([0,1000])
plt.xlabel('total no of pixels')
plt.ylabel('size')
fig.savefig('figs/gif_pixels_size_perc_0-10_1.png',format='png')
fig.savefig('figs/gif_pixels_size_perc_0-10_1.eps',format='eps')

fig,ax=plt.subplots()
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
plt.scatter(pixels,size,c=pix_size_count,cmap="coolwarm", edgecolors='none', marker = '.')
plt.scatter(pixels_,size_,c=pix_size_count_,cmap="coolwarm", edgecolors='none', s= 50)
#plt.scatter(pixels,size,c=pix_size_count,cmap="Blues", s=50)
plt.colorbar()
plt.grid(True)
plt.xlim([0,10])
plt.ylim([20,60])
plt.xlabel('total no of pixels')
plt.ylabel('size')
fig.savefig('figs/gif_pixels_size_0-10_2.png',format='png')
fig.savefig('figs/gif_pixels_size_0-10_2.eps',format='eps')


fig,ax=plt.subplots()
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
plt.scatter(pixels,size,c=pix_size_count/float(df.shape[0]),cmap="coolwarm", edgecolors='none', marker = '.')
plt.scatter(pixels_,size_,c=pix_size_count_/float(df.shape[0]),cmap="coolwarm", edgecolors='none', s= 50)
#plt.scatter(pixels,size,c=pix_size_count,cmap="Blues", s=50)
plt.colorbar()
plt.grid(True)
plt.xlim([0,10])
plt.ylim([20,60])
plt.xlabel('total no of pixels')
plt.ylabel('size')
fig.savefig('figs/gif_pixels_size_perc_0-10_2.png',format='png')
fig.savefig('figs/gif_pixels_size_perc_0-10_2.eps',format='eps')

fig,ax=plt.subplots()
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
plt.scatter(pixels,size,c=pix_size_count,cmap="coolwarm", edgecolors='none')
plt.scatter(pixels_,size_,c=pix_size_count_,cmap="coolwarm", edgecolors='none',s=50)
#plt.scatter(pixels,size,c=pix_size_count,cmap="Blues", s=50)
plt.colorbar()
plt.grid(True)
plt.ylim([0,1000])
plt.xlim([20000,40000])
plt.xlabel('total no of pixels')
plt.ylabel('size')
fig.savefig('figs/gif_pixels_size_20k-40k.png',format='png')
fig.savefig('figs/gif_pixels_size_20k-40k.eps',format='eps')

fig,ax=plt.subplots()
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
plt.scatter(pixels,size,c=pix_size_count/float(df.shape[0]),cmap="coolwarm", edgecolors='none')
plt.scatter(pixels_,size_,c=pix_size_count_/float(df.shape[0]),cmap="coolwarm", edgecolors='none',s=50)
#plt.scatter(pixels,size,c=pix_size_count,cmap="Blues", s=50)
plt.colorbar()
plt.grid(True)
plt.ylim([0,1000])
plt.xlim([20000,40000])
plt.xlabel('total no of pixels')
plt.ylabel('size')
fig.savefig('figs/gif_pixels_size_perc_20k-40k.png',format='png')
fig.savefig('figs/gif_pixels_size_perc_20k-40k.eps',format='eps')

plt.show()


'''

Possible values are: Spectral, summer, coolwarm, Wistia_r, pink_r, Set1, Set2, Set3, brg_r, Dark2, prism, PuOr_r, afmhot_r, terrain_r, PuBuGn_r, RdPu, gist_ncar_r, gist_yarg_r, Dark2_r, YlGnBu, RdYlBu, hot_r, gist_rainbow_r, gist_stern, PuBu_r, cool_r, cool, gray, copper_r, Greens_r, GnBu, gist_ncar, spring_r, gist_rainbow, gist_heat_r, Wistia, OrRd_r, CMRmap, bone, gist_stern_r, RdYlGn, Pastel2_r, spring, terrain, YlOrRd_r, Set2_r, winter_r, PuBu, RdGy_r, spectral, rainbow, flag_r, jet_r, RdPu_r, gist_yarg, BuGn, Paired_r, hsv_r, bwr, cubehelix, Greens, PRGn, gist_heat, spectral_r, Paired, hsv, Oranges_r, prism_r, Pastel2, Pastel1_r, Pastel1, gray_r, jet, Spectral_r, gnuplot2_r, gist_earth, YlGnBu_r, copper, gist_earth_r, Set3_r, OrRd, gnuplot_r, ocean_r, brg, gnuplot2, PuRd_r, bone_r, BuPu, Oranges, RdYlGn_r, PiYG, CMRmap_r, YlGn, binary_r, gist_gray_r, Accent, BuPu_r, gist_gray, flag, bwr_r, RdBu_r, BrBG, Reds, Set1_r, summer_r, GnBu_r, BrBG_r, Reds_r, RdGy, PuRd, Accent_r, Blues, autumn_r, autumn, cubehelix_r, nipy_spectral_r, ocean, PRGn_r, Greys_r, pink, binary, winter, gnuplot, RdYlBu_r, hot, YlOrBr, coolwarm_r, rainbow_r, Purples_r, PiYG_r, YlGn_r, Blues_r, YlOrBr_r, seismic, Purples, seismic_r, RdBu, Greys, BuGn_r, YlOrRd, PuOr, PuBuGn, nipy_spectral, afmhot

'''




