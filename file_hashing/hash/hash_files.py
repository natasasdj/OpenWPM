import hashlib
import os
import pandas as pd
import sqlite3 
import matplotlib.pyplot as plt

def file_hash(fname):
    with open(fname, "rb") as fhand:
        hasher = hashlib.md5()
        buf = fhand.read()
        hasher.update(buf)
        return hasher.hexdigest()

db_file='/home/nsarafij/project/data/output_001/crawl-data.sqlite'
conn = sqlite3.connect(db_file)

ferr = '/home/nsarafij/project/hash/data/err_001.txt'
ferr_hand = open(ferr, "w")


img_dict={}
html_dict={}
for site in range(1,101):
    query = 'SELECT * FROM site_visits WHERE site_id = ' +str(site)
    df = pd.read_sql_query(query,conn)
    if len(df.index)==0:
        '**********************************************' 
        continue 
    print site
    site_dir = '/home/nsarafij/project/data/output_001/httpResp/' +'site-'+ str(site) + '/'
    k=0
    if not os.path.exists(site_dir): continue
    for fname in os.listdir(site_dir):
        k=k+1
        if k%1000 ==0: print k
        fpath = site_dir+fname
        fhash = file_hash(fpath)
        s = fname + ' ' + fhash + '\n'
        #fhand.write(s)
        size = os.path.getsize(fpath)
        if fname.endswith("html"): 
            if fhash in html_dict:
                if html_dict[fhash]['size'] == size:
                    #html_dict[fhash]['files'].append(fname)
                    html_dict[fhash]['no_files'] += 1
                else:
                    ferr_hand.write(fhash + ' ' + fname + ' ' + size + '\n')                            
            else:
                html_dict[fhash] = {'size':size,'files':[fname],'no_files':1}
        else: 
            if fhash in img_dict:
                if img_dict[fhash]['size'] == size:
                    #img_dict[fhash]['files'].append(fname)
                    img_dict[fhash]['no_files'] += 1
                else:
                    ferr_hand.write(fhash + ' ' + fname + ' ' + size + '\n')                            
            else:
                img_dict[fhash] = {'size':size,'files':[fname],'no_files':1}
 
ferr_hand.close()
conn.close()
            
img_no_files =[] 
img_sizes = []
img_files = []
for val in img_dict.values():
    img_no_files.append(val['no_files'])
    img_sizes.append(val['size'])
    img_files.append(val['files'][0]) 

html_no_files =[] 
html_sizes = []
html_files = []           
for val in html_dict.values():
    html_no_files.append(val['no_files'])    
    html_sizes.append(val['size']) 
    html_files.append(val['files'][0])
 
import itertools
def glance(d):
    return dict(itertools.islice(d.iteritems(), 3))      

img = pd.DataFrame({'size':img_sizes,'count':img_no_files,'file':img_files})
html = pd.DataFrame({'size':html_sizes,'count':html_no_files, 'file':html_files})
img.sort_values(by='count',ascending=False,inplace=True)
html.sort_values(by='count',ascending=False,inplace=True)


img_out = '/home/nsarafij/project/hash/data/img_001.txt'
img_hand = open(img_out, "w")
html_out = '/home/nsarafij/project/hash/data/html_001.txt'
html_hand = open(html_out, "w")

for index, row in img.iterrows():
    img_hand.write(str(row['size']) + ' ' + str(row['count']) + ' ' +row['file'] + ' \n')

for index, row in html.iterrows():
    html_hand.write(str(row['size']) + ' ' + str(row['count']) + ' ' + row['file'] + '\n')

img_hand.close()
html_hand.close()

#change directory
#import os
#os.chdir(path)
#os.getcwd()

fig=plt.figure()
plt.scatter(img['size'],img['count'],marker='o')
plt.title('Images with the same MD5 hashes')
plt.xscale('symlog')
plt.yscale('symlog')
plt.xlabel('file size [bytes]')
plt.ylabel('count')
plt.xlim([-1,1e6])
plt.ylim([0,1e5])
plt.grid(True)
fig.savefig("figs/img_hash_size.png",format='png')
fig.savefig("figs/img_hash_size.eps",format='eps')
plt.show()

