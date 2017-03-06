import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

curr_dir = os.getcwd()
res_dir = curr_dir + '/results3/'
db = res_dir + 'images.sqlite'
conn = sqlite3.connect(db)
query = 'SELECT * FROM Images'
df = pd.read_sql_query(query,conn)
#s=df['size'][df['size']!=df['cont_length']]
grouped = df.groupby(df['type'])
s_type_count = grouped.size().sort_values(ascending=False)
df_type_count = pd.DataFrame(s_type_count,columns=['count'])
#df1=df[df['pixels']==1]
#df1.shape[0]/df.shape[0]
#grouped1 = df1.groupby(df1['type'])
#s1_type_count = grouped1.size().sort_values(ascending=False)
#df1_type_count = pd.DataFrame(s1_type_count,columns=['count'])

#print df_type_count_
#print pd.merge(df1_type_count, t, left_index=True, right_on='id')
max_pixels = df['pixels'].max()
#print df['pixels'].max()

#print s_type_count.index
#print s_type_count


#print x
#print df_type_count_.index

#print labels


df_err = df.ix[pd.isnull(df['pixels'])]
print df_err.head()
grouped = df.groupby(df_err['type']) 
df_err_type_count = pd.DataFrame(grouped.size().sort_values(ascending=False),columns=['count'])


for t in df_type_count.index:
    if t in df_err_type_count.index:
        df_type_count.ix[t,'err_count'] = df_err_type_count.ix[t,'count']
    else:
        df_type_count.ix[t,'err_count'] = 0

print df_type_count

query = 'SELECT * FROM Types'
types = pd.read_sql_query(query,conn)
df_type_count_ = pd.merge(df_type_count, types, left_index=True, right_on='id')
print df_type_count_
df_type_count_['type']=map(lambda x: str(x.split("/")[1]),df_type_count_['type'])
print df_type_count_

x=range(1,2*df_type_count_.shape[0]+1,2)
labels = list(df_type_count_['type'])
fig=plt.figure()
ok=plt.bar(x,df_type_count_['count'],align='center')
err=plt.bar(x,df_type_count_['err_count'],color='lightblue',align='center',label = 'error')
plt.xticks(x, labels,rotation=70)
plt.legend(handles=[err])
plt.ylabel('number of images')
fig.savefig('figs/img_types_count.png',format='png')
fig.savefig('figs/img_types_count.eps',format='eps')

fig=plt.figure()
plt.bar(x,df_type_count_['count']/df.shape[0],align='center')
err=plt.bar(x,df_type_count_['err_count']/df.shape[0],color='lightblue',align='center',label = 'error')
plt.xticks(x, labels,rotation=70)
plt.legend(handles=[err])
plt.ylabel('percentage of images')
fig.savefig('figs/img_types_perc.png',format='png')
fig.savefig('figs/img_types_perc.eps',format='eps')

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



from matplotlib.ticker import FuncFormatter


def thousands(x, pos):
    if x>=1000:
        'The two args are the value and tick position'
        return '%dK' % (x*1e-3)
    else:
        return x

formatter = FuncFormatter(thousands)

grouped = df.groupby('pixels')
s_pix_count = grouped.size()
df_pix_count = pd.DataFrame(s_pix_count,columns=['count'])
grouped = df.groupby(['pixels','type'])
s_pix_type_count = grouped.size()
df_pix_type_count = pd.DataFrame(s_type_count,columns=['count'])
print "s_pix_type_count"
print s_pix_type_count
print "df_pix_count"
print df_pix_count.head()

