from automation import TaskManager, CommandSequence

# The list of sites that we wish to crawl
NUM_BROWSERS = 3
#sites = ['http://www.google.com']
sites = ['http://www.blic.rs']

# Loads the manager preference and 3 copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in xrange(NUM_BROWSERS):
    browser_params[i]['http_instrument'] = True # Record HTTP Requests and Responses
    browser_params[i]['disable_flash'] = False #Enable flash for all three browsers
    browser_params[i]['js_instrument']= True
    browser_params[i]['http_instrument']= True
    browser_params[i]['save_javascript']= True
   # browser_params[i]['cookie_instrument']= True
# browser_params[0]['headless'] = True #Launch only browser 0 headless

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/projects/test'
manager_params['log_directory'] = '~/projects/test'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites with all browsers simultaneously
for site in sites:
    command_sequence = CommandSequence.CommandSequence(site)

    # Start by visiting the page
    #command_sequence.get(sleep=0, timeout=60)
    command_sequence.browse(sleep=0, num_links=3, timeout=60)
    #command_sequence.browse_links(timeout=30)

    # dump_profile_cookies/dump_flash_cookies closes the current tab.
    #command_sequence.dump_profile_cookies(120)

    manager.execute_command_sequence(command_sequence, index=None) # index = None = first come / first serve

# Shuts down the browsers and waits for the data to finish logging
manager.close()
