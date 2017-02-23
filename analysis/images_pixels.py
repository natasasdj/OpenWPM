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
s=df['size'][df['size']!=df['cont_length']]
l=s.tolist()
df['pixels'].fillna(value=-100,inplace=True)


fig1 = plt.figure(1)
plt.scatter( df['pixels'], df['size'],alpha=0.01)
plt.title(' No of Pixels vs Size\nno of sites = 100, max no of links = 300')
plt.xlabel('no of pixels')
plt.ylabel('size [bytes]')
plt.xlim([0,1000000])
plt.ylim([0,110000])

fig2 = plt.figure(2)
plt.scatter( df['pixels'], df['size'],alpha=0.01)
plt.title(' Size vs No of Pixels\nno of sites = 100, max no of links = 300')
plt.ylabel('size [bytes]')
plt.xlabel('no of pixels')
plt.xlim([0,10])
plt.ylim([0,3000])

fig3 = plt.figure(3)
plt.scatter( df['pixels'], df['size'],alpha=0.01)
plt.title(' Size vs No of Pixels\nno of sites = 100, max no of links = 300')
plt.ylabel('size [bytes]')
plt.xlabel('no of pixels')
plt.xlim([0,10])
plt.ylim([0,200])

fig4 = plt.figure(4)
plt.scatter(df['pixels'],df['cont_length'],  alpha=0.02)
plt.title(' Content-length vs No of Pixels\nno of sites = 100, max no of links = 300')
plt.ylabel('content-length [bytes]')
plt.xlabel('no of pixels')
plt.xlim([0,1000000])
plt.ylim([0,110000])

fig5 = plt.figure(5)
plt.scatter(df['pixels'],df['cont_length'],  alpha=0.02)
plt.title(' Content-length vs No of Pixels\nno of sites = 100, max no of links = 300')
plt.ylabel('content-length [bytes]')
plt.xlabel('no of pixels')
plt.xlim([0,10])
plt.ylim([0,3000])

fig6 = plt.figure(6)
plt.scatter(df['pixels'],df['cont_length'],  alpha=0.02)
plt.title(' Content-length vs No of Pixels\nno of sites = 100, max no of links = 300')
plt.ylabel('content-length [bytes]')
plt.xlabel('no of pixels')
plt.xlim([0,10])
plt.ylim([0,200])


pix_counts = df['pixels'].value_counts()
total = df.shape[0]
pix_perc = pix_counts/float(total)
pix_perc_cum = pix_perc.cumsum()

fig7 = plt.figure(7)
plt.scatter(pix_perc.index,pix_perc)
#plt.scatter(pix_counts.index,pix_counts)
plt.title('Image Counts for No of Pixels\nno of sites = 100, max no of links = 300')
plt.xlabel('no of pixels')
plt.ylabel('percentage of images')
plt.xlim([-1000,80000])
plt.grid(True)

fig8 = plt.figure(8)
plt.scatter(pix_perc.index,pix_perc)
#plt.scatter(pix_counts.index,pix_counts)
plt.title('Image Counts for No of Pixels\nno of sites = 100, max no of links = 300')
plt.xlabel('no of pixels')
plt.ylabel('percentage of images')
plt.xlim([-200,2000])
plt.grid(True)

fig9 = plt.figure(9)
plt.scatter(pix_perc.index,pix_perc)
#plt.scatter(pix_counts.index,pix_counts)
plt.title('Image Counts for No of Pixels\nno of sites = 100, max no of links = 300')
plt.xlabel('no of pixels')
plt.ylabel('percentage of images')
plt.xlim([-200,100])
plt.grid(True)

'''
fig10 = plt.figure(10)
plt.plot(pix_perc_cum)
#plt.scatter(pix_counts.index,pix_counts)
plt.title('Image Counts for No of Pixels\nno of sites = 100, max no of links = 300')
plt.xlabel('no of pixels')
plt.ylabel('percentage of images')
#plt.xlim([-200,100000])

fig11 = plt.figure(11)
plt.plot(pix_perc_cum)
#plt.scatter(pix_counts.index,pix_counts)
plt.title('Image Counts for No of Pixels\nno of sites = 100, max no of links = 300')
plt.xlabel('no of pixels')
plt.ylabel('percentage of images')
plt.xlim([-200,2000])

fig12 = plt.figure(12)
plt.plot(pix_perc_cum,marker='o')
#plt.scatter(pix_counts.index,pix_counts)
plt.title('Image Counts for No of Pixels\nno of sites = 100, max no of links = 300')
plt.xlabel('no of pixels')
plt.ylabel('percentage of images')
plt.xlim([-200,100])
'''

#plt.show()
'''
for i in range(1,10):
    fig_file = 'figs/img_pixels_' + str(i) +'.eps'
    s = "fig{}.savefig('".format(i) + fig_file + "',format='eps')"
    print s
    exec s
'''
for i in range(1,10):
    fig_file = 'figs/img_pixels/img_pixels_' + str(i) +'.png'
    s = "fig{}.savefig('".format(i) + fig_file + "',format='png')"
    print s
    exec s