fig=plt.figure()
plt.scatter(html['size'],html['count'],marker='o')
plt.title('Html files with the same MD5 hashes')
plt.xscale('symlog')
plt.yscale('symlog')
plt.xlabel('file size [bytes]')
plt.ylabel('count')
plt.xlim([-1,1e9])
plt.ylim([0,1e5])
plt.grid(True)
fig.savefig("figs/html_hash_size.png",format='png')
fig.savefig("figs/html_hash_size.eps",format='eps')
plt.show()


img1 = pd.DataFrame({'size':img['size'],'count':img['count']-1,'file':img_files})
img1 = img1[img1['count']>0]
img_save = img1.groupby('size').agg({'count':sum,'file':lambda x: " ".join(x.tolist())})
img_save['saving'] =  img_save['count']*img_save.index
img_save['cumsum'] = img_save['saving'].cumsum()
img_save = img_save[['count','saving','cumsum','file']]

html1=pd.DataFrame({'size':html['size'],'count':html['count']-1,'file':html_files})
html1 = html1[html1['count']>0]
html_save = html1.groupby('size').agg({'count':sum,'file':lambda x: " ".join(x.tolist())})
html_save['saving'] =  html_save['count']*html_save.index
html_save['cumsum'] = html_save['saving'].cumsum()
html_save = html_save[['count','saving','cumsum','file']]

img_save_sort = img_save.sort_values(by = 'saving', ascending =False)
html_save_sort = html_save.sort_values(by = 'saving', ascending =False)


img_out = '/home/nsarafij/project/hash/data/img_saving_001.txt'
img_hand = open(img_out, "w")
html_out = '/home/nsarafij/project/hash/data/html_saving_001.txt'
html_hand = open(html_out, "w")

for index, val in img_save.iterrows():
    img_hand.write(str(index) + ' ' + str(val['count']) + ' ' + str(val['saving']) + ' '+ str(val['cumsum']) + ' ' + val['file'] + ' \n')

for index, val in html_save.iterrows():
    html_hand.write(str(index) + ' ' + str(val['count']) + ' ' + str(val['saving']) + ' '+ str(val['cumsum']) + ' ' + val['file'] + ' \n')

img_hand.close()
html_hand.close()

img_save_sort = img_save.sort_values(by='saving', ascending =False)
img_save_sort['cumsum'] = img_save_sort['saving'].cumsum()
html_save_sort = html_save.sort_values(by='saving', ascending = False)
html_save_sort['cumsum'] = html_save_sort['saving'].cumsum()

img_out = '/home/nsarafij/project/hash/data/img_saving_sort_001.txt'
img_hand = open(img_out, "w")
html_out = '/home/nsarafij/project/hash/data/html_saving_sort_001.txt'
html_hand = open(html_out, "w")

for index, val in img_save_sort.iterrows():
    img_hand.write(str(index) + ' ' + str(val['count']) + ' ' + str(val['saving']) + ' '+ str(val['cumsum']) + ' ' + val['file'] + ' \n')

for index, val in html_save_sort.iterrows():
    html_hand.write(str(index) + ' ' + str(val['count']) + ' ' + str(val['saving']) + ' '+ str(val['cumsum']) + ' ' + val['file'] + ' \n')

img_hand.close()
html_hand.close()


fig=plt.figure()
plt.scatter(img_save.index, img_save['cumsum'],marker='o')
plt.title('Disk space saving using the MD5 hashes for images')
plt.xscale('symlog')
plt.yscale('symlog')
plt.xlabel('file size [bytes]')
plt.ylabel('disk space saving [bytes]')
plt.ylim([-1,1e10])
plt.xlim([-1,1e6])
plt.grid(True)
fig.savefig("figs/img_hash_size_cum.png",format='png')
fig.savefig("figs/img_hash_size_cum.eps",format='eps')
plt.show()


fig=plt.figure()
plt.scatter(html_save.index, html_save['cumsum'],marker='o')
plt.title('Disk space saving using the MD5 hashes for html files')
plt.xscale('symlog')
plt.yscale('symlog')
plt.xlabel('file size [bytes]')
plt.ylabel('disk space saving [bytes]')
plt.ylim([-1,1e10])
plt.xlim([-1,1e7])
plt.grid(True)
fig.savefig("figs/html_hash_size_cum.png",format='png')
fig.savefig("figs/html_hash_size_cum.eps",format='eps')
plt.show()

