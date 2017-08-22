import sqlite3
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from matplotlib.ticker import FuncFormatter
from statsmodels.distributions.empirical_distribution import ECDF

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


main_dir = '/root/OpenWPM/analysis_parallel/'
res_dir = os.path.join(main_dir,'results')

db = os.path.join(res_dir,'images1.sqlite')
conn1 = sqlite3.connect(db)
query = 'SELECT * FROM Images1'
df1 = pd.read_sql_query(query,conn1)
conn1.close()

###### ##### ##### #####  distinct page and response domain ##### ##### ##### #####

# total_homesites = 34716
total_domains = 34716



############################## 1-pixel images ###########################################


# response domains

df = df1[['site_id', 'respDom_domain2', 'respCompany']].drop_duplicates()
dom_pix1 = df['respDom_domain2'].value_counts()
dom_pix1_perc = dom_pix1/float(total_domains)*100


### figures
fig_dir = os.path.join(main_dir,'figs')

# percentages
fig = plt.figure()
plt.plot(range(1,dom_pix1_perc.shape[0]+1),dom_pix1_perc,marker='.')
plt.xscale('symlog')
plt.xlabel('domain rank')
plt.ylabel('percentage of visited pages')
plt.title('1-pixel Images')
plt.grid(True)
fig.savefig(os.path.join(fig_dir,'07a_respDomain_pix1_percPerDomain.png'),format='png')

### table domains - companies
domcom = df[['respDom_domain2','respCompany']].groupby(['respDom_domain2','respCompany']).size().reset_index(name='img_perc').sort_values('img_perc',ascending=False)
domcom['img_perc']=domcom['img_perc']/float(total_domains)*100
table_dir = os.path.join(main_dir,'tables')
fhand = open(os.path.join(table_dir,'baseDomain_Company_pix1_percPerDomain_top30.txt'),'w+')

n = 30
for i in range(0,n):
    dom = domcom.iloc[i,0]
    com =  domcom.iloc[i,1]
    perc = domcom.iloc[i,2]
    s = str(i+1) + ' & ' + dom  +  ' & ' + com + ' & ' + '%.2f' % perc + '\\\\ \\hline'
    s = s.encode('UTF-8')
    print s
    fhand.write(s + '\n')  

fhand.close()

##### companies

df = df1[['site_id', 'respCompany']].drop_duplicates()
com_pix1 = df['respCompany'].value_counts()
com_pix1_perc = com_pix1/float(total_domains)*100

# percentages
fig = plt.figure()
plt.plot(range(1,com_pix1.shape[0]+1),com_pix1_perc,marker='.')
plt.xscale('log')
plt.xlabel('company rank')
plt.ylabel('percentage of visited pages')
plt.xlim([1,com_pix1.size])
plt.grid(True)
fig.savefig(os.path.join(fig_dir, '07c_respCompany_pix1_percPerDomain.png'),format='png')


### table top 30 companies
fhand = open(os.path.join(table_dir,'company_pix1_percPerDomain_top30.txt'),'w+')


for i in range(0,n):
    com = com_pix1_perc.index[i]
    perc = com_pix1_perc[i]
    s = str(i+1) +  ' & ' + com + ' & ' + '%.3f' % perc + '\\\\ \\hline'
    s = s.encode('UTF-8')
    print s
    fhand.write(s + '\n')  
          
fhand.close()



#################################### zero-size images ######################################


##### response domains

db = os.path.join(res_dir,'images0.sqlite')
conn0 = sqlite3.connect(db)
query = 'SELECT * FROM Images0'
df0 = pd.read_sql_query(query,conn0)
conn0.close()



df = df0[['site_id', 'respDom_domain2', 'respCompany']].drop_duplicates()
dom_zero = df['respDom_domain2'].value_counts()
dom_zero_perc = dom_zero/float(total_domains)*100


# percentages
fig = plt.figure()
plt.plot(range(1,dom_zero_perc.shape[0]+1),dom_zero_perc,marker='.')
plt.xscale('symlog')
plt.xlabel('domain rank')
plt.ylabel('percentage of visited pages')
plt.title('1-pixel Images')
plt.grid(True)
fig.savefig(os.path.join(fig_dir,'08a_respDomain_zero_percPerDomain.png'),format='png')

### table domains - companies
domcom = df[['respDom_domain2','respCompany']].groupby(['respDom_domain2','respCompany']).size().reset_index(name='img_perc').sort_values('img_perc',ascending=False)
domcom['img_perc']=domcom['img_perc']/float(total_domains)*100
table_dir = os.path.join(main_dir,'tables')
fhand = open(os.path.join(table_dir,'baseDomain_Company_zero_percPerDomain_top30.txt'),'w+')

n = 30
for i in range(0,n):
    dom = domcom.iloc[i,0]
    com =  domcom.iloc[i,1]
    perc = domcom.iloc[i,2]
    s = str(i+1) + ' & ' + dom  +  ' & ' + com + ' & ' + '%.2f' % perc + '\\\\ \\hline'
    s = s.encode('UTF-8')
    print s
    fhand.write(s + '\n')

fhand.close()

##### companies

df = df0[['site_id', 'respCompany']].drop_duplicates()
com_zero = df['respCompany'].value_counts()
com_zero_perc = com_zero/float(total_domains)*100


# percentages
fig = plt.figure()
plt.plot(range(1,com_zero.shape[0]+1),com_zero_perc*100,marker='.')
plt.xscale('log')
plt.xlabel('company rank')
plt.ylabel('percentage of third-party images')
plt.xlim([1,com_zero.size])
plt.grid(True)
fig.savefig(os.path.join(fig_dir, '08c_respCompany_zero_percPerDomain.png'),format='png')

### table top 30 companies
fhand = open(os.path.join(table_dir,'company_zero_percPerDomain_top30.txt'),'w+')

for i in range(0,n):
    com = com_zero_perc.index[i]
    perc = com_zero_perc[i]
    s = str(i+1) +  ' & ' + com + ' & ' + '%.3f' % perc + '\\\\ \\hline'
    s = s.encode('UTF-8')
    print s
    fhand.write(s + '\n')
               
fhand.close()