'''
start=0
end = 100000
n = end-start +1
pix_count = [0] * n
jpeg_count = [0] * n
png_count = [0] * n
gif_count = [0] * n
icon_count = [0] * n
plain_count = [0] * n
x_=range(start,end +1)
for i in x_:
    if i%10000==0: print i
    if i in df_pix_count.index:
        pix_count[i] = s_pix_count[i]
        #if pix_count[i] > 300:
           #pix_c.append(pix_count[i])
           #pix_x.append(i)
        #print i, " 0 ", pix_count[i]
    try: 
        jpeg_count[i] = s_pix_type_count[i,2]
        #print i, " 1 ", jpeg_count[i]
    except: pass
    try: 
        gif_count[i]  = s_pix_type_count[i,5] 
    except: pass
    try: 
        png_count[i] = s_pix_type_count[i,1] 
    except: pass
    try: 
        icon_count[i] = s_pix_type_count[i,3] 
    except: pass
    try: 
        plain_count[i] = s_pix_type_count[i,7] 
    except: pass
    # jpeg 2 gif 5 png 1 icon 3 plain 7 
         
def sumzip(*items):
    return [sum(values) for values in zip(*items)]

s=0
e=10

def plot_pix_type(s,e,width=0.8):
    x=range(s,e+1)
    pix = pix_count[s:e+1]
    jpeg = jpeg_count[s:e+1]
    gif = gif_count[s:e+1]
    png = png_count[s:e+1]
    icon = icon_count[s:e+1]
    plain = plain_count[s:e+1]
    
    fig,ax=plt.subplots()
    ax.yaxis.set_major_formatter(formatter)
    plt.bar(x,pix,align='center',width=width)
    jpeg_=plt.bar(x,jpeg,color='lightblue',align='center',label = 'jpeg',width=width)
    gif_=plt.bar(x,gif,color='red',bottom=sumzip(jpeg),align='center',label = 'gif',width=width)
    png_=plt.bar(x,png,color='yellow',bottom=sumzip(jpeg,gif),align='center',label = 'png',width=width)
    icon_=plt.bar(x,icon,color='green',bottom=sumzip(jpeg,gif,png),align='center',label = 'icon',width=width)
    plain_=plt.bar(x,plain,color='black',bottom=sumzip(jpeg,gif,png,icon),align='center',label = 'plain',width=width)
    plt.legend(handles=[jpeg_,gif_,png_,icon_,plain_])
    plt.xlabel('total number of pixels')
    plt.ylabel('number of images')
    plt.grid(True)
    fig.savefig('figs/img_pix_types_count_'+str(s)+'-'+str(e)+'.png',format='png')
    fig.savefig('figs/img_pix_types_count_'+str(s)+'-'+str(e)+'.eps',format='eps')    

    fig,ax=plt.subplots()
    ax.yaxis.set_major_formatter(formatter)
    pix_perc = map(lambda k: float(k)/df.shape[0],pix)
    jpeg_perc = map(lambda k: float(k)/df.shape[0],jpeg)
    gif_perc = map(lambda k: float(k)/df.shape[0],gif)
    png_perc = map(lambda k: float(k)/df.shape[0],png)
    icon_perc = map(lambda k: float(k)/df.shape[0],icon)
    plain_perc = map(lambda k: float(k)/df.shape[0],plain)
    plt.bar(x,pix_perc,align='center',width=width)
    jpeg_=plt.bar(x,jpeg_perc,color='lightblue',align='center',label = 'jpeg',width=width)
    gif_=plt.bar(x,gif_perc,color='red',bottom=sumzip(jpeg_perc),align='center',label = 'gif',width=width)
    png_=plt.bar(x,png_perc,color='yellow',bottom=sumzip(jpeg_perc,gif_perc),align='center',label = 'png',width=width)
    icon_=plt.bar(x,icon_perc,color='green',bottom=sumzip(jpeg_perc,gif_perc,png_perc),align='center',label = 'icon',width=width)
    plain_=plt.bar(x,plain_perc,color='black',bottom=sumzip(jpeg_perc,gif_perc,png_perc,icon_perc),align='center',label = 'plain',width=width)
    plt.legend(handles=[jpeg_,gif_,png_,icon_,plain_])
    plt.xlabel('total number of pixels')
    plt.ylabel('number of images')
    plt.grid(True)
    fig.savefig('figs/img_pix_types_perc_'+str(s)+'-'+str(e)+'.png',format='png')
    fig.savefig('figs/img_pix_types_perc_'+str(s)+'-'+str(e)+'.eps',format='eps') 
 
print "0,10"
plot_pix_type(0,10)
print "10,100"
plot_pix_type(10,100)
print "10,100"
plot_pix_type(0,100)

'''