fig=plt.figure()
plt.scatter(img_save.index, img_save['cumsum'],marker='o')
plt.title('Disk space saving using the MD5 hashes for images')
plt.xscale('symlog')
#plt.yscale('symlog')
plt.xlabel('file size [bytes]')
plt.ylabel('disk space saving [bytes]')
plt.ylim([-1,1.25*1e9])
plt.xlim([-1,1e6])
plt.grid(True)
fig.savefig("figs/img_hash_size_cum_ylin.png",format='png')
fig.savefig("figs/img_hash_size_cum_ylin.eps",format='eps')
plt.show()





fig=plt.figure()
plt.scatter(html_save.index, html_save['cumsum'],marker='o')
plt.title('Disk space saving using the MD5 hashes for html files')
plt.xscale('symlog')
#plt.yscale('symlog')
plt.xlabel('file size [bytes]')
plt.ylabel('disk space saving [bytes]')
plt.ylim([-1,0.12*1e10])
plt.xlim([-1,1e7])
plt.grid(True)
fig.savefig("figs/html_hash_size_cum_ylin.png",format='png')
fig.savefig("figs/html_hash_size_cum_ylin.eps",format='eps')
plt.show()

data_dir = '/home/nsarafij/project/OpenWPM/hash/data/'
fig_dir = '/home/nsarafij/project/OpenWPM/hash/figs/'

fhand = open(data_dir + 'img_saving_001.txt')
html_size = []; html_saving = []
for line in fhand:
    line.strip()
    elem = line.split()
    print elem
    html_size.append(elem[0])
    html_saving.append(elem[3])

fig=plt.figure()
plt.scatter(html_size, html_saving,marker='o')
plt.title('Disk space saving using the MD5 hashes for html files')
plt.xscale('symlog')
#plt.yscale('symlog')
plt.xlabel('file size [bytes]')
plt.ylabel('disk space saving [bytes]')
plt.ylim([-1,0.12*1e10])
plt.xlim([-1,1e7])
plt.grid(True)
fig.savefig(fig_dir + "html_hash_size_cum_ylin.png",format='png')
fig.savefig(fig_dir + "html_hash_size_cum_ylin.eps",format='eps')
plt.show()


data_dir = '/home/nsarafij/project/OpenWPM/hash/data/'
fig_dir = '/home/nsarafij/project/OpenWPM/hash/figs/'
df = pd.read_csv(data_dir + 'img_001.txt', sep=' ',header = None)
df=df[[0,1,2]]
df.columns=['size','count','file']

fig=plt.figure()
plt.scatter(df['size'],df['count'],marker='.',color='blue')
plt.title('Images with the same MD5 hashes')
plt.xscale('symlog')
plt.yscale('symlog')
plt.xlabel('file size [bytes]')
plt.ylabel('count')
plt.xlim([-1,1e6])
plt.ylim([0,1e5])
plt.grid(True)
fig.savefig(fig_dir + "img_hash_size.png",format='png')
fig.savefig(fig_dir + "img_hash_size.eps",format='eps')
plt.show()


data_dir = '/home/nsarafij/project/OpenWPM/hash/data/'
fig_dir = '/home/nsarafij/project/OpenWPM/hash/figs/'
df = pd.read_csv(data_dir + 'html_001.txt', sep=' ',header = None)
df=df[[0,1,2]]
df.columns=['size','count','file']
fig=plt.figure()
plt.scatter(df['size'],df['count'],marker='.',color='blue')
plt.title('Html files with the same MD5 hashes')
plt.xscale('symlog')
plt.yscale('symlog')
plt.xlabel('file size [bytes]')
plt.ylabel('count')
plt.xlim([-1,1e9])
plt.ylim([0,1e5])
plt.grid(True)
fig.savefig(fig_dir + "html_hash_size.png",format='png')
fig.savefig(fig_dir + "html_hash_size.eps",format='eps')
plt.show()


    








    

