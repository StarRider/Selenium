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
import re
from urllib.request import urlretrieve

NUM_OF_MOBILES = 0

class Amazon_all_mobile_scraper:
    def __init__(self):
        self.driver = None
        self.delay = 20
        self.url = 'https://www.amazon.in/s/s/ref=sr_nr_p_89_1?bq=%28not+browse%3A%2714991705031%7C14991710031%7C14991712031%7C14991716031%7C14991714031%7C14991718031%27%29&fst=as%3Aoff&rh=n%3A976419031%2Cn%3A%21976420031%2Cn%3A1389401031%2Cn%3A1389432031%2Cn%3A1805560031%2Cp_98%3A10440597031%2Cp_36%3A1500000-99999999%2Cp_89%3ASamsung&bbn=1805560031&ie=UTF8&qid=1541004646&rnid=3837712031'
        self.soup = None
        
    def load_amazon(self):
        reload = 1
        while reload == 1:
            try:
                self.driver = webdriver.Firefox()
                self.driver.get(self.url)
                wait = WebDriverWait(self.driver,self.delay)
                wait.until(EC.presence_of_element_located((By.ID,"a-page")))
                print("Page is ready.")
                # create the soup when page is ready
                html_page = self.driver.page_source
                self.soup = BeautifulSoup(html_page,'lxml')
                reload = 0
            except TimeoutException:
                print("Took too much time to load!")
                self.driver.close()
            except:
                print("Something went wrong in loading part!!")
                self.driver.close()
            
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
        NUM_OF_MOBILES = len(mobiles)
        for i in range(NUM_OF_MOBILES):
            var = self.soup.find("a",{"title":mobiles[i]})
            url_list.append(var["href"])
        return url_list
        
    def extract_images_of_mobiles(self):
        img_num =  0
        images = []
        all_img_tags = self.soup.find_all("img",{'class':'s-access-image cfMarker'})
        for tag in all_img_tags:
            filename = "images//image" + str(img_num) + ".png"
            images.append(urlretrieve(tag["src"],filename))
            img_num = img_num + 1
        return images
        
    def extract_price_of_mobile(self):
        # This function returns the deal and retail price of phones
        deal_price = []
        retail_price = []
        deal_price_tag = self.soup.find_all("span",{"class":"a-size-base a-color-price s-price a-text-bold"})
        retail_price_tag = self.soup.find_all("span",{"class":"a-size-small a-color-secondary a-text-strike"})
        #print(len(retail_price_tag))
        #print(len(deal_price_tag))
        for tag in range(len(deal_price_tag)):
            string_deal_price = deal_price_tag[tag].text
            string_retail_price = retail_price_tag[tag].text
            price = [string_deal_price,string_retail_price]
            price_in_int = []
        
            for i in range(2):
                # cleaning price
                string_price = re.sub('\\xa0\\xa0','',price[i])
                string_price = re.sub(',','',string_price)
                price_in_int.append(int(string_price))

            # storing cleaned price
            deal_price.append(price_in_int[0])
            retail_price.append(price_in_int[1])
            
        return deal_price,retail_price
        
        
    def exitAmazon(self):
        self.driver.close()

scraper = Amazon_all_mobile_scraper()
scraper.load_amazon()
data = scraper.extract_list_of_mobiles()
data_link = scraper.extract_url_of_mobiles(data)
data_img = scraper.extract_images_of_mobiles()
deal_price, retail_price = scraper.extract_price_of_mobile()
scraper.exitAmazon()

# Removing commas in mobile names
NUM_OF_MOBILES = len(data)
mobile_names = []
for i in range(NUM_OF_MOBILES):
    mobile_names.append(re.sub(",","",data[i]))

# Converting to csv file    
with open('mobilename_link.csv','a') as f:
    f.write('Mobile Name,Link,Image_location,Deal_price,Retail_price\n')
    for i in range(NUM_OF_MOBILES):
        f.write(mobile_names[i] + "," + data_link[i] + "," + data_img[i][0] + "," +  str(deal_price[i]) + "," + str(retail_price[i]) +"\n")
        
        
        
        
        



