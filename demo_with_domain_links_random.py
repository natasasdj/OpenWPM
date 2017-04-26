import sys
import csv
import os
import zipfile
import cStringIO
import threading
import time
import psutil


from urllib import urlopen
from automation import TaskManager, CommandSequence
from timeit import default_timer as timer
from random import randint
from automation.MPLogger import loggingclient

# The list of sites that we wish to crawl
NUM_BROWSERS = int(sys.argv[1])
no_start_site = int(sys.argv[2])
no_of_sites = int(sys.argv[3])
no_of_links = int(sys.argv[4])
no_of_times = int(sys.argv[5])
sleeping_time = int(sys.argv[6])

curr_dir = os.getcwd()
data_input_dir = curr_dir + '/data/input/'
data_output_dir_links = curr_dir + '/data/output/links/'
#alexa_file_name = data_input_dir + 'proba.csv'
alexa_file_name = data_input_dir + 'top-1m.csv'
log_dir = curr_dir + '/data/log/'
file=data_input_dir+'resps.txt'
r=[]

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

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
    browser_params[i]['http_instrument']= True # Record HTTP Requests and Responses
    browser_params[i]['headless'] = True
    browser_params[i]['cookie_instrument']= True
    browser_params[i]['extension_enabled']= True
    browser_params[i]['disable_flash'] = True #Enable flash for all three browsers
#    browser_params[i]['js_instrument']= True  
#    browser_params[i]['save_javascript']= True  

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = os.getcwd()+'/data/output'

manager_params['log_directory'] = os.getcwd()+'/data/output'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds

manager = TaskManager.TaskManager(manager_params, browser_params)


# Visits the sites with all browsers simultaneously
browsers_ready_list = range(0,NUM_BROWSERS)
threadLock = threading.Lock()
counter = 0

logger = loggingclient(*manager_params['logger_address'])

def browse_site_and_links(site,browser_no,browser): 
    browser.set_link_id(new=True)
    #logger.info("browse_site_and_links - BROWSER %i %i - %s %i %i" % (browser_no, browser.browser_params['crawl_id'], site, browser.curr_site_id, browser.curr_link_id))
    command_sequence = CommandSequence.CommandSequence(site,blocking=True,new=True)
    try:
        command_sequence.browse2(sleep=0, timeout=90)
        manager.execute_command_sequence(command_sequence, index= browser_no) 
        file_name = manager_params['data_directory']+'/links/link_' + str(browser.curr_site_id) 
        if os.path.exists(file_name):
            with open(file_name,'r') as f:
                links = f.read().strip().split('\n')
                l = len(links)
                for k in range(1,l): 
                    if k>no_of_links: break
                    link=links[k]                
                    browser.set_link_id() 
                    #logger.info("browse_site_and_links - BROWSER %i %i - %s %i %i" % (browser_no, browser.browser_params['crawl_id'], link, browser.curr_site_id, browser.curr_link_id))
                    if k==l-1:                           
                        command_sequence = CommandSequence.CommandSequence(link,blocking=True,reset=True) 
                    else:
                        command_sequence = CommandSequence.CommandSequence(link,blocking=True)   
		   
                    command_sequence.get2(sleep=0, timeout=60)
		    

                    manager.execute_command_sequence(command_sequence, index= browser_no) 
    except:
       pass                   
    browsers_ready_list.append(browser_no)
    global counter
    #logger.info("browse_site_and_links - counter %i" % (counter,))
    threadLock.acquire()   
    counter = counter + 1
    threadLock.release()
    #logger.info("browse_site_and_links - counter %i" % (counter,))
 
with open(alexa_file_name) as myfile:
    head = [next(myfile) for x in xrange(no_start_site+no_of_sites-1)]

head = head[no_start_site-1:]
print head 

def calc_ul_dl(dt=1, output = '/home/nsarafij/project/analysis/output/ul_dl_speed'):
    t0 = time.time()
    counter = psutil.net_io_counters()
    tot = (counter.bytes_sent, counter.bytes_recv)
    with open(output,'a') as f:
	    while True:
		last_tot = tot
		time.sleep(dt)
		t1 = time.time()
		counter = psutil.net_io_counters()       
		tot = (counter.bytes_sent, counter.bytes_recv)
		#ul, dl = [(now - last) / dt for now, last in zip(tot, last_tot)]
		ul, dl = [(now - last) / (t1-t0) for now, last in zip(tot, last_tot)]
		t0 = t1
		f.write('{2} {0:.0f} {1:.0f}\n'.format(ul, dl,time.ctime(int(t1)).split()[-2]))


t0 = threading.Thread(target=calc_ul_dl, args=(1,'/root/analysis/output/ul_dl_speed_'+str(NUM_BROWSERS)))
t0.daemon = True
t0.start()


start = timer()
print("Start time: ", start)
sleep = False
for k in range(no_of_times):
    i=0
    for line in head:
        #if i == no_start_site + no_of_sites - 1: break
        row=line.strip().split(',')            
        #print str(i)+" " + site        
        i=i+1
        #if i < no_start_site: continue
        site = 'http://www.' + row[1]
        while True:
            try:
                browser_no = browsers_ready_list.pop() 
                browser=manager.browsers[browser_no]
                site_id = k*no_of_sites + i
                print site_id, len(browsers_ready_list)
                browser.set_site_id(site_id)
                if sleep: 
                    #print str(site_id) + ": sleeping 2s"
                    time.sleep(sleeping_time)	
                sleep = len(browsers_ready_list) > 0
                t = threading.Thread(target=browse_site_and_links,args=(site,browser_no,browser)) 
                t.start()                                                                
                break
            except IndexError:           
                #logger.info("no more browsers ")
                time.sleep(1)    

# Shuts down the browsers and waits for the data to finish logging


#time.sleep(5)

while counter < no_of_sites*no_of_times:
      logger.info("********** counter %i, sleep for 15 sec **********" % (counter,))
      time.sleep(15) 
logger.info("********** counter %i **********" % (counter,))
end = timer()
rsp=end-start
r.append(rsp)
with open(file, 'a') as f:	
	f.write("r="+str(r))
manager.close()
print("Response time:", end - start)
