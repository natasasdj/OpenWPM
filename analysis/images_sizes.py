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

fig1 = plt.figure(1)
plt.hist(df['size'], bins=100, color='lightblue',histtype = 'bar',label ='all')
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
'''
for i in range(1,7):
    fig_file = 'figs/img_sizes_' + str(i) +'.eps'
    s = "fig{}.savefig('".format(i) + fig_file + "',format='eps')"
    print s
    exec s
'''
for i in range(1,7):
    fig_file = 'figs/img_sizes/img_sizes_' + str(i) +'.png'
    s = "fig{}.savefig('".format(i) + fig_file + "',format='png')"
    print s
    exec s




