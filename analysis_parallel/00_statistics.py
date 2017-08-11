#TODO: number of successfully loaded sites
#TODO: number of successfully loaded links
import pandas as pd
import sqlite3
import os
import sys
from statsmodels.distributions.empirical_distribution import ECDF
import matplotlib.pyplot as plt

res_dir = '/home/nsarafij/project/OpenWPM/analysis_parallel/results'
db = os.path.join(res_dir,'site_visits.sqlite')
conn = sqlite3.connect(db)
query = 'SELECT * FROM site_visits'
sv = pd.read_sql_query(query,conn)

# total number of pages visites
sv.shape[0] #1000619 #4351318
# number of home sites visited
sv0 = sv.query('link_id==0') 
sv0.shape[0] #10000 #37999
for i in range(1,38001):
    if i in sv0['site_id'].values: continue
    print "missing site_id:", i     
# missing site_id: 6800


# number of successfully loaded home sites
sv0['success'].sum() # 34716
sv0['success'].sum() / float(sv0.shape[0]) #0.9136
# numer of first links visited
sv1 = sv.query('link_id<>0')
sv1.shape[0] #990619 #4313319
# number of successfully loaded first links 
sv1['success'].sum() #964315 #4313319
sv1['success'].sum() / float(sv1.shape[0]) # 1
# number of successfully loaded pages 
sv['success'].sum() #4347837
sv['success'].sum() / float(sv.shape[0]) #0.9992

# average number of the first links in a successfully loaded sites
float(sv1.shape[0])/sv0.shape[0]
#113.51138187847049


# distribution of the number of links
# distribution of the response time for the home sites
# distribution of the response time for the links

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
    
resp_time_sites = df0['resp_time_3'].fillna(91)
resp_time_links = df1['resp_time_2'].fillna(61)
(x1,y1) = ecdf_for_plot(resp_time_sites)
(x2,y2) = ecdf_for_plot(resp_time_links)
no_links = df0['no_links'][df0['resp_time_3'].notnull()]
(x3,y3) = ecdf_for_plot(no_links)

fig_dir = '/home/nsarafij/project/OpenWPM/analysis/figs_10k'

plt.figure()
plt.step(x1,y1,label='sites')
plt.step(x2,y2,label='first links')
plt.title('CDF of the response time')
plt.xlabel('time [s]')
plt.legend(loc='lower right',shadow=True)
plt.grid(True)
plt.savefig(os.path.join(fig_dir,'resp_time_cdf.png'))
plt.show()

plt.figure()
plt.step(x3,y3)
plt.title('CDF of the number of links for the home sites')
plt.xlabel('number of links')
plt.grid(True)
plt.savefig(os.path.join(fig_dir,'no_links_cdf.png'))


no_links_counts = no_links.value_counts(sort = False).sort_index()
no_links_cumSum = (no_links_counts * no_links_counts.index).cumsum()
no_links_cumPerc = no_links_cumSum/no_links_cumSum.iloc[-1]

from matplotlib.ticker import FuncFormatter

# function for formating numbers in images
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

fig, ax = plt.subplots()
plt.plot(no_links_cumSum)
plt.title('Cumulative sum of the number of links for the home sites')
plt.ylabel('cumulative sum')
plt.xlabel('number of links')
plt.grid(True)
ax.yaxis.set_major_formatter(formatter)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir,'no_links_cumSum.png'))

plt.figure()
plt.plot(no_links_cumPerc)
plt.title('Cumulative percentage of the number of links for the home sites')
plt.xlabel('number of links')
plt.ylabel('cumulative percentage of the total number of links')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir,'no_links_cumPerc.png'))

plt.show()






    
    
    
    
