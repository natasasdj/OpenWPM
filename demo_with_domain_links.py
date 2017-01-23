
import csv
import os
import zipfile
import cStringIO
import threading
import time
from urllib import urlopen
from automation import TaskManager, CommandSequence
from timeit import default_timer as timer

# The list of sites that we wish to crawl
NUM_BROWSERS = 3

data_input_dir = os.getcwd() + '/data/input/'
data_output_dir_links = os.getcwd() + '/data/output/links/'
alexa_file_name = data_input_dir + 'proba.csv'
#alexa_file_name = data_input_dir + 'top-1m.csv'

if not os.path.exists(alexa_file_name):
    if not os.path.exists(data_input_dir):
        os.makedirs(data_input_dir)
    ALEXA_DATA_URL = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'


    f = urlopen(ALEXA_DATA_URL)
    buf = cStringIO.StringIO(f.read())
    zfile = zipfile.ZipFile(buf)
    buf = cStringIO.StringIO(zfile.read('top-1m.csv'))
    with open(alexa_file_name, 'w') as alexa_file:
        for line in buf: 
            alexa_file.writelines(line)

if not os.path.exists(data_output_dir_links):
        os.makedirs(data_output_dir_links)


#sites = ['http://www.google.com','http://www.blic.rs','http://www.yachoo.com','http://facebook.com']
#sites = ['http://www.blic.rs']
#sites = ['http://www.google.com']

# Loads the manager preference and 3 copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in xrange(NUM_BROWSERS):
#    browser_params[i]['http_instrument'] = True # Record HTTP Requests and Responses
    browser_params[i]['disable_flash'] = True #Enable flash for all three browsers
#    browser_params[i]['js_instrument']= True
#    browser_params[i]['http_instrument']= True
#    browser_params[i]['save_javascript']= True
#    browser_params[i]['headless'] = True
#    browser_params[i]['cookie_instrument']= True
#    browser_params[i]['extension_enabled']= True
    

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = os.getcwd()+'/data/output'
print manager_params['data_directory']
manager_params['log_directory'] = os.getcwd()+'/data/output'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)


# Visits the sites with all browsers simultaneously
browsers_ready_list = range(0,NUM_BROWSERS)

def browse_site_and_links(site,browser_no,site_no):
    s=str(browser_no)+"-execute command sequence start"+site
    print s 
    file_name = data_output_dir_links + "links_"+str(site_no)
    print "file_name: " + file_name
    command_sequence = CommandSequence.CommandSequence(site,blocking=True)
    command_sequence.browse2(sleep=0, file_name=file_name,timeout=15)    
    manager.execute_command_sequence(command_sequence, index= browser_no) 
    s=str(browser_no)+"-execute command sequence end"+site  
    if os.path.exists(file_name):
        print "open file"
        with open(file_name,'r') as f:
            links = f.read().strip().split('\n')
            l = len(links)
            for k in range(1,l): 
                link=links[k]
                print str(k) + "get link: " + link 
                if k==l-1:                           
                    command_sequence = CommandSequence.CommandSequence(link,blocking=True,reset=True) 
                else:
                    command_sequence = CommandSequence.CommandSequence(link,blocking=True)      
                command_sequence.get2(sleep=0, link_no=k,timeout=15)
                manager.execute_command_sequence(command_sequence, index= browser_no)
                         
    browsers_ready_list.append(browser_no) 
    

start = timer()
print("Start time: ", start)
with open(alexa_file_name, 'r') as f:
    csv_reader = csv.reader(f, delimiter=',')
    i=0
    for row in csv_reader:       
        if i==1: 
            break       
        site = 'http://www.' + row[1]
        print str(i)+" " + site
        i=i+1
        while True:
            try:
                browser_no = browsers_ready_list.pop() 
                #browse_site_and_links(site,browser_no)
                t = threading.Thread(target=browse_site_and_links,args=(site,browser_no,i))
                t.start()
                break
            except IndexError:           
                print "no more elements"
                time.sleep(1)
  

      
    



  

    



# Shuts down the browsers and waits for the data to finish logging

end = timer()
print("End time: ", end)
print("Response time:", end - start)
while len(browsers_ready_list) < NUM_BROWSERS:
      print "sleep for 5 seconds" 
      time.sleep(5) 
manager.close()