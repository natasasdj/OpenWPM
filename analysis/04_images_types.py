import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

res_dir = '/home/nsarafij/project/OpenWPM/analysis/results/'
db = res_dir + 'images.sqlite'
conn = sqlite3.connect(db)
query = 'SELECT * FROM Images'
df = pd.read_sql_query(query,conn)
grouped = df.groupby(df['type'])
s_type_count = grouped.size().sort_values(ascending=False)
df_type_count = pd.DataFrame(s_type_count,columns=['count'])

df_err = df.ix[pd.isnull(df['pixels'])]
grouped = df.groupby(df_err['type']) 
df_err_type_count = pd.DataFrame(grouped.size().sort_values(ascending=False),columns=['count'])
for t in df_type_count.index:
    if t in df_err_type_count.index:
        df_type_count.ix[t,'err_count'] = df_err_type_count.ix[t,'count']
    else:
        df_type_count.ix[t,'err_count'] = 0

#print df_type_count

query = 'SELECT * FROM Types'
types = pd.read_sql_query(query,conn)
df_type_count_ = pd.merge(df_type_count, types, left_index=True, right_on='id')
#print df_type_count_
df_type_count_['type']=map(lambda x: str(x.split("/")[1]),df_type_count_['type'])
df_type_count_['type']=df_type_count_['type'].apply(lambda x: re.split(r'[;,]',x,maxsplit=1)[0])
df_type_count_['type']=df_type_count_['type'].apply(lambda x: x.replace('jpg','jpeg')
df_type_count_= df_type_count_.groupby('type').sum().sort_values(by='count',ascending=False)
#print df_type_count_

x=range(1,2*df_type_count_.shape[0]+1,2)
labels = list(df_type_count_.index)

fig_dir = '/home/nsarafij/project/OpenWPM/analysis/figs/'



fig=plt.figure()
ok=plt.bar(x,df_type_count_['count'],align='center')
err=plt.bar(x,df_type_count_['err_count'],color='lightblue',align='center',label = 'error')
plt.xticks(x, labels,rotation=70)
plt.legend(handles=[err])
#plt.xlabel('file type')
plt.ylabel('number of images')
fig.tight_layout()
#plt.show()
fig.savefig(fig_dir+'types_count.png',format='png')
fig.savefig(fig_dir+'types_count.eps',format='eps')

fig=plt.figure()
plt.bar(x,df_type_count_['count']/df.shape[0],align='center')
err=plt.bar(x,df_type_count_['err_count']/df.shape[0],color='lightblue',align='center',label = 'error')
plt.xticks(x, labels,rotation=70)
plt.legend(handles=[err])
plt.ylabel('percentage of total number of images')
fig.tight_layout()
plt.show()
fig.savefig(fig_dir+'types_perc.png',format='png')
fig.savefig(fig_dir+'types_perc.eps',format='eps')


'''
fig=plt.figure()
plt.bar(x,df_type_count_['err_count'],color='lightblue',align='center',label = 'error')
plt.xticks(x, labels,rotation=70)
plt.ylabel('number of images')
fig.savefig('figs/img_err_types_count.png',format='png')
fig.savefig('figs/img_err_types_count.eps',format='eps')

fig=plt.figure()
plt.bar(x,df_type_count_['err_count']/df_type_count_['count'],color='lightblue',align='center',label = 'error')
plt.xticks(x, labels,rotation=70)
plt.ylabel('percentage of images')
fig.savefig('figs/img_err_types_perc.png',format='png')
fig.savefig('figs/img_err_types_perc.eps',format='eps')
'''





'''
Possible values are: Spectral, summer, coolwarm, Wistia_r, pink_r, Set1, Set2, Set3, brg_r, Dark2, prism, PuOr_r, afmhot_r, terrain_r, PuBuGn_r, RdPu, gist_ncar_r, gist_yarg_r, Dark2_r, YlGnBu, RdYlBu, hot_r, gist_rainbow_r, gist_stern, PuBu_r, cool_r, cool, gray, copper_r, Greens_r, GnBu, gist_ncar, spring_r, gist_rainbow, gist_heat_r, Wistia, OrRd_r, CMRmap, bone, gist_stern_r, RdYlGn, Pastel2_r, spring, terrain, YlOrRd_r, Set2_r, winter_r, PuBu, RdGy_r, spectral, rainbow, flag_r, jet_r, RdPu_r, gist_yarg, BuGn, Paired_r, hsv_r, bwr, cubehelix, Greens, PRGn, gist_heat, spectral_r, Paired, hsv, Oranges_r, prism_r, Pastel2, Pastel1_r, Pastel1, gray_r, jet, Spectral_r, gnuplot2_r, gist_earth, YlGnBu_r, copper, gist_earth_r, Set3_r, OrRd, gnuplot_r, ocean_r, brg, gnuplot2, PuRd_r, bone_r, BuPu, Oranges, RdYlGn_r, PiYG, CMRmap_r, YlGn, binary_r, gist_gray_r, Accent, BuPu_r, gist_gray, flag, bwr_r, RdBu_r, BrBG, Reds, Set1_r, summer_r, GnBu_r, BrBG_r, Reds_r, RdGy, PuRd, Accent_r, Blues, autumn_r, autumn, cubehelix_r, nipy_spectral_r, ocean, PRGn_r, Greys_r, pink, binary, winter, gnuplot, RdYlBu_r, hot, YlOrBr, coolwarm_r, rainbow_r, Purples_r, PiYG_r, YlGn_r, Blues_r, YlOrBr_r, seismic, Purples, seismic_r, RdBu, Greys, BuGn_r, YlOrRd, PuOr, PuBuGn, nipy_spectral, afmhot

'''




