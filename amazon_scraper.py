# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 09:05:39 2018

@author: SHALOM ALEXANDER
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup
import urllib.request
import re

class Amazon_all_mobile_scraper:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.delay = 20
        self.url = 'https://www.amazon.in/s/s/ref=sr_nr_p_89_1?bq=%28not+browse%3A%2714991705031%7C14991710031%7C14991712031%7C14991716031%7C14991714031%7C14991718031%27%29&fst=as%3Aoff&rh=n%3A976419031%2Cn%3A%21976420031%2Cn%3A1389401031%2Cn%3A1389432031%2Cn%3A1805560031%2Cp_98%3A10440597031%2Cp_36%3A1500000-99999999%2Cp_89%3ASamsung&bbn=1805560031&ie=UTF8&qid=1541004646&rnid=3837712031'
        
    def load_amazon(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver,self.delay)
            wait.until(EC.presence_of_element_located((By.ID,"a-page")))
            print("Page is ready.")
        except TimeoutException:
            print("Took too much time to load!")
        except:
            print("Something went wrong in loading part!!")
            
    def extract_list_of_mobiles(self):
        mobile_list_text = []
        try:
            mobile_list = self.driver.find_elements_by_xpath('//h2[@class = "a-size-medium s-inline  s-access-title  a-text-normal"]')
            #print(mobile_list)
            mobile_list_text = [each_mobile.text for each_mobile in mobile_list]
        except NoSuchElementException:
            print("Sorry, Unable to get the requested element")
        except:
            print("Something went wrong in extract element process!!")
        return mobile_list_text
    
    def extract_url_of_mobiles(self,mobiles):
        url_list = []
        html_page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(html_page,'lxml')
        for link in soup.find_all("a",{"class":"a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"}):
            url_list.append(link["href"])        
        return url_list,soup
    
    def exitAmazon(self):
        self.driver.close()

scraper = Amazon_all_mobile_scraper()
scraper.load_amazon()
data = scraper.extract_list_of_mobiles()
data_link,soup = scraper.extract_url_of_mobiles(data)
scraper.exitAmazon()

#print("Preview of scraped data.")
#for i in range(3):
#    print("Mobile:" + data[i])
#    print("Link:" + data_link[i])
        