fig,ax=plt.subplots()
#s_pix_count_ = s_pix_count[1000:100000]
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
s_pix_count_ = s_pix_count[100:100000]
plt.scatter(s_pix_count_.index,s_pix_count_,marker='.',color='darkblue',alpha = 0.3)
s_pix_count_lim = s_pix_count_[s_pix_count_ > 0.01*df.shape[0]]
plt.scatter(s_pix_count_lim.index,s_pix_count_lim)
plt.xlabel('total number of pixels')
plt.ylabel('number of images')
plt.xlim([-1000,100000])
plt.grid(True)
fig.savefig('figs/img_pix_count_100-100k.png',format='png')
fig.savefig('figs/img_pix_count_100-100k.eps',format='eps')

s_pix_count_=s_pix_count_/float(df.shape[0])
fig,ax=plt.subplots()
#s_pix_count_ = s_pix_count[1000:100000]
ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
plt.scatter(s_pix_count_.index,s_pix_count_,marker='.',color='darkblue',alpha = 0.3)
s_pix_count_lim = s_pix_count_[s_pix_count_ > 0.01]
plt.scatter(s_pix_count_lim.index,s_pix_count_lim)
plt.xlabel('total number of pixels')
plt.ylabel('number of images')
plt.xlim([-1000,100000])
#plt.ylim([0,10000])
plt.grid(True)
fig.savefig('figs/img_pix_perc_100-100k.png',format='png')
fig.savefig('figs/img_pix_perc_100-100k.eps',format='eps')

print s_pix_count[s_pix_count > 0.01*df.shape[0]].index




plt.show()

'''
for t in df_type_count_['id']:

    print "type",t," ", df_type_count_[df_type_count_['id']==t]['type']  
      
    #print df_type_count_.ix([t,'count'])  
    d = df[df['type']==t]
    #print "ddddd", d.head()
    print "size of d",d.shape[0]  
    pix_t_count = df[df['type']==t].groupby(['pixels']).size()
    print "pix_t_count size",pix_t_count.size
    print pix_t_count
    #print type(pix_t_count)
    #print pix_t_count.index
    #print pix_t_count
    fig = plt.figure()
    plt.scatter(pix_t_count.index,pix_t_count)
    
    plt.title(df_type_count_[df_type_count_['id']==t]['type'])
    #plt.xlim([0,10000])
    #plt.ylim([0,10000])
'''

