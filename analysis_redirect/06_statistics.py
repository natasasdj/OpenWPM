import sqlite3
import pandas as pd
import os
import operator
import matplotlib.pyplot as plt
from wordcloud import WordCloud


#data_dir = sys.argv[1]
main_dir = '/home/nsarafij/project/'
data_dir = os.path.join(main_dir,'data/output_001/')
#output_dir = sys.argv[2]
output_dir = os.path.join(main_dir,'OpenWPM/analysis_redirect/output/')
anal_dir = os.path.join(main_dir,'OpenWPM/analysis/results/')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


db2_file = os.path.join(anal_dir,'images.sqlite')
conn2 = sqlite3.connect(db2_file)


query = 'SELECT count(*) FROM Images WHERE site_id BETWEEN 1 AND 100'
df = pd.read_sql_query(query,conn2)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

urls_file =  os.path.join(output_dir,'urls')
keysPersist_file =  os.path.join(output_dir,'keysPersist')
file_len(urls_file)
file_len(keysPersist_file)

fhand = open(keysPersist_file)
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
                
 
     
fhand.close()

#keysDict_sorted = sorted(keys_dict.items(), key=operator.itemgetter(1), reverse = True)

fig_dir = '/home/nsarafij/project/OpenWPM/analysis_redirect/output/figs'

wordcloud = WordCloud(max_font_size=40,collocations=False).generate_from_frequencies(keys_dict)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig(os.path.join(fig_dir, 'keysPersist_worldCloud.png'))
plt.show()

keysDict_sorted = sorted(keys_dict.items(), key=operator.itemgetter(1), reverse = True)
keys,values = zip(*keysDict_sorted)

plt.figure()
plt.plot(range(1,len(values)+1), values, linestyle='None', marker='o', color='red', markersize=5)
plt.xscale('symlog')
plt.xlabel('key rank')
plt.ylabel('number of 1-pixel Image redirects')
plt.xlim([0,len(values)+1])
plt.grid(True)
plt.savefig(os.path.join(fig_dir, 'keysPersistPerRedirect_worldCloud.png'))
plt.show()





conn2.close()

