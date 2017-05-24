import sqlite3
import pandas as pd
import os
import operator
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import sys
from matplotlib.ticker import FuncFormatter

main_dir = sys.argv[1]
# main_dir = '/home/nsarafij/project/'
# main_dir = '/root/'
output_dir = os.path.join(main_dir,'OpenWPM/analysis_redirect/output/')
anal_dir = os.path.join(main_dir,'OpenWPM/analysis/results/')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# function for determining number of lines in a file
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# function for formating numbers in images
def thousands(x, pos):
    if x>=1e9:
        return '%.0fB' % (x*1e-9)
    elif x>=1e6:
        return '%.0fM' % (x*1e-6)
    elif x>=1e3:
        return '%.0fK' % (x*1e-3)
    else:
        return x


formatter = FuncFormatter(thousands)

###### The top 10000 sites and their first links (limited to 300)

### total number of images

db2_file = os.path.join(anal_dir,'images.sqlite')
conn2 = sqlite3.connect(db2_file)

query = 'SELECT count(*) FROM Images WHERE site_id BETWEEN 1 AND 10000'
df = pd.read_sql_query(query,conn2)
# 31,861,758

### number of 1-pixel images 

query = 'SELECT count(*) FROM Images WHERE (site_id BETWEEN 1 AND 10000) AND (pixels =1)'
df = pd.read_sql_query(query,conn2)
no_1pix = 9906784
# 9,906,784 = 31.1 percent of total number of images

### number of 1-pixel images following a redirection chain

urls_file =  os.path.join(output_dir,'urls')
file_len(urls_file)
# 773,802 = 7.8 percent of 1-pixel images

### number of 1-pixel images following a redirection chain with at least one persistent key
# a persistent key is the one that appears at least once in a redirection chain 

keysPersist_file =  os.path.join(output_dir,'keysPersist')
file_len(keysPersist_file)
# 483,820 = 4.9 percent of 1-pixel images

### frequencies of keys

keys_file =  os.path.join(output_dir,'keys')
file_len(keys_file)
#1,011,727
with open(keys_file) as fhand:
    keys_dict = dict()
    for line in fhand:
        redirects = line.rstrip().split(' & ')
        for redirect in redirects:
            keys = redirect.split()[1:]
            print keys
            for key in keys:
                keys_dict[key] = keys_dict.get(key,0) + 1

fig_dir = '/home/nsarafij/project/OpenWPM/analysis_redirect/figs'
if not os.path.exists(fig_dir):
    os.makedirs(fig_dir)

wordcloud = WordCloud(max_font_size=40,collocations=False).generate_from_frequencies(keys_dict)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig(os.path.join(fig_dir, 'keys_wordCloud_10k.png'))
plt.show()

keysDict_sorted = sorted(keys_dict.items(), key=operator.itemgetter(1), reverse = True)
keys,values = zip(*keysDict_sorted)

## number of keys
len(keys)
# 3841

# ranking of keys
fig, ax = plt.subplots()
plt.plot(range(1,len(values)+1), values, linestyle='None', marker='o', color='red', markersize=5)
plt.xscale('symlog')
plt.xlabel('key rank')
plt.ylabel('number of 1-pixel Image redirects')
plt.xlim([0,len(values)+1])
plt.grid(True)
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
fig.savefig(os.path.join(fig_dir, 'keysRanking_10k.png'))
plt.show()

fig, ax = plt.subplots()
n=20
x=range(0,n)
labels = list(keys[0:n])
plt.bar(x,values[0:n], align = 'center')
plt.xticks(x, labels, rotation=75)
plt.xlabel('key rank')
plt.ylabel('number of 1-pixel Image redirects')
plt.xlim([-1,20])
plt.grid(True)
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
fig.savefig(os.path.join(fig_dir, 'keysTop20_10k.png'))
plt.show()



### frequencies of persistent keys

with open(keysPersist_file) as fhand:
    keys_dict = dict()
    for line in fhand:
        line_keys = dict()
        keys = line.rstrip().split()
        #print keys
        for key in keys:
            if key not in keys_dict:
                keys_dict[key] = 1	
                line_keys[key] = 1
            elif key not in line_keys:
                    keys_dict[key] = keys_dict[key] + 1
                    line_keys[key] = 1

fig_dir = '/home/nsarafij/project/OpenWPM/analysis_redirect/figs'
if not os.path.exists(fig_dir):
    os.makedirs(fig_dir)

wordcloud = WordCloud(max_font_size=40,collocations=False).generate_from_frequencies(keys_dict)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig(os.path.join(fig_dir, 'keysPersist_wordCloud_10k.png'))
plt.show()

keysDict_sorted = sorted(keys_dict.items(), key=operator.itemgetter(1), reverse = True)
keys,values = zip(*keysDict_sorted)

## number of persistent keys
len(keys)
# 1,322

# ranking of persistent keys
fig, ax = plt.subplots()
plt.plot(range(1,len(values)+1), values, linestyle='None', marker='o', color='red', markersize=5)
plt.xscale('symlog')
plt.xlabel('key rank')
plt.ylabel('number of 1-pixel Image redirects')
plt.xlim([0,len(values)+1])
plt.grid(True)
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
fig.savefig(os.path.join(fig_dir, 'keysPersistRanking_10k.png'))
plt.show()

fig, ax = plt.subplots()
n=20
x=range(0,n)
labels = list(keys[0:n])
plt.bar(x,values[0:n], align = 'center')
plt.xticks(x, labels, rotation=75)
plt.xlabel('key rank')
plt.ylabel('number of 1-pixel Image redirects')
plt.xlim([-1,20])
plt.grid(True)
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()
fig.savefig(os.path.join(fig_dir, 'keysPersistTop20_10k.png'))
plt.show()

conn2.close()

df = pd.read_csv('/home/nsarafij/project/OpenWPM/analysis_redirect/output/no_redirects')
df.columns=['no_redirects']
count = df['no_redirects'].value_counts()
fig, ax = plt.subplots()
plt.bar(count.index-1,count,align='center')
plt.xlabel('Number of redirects')
plt.ylabel('Number of 1-pixel images')
plt.grid(True)
ax.yaxis.set_major_formatter(formatter)
fig.savefig(os.path.join(fig_dir, 'noRedirects_10k.png'))
plt.show()


plt.bar(count.index-1,count,align='center')
plt.xlabel('Number of redirects')
plt.ylabel('Number of 1-pixel images')
plt.grid(True)
plt.yscale('symlog')
plt.savefig(os.path.join(fig_dir, 'noRedirects_10k_log.png'))
plt.show()