'''
jpeg = df[df['type'] == 2]
jpeg1 = df1[df1['type'] == 2]

fig1 = plt.figure(1)
plt.scatter( jpeg['pixels'], jpeg['size'],alpha=0.01)
plt.title(' No of Pixels vs Size\nno of sites = 100, max no of links = 300')
plt.xlabel('no of pixels')
plt.ylabel('size [bytes]')
plt.xlim([0,100000])
plt.ylim([0,100000])
plt.grid(True)
fig1.savefig('jpeg_pixels_size.png',format='png')
fig1.savefig('jpeg_pixels_size.eps',format='eps')

fig2 = plt.figure(2)
plt.scatter( jpeg['pixels'], jpeg['size'],alpha=0.01)
plt.title(' Size vs No of Pixels\nno of sites = 100, max no of links = 300')
plt.ylabel('size [bytes]')
plt.xlabel('no of pixels')
plt.xlim([0,3000])
plt.ylim([0,10000])
plt.grid(True)
fig1.savefig('jpeg_pixels_size_3k.png',format='png')
fig1.savefig('jpeg_pixels_size_3k.eps',format='eps')

fig3 = plt.figure(3)
plt.scatter( jpeg['pixels'], jpeg['size'],alpha=0.01)
plt.title(' Size vs No of Pixels\nno of sites = 100, max no of links = 300')
plt.ylabel('size [bytes]')
plt.xlabel('no of pixels')
plt.xlim([0,100])
plt.ylim([0,1000])
plt.grid(True)
fig1.savefig('jpeg_pixels_size_100.png',format='png')
fig1.savefig('jpeg_pixels_size_100.eps',format='eps')

fig4 = plt.figure(4)
plt.scatter( jpeg1['pixels'], jpeg1['size'],alpha=0.01)
plt.title(' No of Pixels vs Size\nno of sites = 100, max no of links = 300')
plt.xlabel('no of pixels')
plt.ylabel('size [bytes]')
plt.xlim([0,5])
plt.ylim([0,1000])
plt.grid(True)
fig1.savefig('jpeg_1pixel_size.png',format='png')
fig1.savefig('jpeg_1pixel_size.eps',format='eps')


gif = df[df['type'] == 5]
gif1 = df1[df1['type'] == 5]

fig1 = plt.figure(1)
plt.scatter( gif['pixels'], gif['size'],alpha=0.01)
plt.title(' No of Pixels vs Size\nno of sites = 100, max no of links = 300')
plt.xlabel('no of pixels')
plt.ylabel('size [bytes]')
plt.xlim([0,100000])
plt.ylim([0,100000])
plt.grid(True)
fig1.savefig('gif_pixels_size.png',format='png')
fig1.savefig('gif_pixels_size.eps',format='eps')

fig2 = plt.figure(2)
plt.scatter( gif['pixels'], gif['size'],alpha=0.01)
plt.title(' Size vs No of Pixels\nno of sites = 100, max no of links = 300')
plt.ylabel('size [bytes]')
plt.xlabel('no of pixels')
plt.xlim([0,3000])
plt.ylim([0,10000])
plt.grid(True)
fig1.savefig('gif_pixels_size_3k.png',format='png')
fig1.savefig('gif_pixels_size_3k.eps',format='eps')

fig3 = plt.figure(3)
plt.scatter( gif['pixels'], gif['size'],alpha=0.01)
plt.title(' Size vs No of Pixels\nno of sites = 100, max no of links = 300')
plt.ylabel('size [bytes]')
plt.xlabel('no of pixels')
plt.xlim([0,50])
plt.ylim([0,1000])
plt.grid(True)
fig1.savefig('gif_pixels_size_100.png',format='png')
fig1.savefig('gif_pixels_size_100.eps',format='eps')

fig4 = plt.figure(4)
plt.scatter( gif1['pixels'], gif1['size'],alpha=0.01)
plt.title(' No of Pixels vs Size\nno of sites = 100, max no of links = 300')
plt.xlabel('no of pixels')
plt.ylabel('size [bytes]')
plt.xlim([0,5])
plt.ylim([0,1000])
plt.grid(True)
fig1.savefig('gif_1pixel_size.png',format='png')
fig1.savefig('gif_1pixel_size.eps',format='eps')
'''
'''
#print gif.head()
pix_size_count = gif[['pixels','size']].groupby(['pixels','size']).size()
pix_size_count.sort_values(inplace = True)
print pix_size_count
print type(pix_size_count)
#print pix_size_count.name
#print pix_size_count.head()
#print pix_size_count.index
#print pix_size_count.index.names
#print type(pix_size_count.index.get_level_values(level='pixels'))
pixels = pix_size_count.index.get_level_values(level='pixels')
size = pix_size_count.index.get_level_values(level='size')
p=pixels[0:10]
s=size[0:10]
c1=pix_size_count[0:10]
fig = plt.figure(5)
count_proc = pix_size_count/pix_size_count.sum()
c2=count_proc[0:10]
#print p
#print s
#print c1
#print c2
#plt.scatter( p, s, c = c2,s=50)
print pix_size_count[pix_size_count.index.get_level_values('pixels') == 2]
print pix_size_count[pix_size_count.index.get_level_values('pixels') == 1]
#plt.scatter(pixels,size,c=count_proc)
plt.scatter(pixels,size,c=pix_size_count,cmap="summer_r", edgecolors='none')
#plt.scatter(pixels,size,c=pix_size_count,cmap="Blues", s=50)
plt.colorbar()
#plt.gray()
plt.xlim([0,1000])
plt.ylim([0,10000])
#plt.show()
#print pix_size_count.values()

fig = plt.figure(6)
# Plot...
plt.scatter(pixels,size,c=count_proc,cmap="summer_r", edgecolors='none',s=100)
plt.colorbar()
#plt.gray()
plt.xlim([0,100])
plt.ylim([0,1000])
plt.show()

fig = plt.figure(7)
# Plot...
plt.scatter(pixels,size,c=count_proc,cmap="summer_r", edgecolors='none',s=100)
plt.colorbar()
#plt.gray()
plt.xlim([0,10])
plt.ylim([0,100])
plt.show()
'''

