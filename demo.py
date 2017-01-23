
import csv
import os
import zipfile
import cStringIO
from urllib import urlopen
from automation import TaskManager, CommandSequence
from timeit import default_timer as timer

# The list of sites that we wish to crawl
NUM_BROWSERS = 2

data_input_dir = os.getcwd() + '/data/input/'

alexa_file_name = data_input_dir + 'top-1m.csv'

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




#sites = ['http://www.google.com','http://www.blic.rs','http://www.yachoo.com','http://facebook.com']
#sites = ['http://www.blic.rs']
#sites = ['http://www.google.com']

# Loads the manager preference and 3 copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in xrange(NUM_BROWSERS):
    browser_params[i]['http_instrument'] = True # Record HTTP Requests and Responses
    browser_params[i]['disable_flash'] = True #Enable flash for all three browsers
#    browser_params[i]['js_instrument']= True
    browser_params[i]['http_instrument']= True
#    browser_params[i]['save_javascript']= True
    browser_params[i]['headless'] = True
    browser_params[i]['cookie_instrument']= True
    browser_params[i]['extension_enabled']= True
    

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = os.getcwd()+'/data/output'
print manager_params['data_directory']
manager_params['log_directory'] = os.getcwd()+'/data/output'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites with all browsers simultaneously
start = timer()
print("Start time: ", start)
with open(alexa_file_name, 'r') as f:
    r = csv.reader(f, delimiter=',')    
    for i in range(2):
        site = 'http://www.' + r.next()[1]
        command_sequence = CommandSequence.CommandSequence(site,reset=True)
        command_sequence.browse2(sleep=0, num_links=3, timeout=10)
        manager.execute_command_sequence(command_sequence, index=None)
"""
        parses command type and issues command(s) to the proper browser
        <index> specifies the type of command this is:
        = None  -> first come, first serve
        =  #    -> index of browser to send command to
        = *     -> sends command to all browsers
        = **    -> sends command to all browsers (synchronized)
"""

# Shuts down the browsers and waits for the data to finish logging
manager.close()
end = timer()
print("End time: ", end)
print("Response time:", end - start)

