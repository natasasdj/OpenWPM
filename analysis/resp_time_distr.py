
import pandas as pd
import sqlite3
import matplotlib.pyplot as pl

db_file='/home/nsarafij/projects/data/output_1_1000/crawl-data.sqlite'
conn = sqlite3.connect(db_file)

query = 'SELECT * FROM site_visits WHERE visit_domain_id = 1'

#cur=conn.cursor()
#cur.execute()
#for row in cur:
#    print row

df = pd.read_sql_query(query,conn)
print df

#sql = 'DELETE FROM site_visits WHERE visit_id=?'
#cur = conn.cursor()
#cur.execute(sql, (1001,))
#cur.execute(sql, (1002,))
#conn.commit()


df_filled = df.fillna(100)
print df_filled

ax=pl.subplot(221)
ax.set_title("Response Time 1")
pl.hist(df_filled['resp_time_1'])

ax=pl.subplot(222)
ax.set_title("Response Time 2")
pl.hist(df_filled['resp_time_2'])
ax=pl.subplot(223)
ax.set_title("Response Time 3")
pl.hist(df_filled['resp_time_5'])
ax=pl.subplot(224)
ax.set_title("Number of links")
pl.hist(df_filled['no_links'])

pl.suptitle('Some distributions')
#pl.show()
pl.savefig('figs/some_distrib.pdf')

print df['resp_time_1'].isnull().sum()
print df['resp_time_2'].isnull().sum()
print df['resp_time_5'].isnull().sum()
print (df['no_links']<300).sum()
print (df['no_links']>1000).sum()
print max(df['no_links'])
conn.close()