'''
pix_count = gif[['pixels']].groupby(['pixels']).size()


fig = plt.figure()
plt.scatter(pix_count.index,pix_count)

fig = plt.figure()
plt.scatter(pix_count.index,pix_count/pix_count.sum())

fig = plt.figure()
plt.scatter(pix_count.index,pix_count)
plt.xlim([-10,100])
#plt.ylim([0,10000])

fig = plt.figure()
plt.scatter(pix_count.index,pix_count/pix_count.sum())
plt.xlim([-10,100])
#plt.ylim([0,10000])

fig = plt.figure()
plt.scatter(pix_count.index,pix_count)
plt.xlim([-2,10])
#plt.ylim([0,10000])

fig = plt.figure()
plt.scatter(pix_count.index,pix_count/pix_count.sum())
plt.xlim([-2,10])

 
fig = plt.figure()
plt.scatter(pix_count.index, pix_count.cumsum()/pix_count.sum())
plt.xlim([-100,100000])

fig = plt.figure()
plt.scatter(pix_count.index, pix_count.cumsum()/pix_count.sum())
plt.xlim([-100,10000])

fig = plt.figure()
plt.scatter(pix_count.index, pix_count.cumsum()/pix_count.sum())
plt.xlim([-10,1000])

fig = plt.figure()
plt.scatter(pix_count.index, pix_count.cumsum()/pix_count.sum())
plt.xlim([-10,100])

fig = plt.figure()
plt.scatter(pix_count.index,pix_count.cumsum()/pix_count.sum())
plt.xlim([-2,10])

 '''

#plt.show()

'''
import numpy as np
#from matplotlib import cm 
fig = plt.figure(5)
#gridsize = 100
#plt.hexbin(gif1['pixels'], gif1['size'], cmap=cm.jet, bins=None)
plt.scatter( gif1['pixels'], gif1['size'],col=pix_size_count)
#heatmap, xedges, yedges = np.histogram2d(gif1['pixels'], gif1['size'], bins=50)
#extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
#plt.clf()
#plt.imshow(heatmap.T, extent=extent, origin='lower')

plt.title(' No of Pixels vs Size\nno of sites = 100, max no of links = 300')
plt.xlabel('no of pixels')
plt.ylabel('size [bytes]')
plt.xlim([0,5])
plt.ylim([0,1000])
plt.grid(True)
fig.savefig('gif_1pixel_size.png',format='png')
fig.savefig('gif_1pixel_size.eps',format='eps')

plt.show()

Possible values are: Spectral, summer, coolwarm, Wistia_r, pink_r, Set1, Set2, Set3, brg_r, Dark2, prism, PuOr_r, afmhot_r, terrain_r, PuBuGn_r, RdPu, gist_ncar_r, gist_yarg_r, Dark2_r, YlGnBu, RdYlBu, hot_r, gist_rainbow_r, gist_stern, PuBu_r, cool_r, cool, gray, copper_r, Greens_r, GnBu, gist_ncar, spring_r, gist_rainbow, gist_heat_r, Wistia, OrRd_r, CMRmap, bone, gist_stern_r, RdYlGn, Pastel2_r, spring, terrain, YlOrRd_r, Set2_r, winter_r, PuBu, RdGy_r, spectral, rainbow, flag_r, jet_r, RdPu_r, gist_yarg, BuGn, Paired_r, hsv_r, bwr, cubehelix, Greens, PRGn, gist_heat, spectral_r, Paired, hsv, Oranges_r, prism_r, Pastel2, Pastel1_r, Pastel1, gray_r, jet, Spectral_r, gnuplot2_r, gist_earth, YlGnBu_r, copper, gist_earth_r, Set3_r, OrRd, gnuplot_r, ocean_r, brg, gnuplot2, PuRd_r, bone_r, BuPu, Oranges, RdYlGn_r, PiYG, CMRmap_r, YlGn, binary_r, gist_gray_r, Accent, BuPu_r, gist_gray, flag, bwr_r, RdBu_r, BrBG, Reds, Set1_r, summer_r, GnBu_r, BrBG_r, Reds_r, RdGy, PuRd, Accent_r, Blues, autumn_r, autumn, cubehelix_r, nipy_spectral_r, ocean, PRGn_r, Greys_r, pink, binary, winter, gnuplot, RdYlBu_r, hot, YlOrBr, coolwarm_r, rainbow_r, Purples_r, PiYG_r, YlGn_r, Blues_r, YlOrBr_r, seismic, Purples, seismic_r, RdBu, Greys, BuGn_r, YlOrRd, PuOr, PuBuGn, nipy_spectral, afmhot

'''




