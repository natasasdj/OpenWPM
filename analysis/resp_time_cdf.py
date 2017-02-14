
import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF

db_file='/home/nsarafij/project/data/output_1_1000/crawl-data.sqlite'
conn = sqlite3.connect(db_file)
print "open sqlite db"
query = 'SELECT * FROM site_visits WHERE visit_domain_id = 1'
df = pd.read_sql_query(query,conn)
print df

df_filled = df.fillna(100)
print df_filled

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


(x1,y1) = ecdf_for_plot(df_filled['resp_time_1'])
(x2,y2) = ecdf_for_plot(df_filled['resp_time_2'])
(x3,y3) = ecdf_for_plot(df_filled['resp_time_4'])
(x4,y4) = ecdf_for_plot(df_filled['no_links'])

#print x1
print "x1: ", type(x1)
#print y1
print "y1: ", type(y1)
fig = plt.figure()
fig.subplots_adjust(hspace=.4)

ax=plt.subplot(221)
ax.set_title("CDF of Response Time 1")
ax.set_xlabel('time [s]')

plt.step(x1,y1)

ax=plt.subplot(222)
ax.set_title("CDF of Response Time 2")
ax.set_xlabel('time [s]')
plt.step(x2,y2)

ax=plt.subplot(223)
ax.set_title("CDF of Response Time 3")
ax.set_xlabel('time [s]')
plt.step(x3,y3)

ax=plt.subplot(224)
ax.set_title("CDF of Number of Links")
ax.set_xlabel('number of links')
plt.step(x4,y4)


#plt.suptitle('CDFs')
plt.show()
#plt.savefig('figs/cdfs.pdf')


conn.close()
