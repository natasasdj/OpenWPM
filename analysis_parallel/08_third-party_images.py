import sqlite3
import os
import pandas as pd

# on how many pages appear third-party/one-pixel/zero-size images
# on how many homesites appear third party/one-pixel/zero-size images
# on how many first links appear third-party/one-pixel/zero-size images
# on how many domains appear third party/one-pixel/zero-size images


################ df3 - third party images


main_dir = '/root/OpenWPM/analysis_parallel/'
res_dir = os.path.join(main_dir,'results')
db = os.path.join(res_dir,'images3.sqlite')
conn3 = sqlite3.connect(db)
query = 'SELECT * FROM Images3'
df3 = pd.read_sql_query(query,conn3)
conn3.close()



#find how many unique site_id, link_id are there
#find how many unique site_id where link_id=0
#find how many unique site_id, link_id where link_id!=0
#find how many unique site_ids are

pages = df3[['site_id','link_id']].drop_duplicates()
no_pages = pages.shape[0]
total_pages = 4347837 # 00_statistics.py
float(no_pages)/total_pages
#0.8963063702710106
homesites = pages[pages['link_id']==0]
no_homesites = homesites.shape[0]
total_homesites = 34716
float(no_homesites)/total_homesites
#0.8837135614702155
firstLinks = pages[pages['link_id']!=0]
no_firstLinks = firstLinks.shape[0]
total_firstLinks = 4313319
float(no_firstLinks)/total_firstLinks
# 0.896366579888944
domains = pages['site_id'].drop_duplicates()
no_domains = domains.shape[0]
float(no_domains)/total_homesites
# 0.9049717709413527



##### ##### ###### ##### one-pixel images

pages = df3[df3['pixels']==1][['site_id','link_id']].drop_duplicates()
no_pages = pages.shape[0]
total_pages = 4347837 # 00_statistics.py
float(no_pages)/total_pages
# 0.8333189583694145
homesites = pages[pages['link_id']==0]
no_homesites = homesites.shape[0]
total_homesites = 34716
float(no_homesites)/total_homesites
# 0.8169720013826478
firstLinks = pages[pages['link_id']!=0]
no_firstLinks = firstLinks.shape[0]
total_firstLinks = 4313319
float(no_firstLinks)/total_firstLinks
# 0.8334122748630463
domains = pages['site_id'].drop_duplicates()
no_domains = domains.shape[0]
float(no_domains)/total_homesites
# 0.8664304643392096

##### ##### ##### ##### zero-size images

pages = df3[df3['size']==0][['site_id','link_id']].drop_duplicates()
no_pages = pages.shape[0]
total_pages = 4347837 # 00_statistics.py
float(no_pages)/total_pages
# 0.32237892082890873
homesites = pages[pages['link_id']==0]
no_homesites = homesites.shape[0]
total_homesites = 34716
float(no_homesites)/total_homesites
# 0.2408975688443369
firstLinks = pages[pages['link_id']!=0]
no_firstLinks = firstLinks.shape[0]
total_firstLinks = 4313319
float(no_firstLinks)/total_firstLinks
# 0.32301992966437215
domains = pages['site_id'].drop_duplicates()
no_domains = domains.shape[0]
float(no_domains)/total_homesites
# 0.6728309713100588
