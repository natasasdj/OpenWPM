from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import os
import time
from timeit import default_timer as timer

url = "http://www.yahoo.com"
root_dir = os.path.dirname(__file__)
fp = webdriver.FirefoxProfile()
fb = FirefoxBinary(root_dir  + "firefox-bin/firefox")
driver = webdriver.Firefox(firefox_profile=fp, firefox_binary=fb)
print "start"
##start = time.clock()
start = timer()
try:
    driver.get(url)
except TimeoutException:
    pass
#end = time.clock()
end = timer()
print "end"
print("Response time:", end - start)
driver.quit()
