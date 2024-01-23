# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 09:05:39 2018

@author: SHARON ALEXANDER
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

import pandas as pd
import traceback

NUM_OF_MOBILES = 0

class Amazon_all_mobile_scraper:
    def __init__(self):
        self.driver = None
        self.delay = 20
        self.url = 'https://www.amazon.in/s/s/ref=sr_nr_p_89_1?bq=%28not+browse%3A%2714991705031%7C14991710031%7C14991712031%7C14991716031%7C14991714031%7C14991718031%27%29&fst=as%3Aoff&rh=n%3A976419031%2Cn%3A%21976420031%2Cn%3A1389401031%2Cn%3A1389432031%2Cn%3A1805560031%2Cp_98%3A10440597031%2Cp_36%3A1500000-99999999%2Cp_89%3ASamsung&bbn=1805560031&ie=UTF8&qid=1541004646&rnid=3837712031'
        self.page_link = [self.url]
        self.soup = None
        self.driver = webdriver.Firefox()
        
    def setUrl(self,url):
        self.url = url
    
    def get_page_link(self):
        return self.page_link
        
    def load_amazon(self):
        reload = 1
        while reload == 1:
            try:
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
                self.driver = webdriver.Firefox()
            except:
                print("Something went wrong in loading part!!")
                self.driver.close()
                self.driver = webdriver.Firefox()
            
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
    
    def extract_next_page_url(self):
        # find all span with page links
        var = self.soup.find_all("span",{"class":"pagnLink"})
        # get the a tags
        atag = []
        for span in var:
            atag.append(span.find("a"))
        # get the href part
        for tag in atag:
            self.page_link.append('https://www.amazon.in' + tag["href"])
        
        
    def extract_price_of_mobile2(self):
        deal_price = []
        retail_price = []
        all_price = self.soup.find_all("div",{"class":"a-column a-span7"})
        for price in all_price:
            deal_price_tag = price.find("span",{"class":"a-size-base a-color-price s-price a-text-bold"})
            retail_price_tag = price.find("span",{"class":"a-size-small a-color-secondary a-text-strike"})
            
            
            # if deal price with diff class name
            if deal_price_tag == None:
                deal_price_tag = price.find("span",{"class":"a-size-base a-color-price a-text-bold"})
            
            # if retail price isn't mentioned
            if retail_price_tag == None:
                retail_price_tag = deal_price_tag
                
            try:
                string_deal_price = deal_price_tag.text
                string_retail_price = retail_price_tag.text
            except AttributeError:
                string_deal_price = '0'
                string_retail_price = '0'
                print("Warning new class encountered please add in your list!!")
            price_in_str = [string_deal_price,string_retail_price]
            price_in_int = []
            
            for i in range(2):
                # cleaning price
                string_price = re.sub('\\xa0\\xa0','',price_in_str[i])
                string_price = re.sub(',','',string_price)
                price_in_int.append(int(string_price))
            
            deal_price.append(price_in_int[0])
            retail_price.append(price_in_int[1])
        
        return deal_price,retail_price
            
    
    def extract_rating_from_string(self,string):
        if string == "":
            result = "0.0"
        else:
            string = list(string)
            result = "".join(string[0:3])
        try:
            result = float(result)
        except:
            result = float(string[0] + ".0")
        return result
    
    def extract_rating_n_count_for_blanks(self,tag):
        # This function goes to link of mobile and scraps the customer count and ratings
        # else it assigns them zero
        customer_count = '0'
        rating = 0
        link_tag = tag.find("a",{"class":"a-size-small a-link-normal a-text-normal"})
        link = link_tag["href"]
        scraper2 = Amazon_all_mobile_scraper()
        scraper2.setUrl(link)
        scraper2.load_amazon()
        # scrap the customer count then the rating
        var = scraper2.soup.find('h2',{'data-hook':'total-review-count'})
        try:
            if var.text != 'No customer reviews':
                customer_count = re.sub(' customer reviews','',var.text)
                string_rating = scraper2.soup.find('span',{'data-hook':'rating-out-of-text'})
                #print(string_rating)
                rating = float(re.sub(' out of 5 stars','',string_rating.text))
                
        except:
            print("Something went wrong in extract_rating_n_count_for_blanks!")
            traceback.print_exc()
        
        scraper2.exitAmazon()
        return rating,customer_count
    
    def extract_rating_n_count(self):
        var = self.soup.find_all("div",{"class":"a-column a-span5 a-span-last"})
        rating = []
        count = []
        for tag in var:
            rating_tag = tag.find("span",{"class":"a-icon-alt"})
            if rating_tag == None:
                string = ""
            else:
                string = rating_tag.text
            rating_from_string =self.extract_rating_from_string(string)
            
            count_tag = tag.find("a",{"class":"a-size-small a-link-normal a-text-normal"})
            count_from_string = count_tag == None and "" or count_tag.text
            
            # If no review or customer count scraped go to the
            # specific website and scrap it
            if count_from_string == 'See Details':
                rating_from_string,count_from_string = self.extract_rating_n_count_for_blanks(tag)
                
            rating.append(rating_from_string)
            count.append(count_from_string)
        return rating,count 

    
    def exitAmazon(self):
        self.driver.close()


data = pd.DataFrame(columns = ['Mobile_names'])
deal_price = pd.DataFrame(columns = ['Deal_price'])
retail_price = pd.DataFrame(columns = ['Retail_price'])
mobile_rating = pd.DataFrame(columns = ['Mobile_rating'])
customer_count = pd.DataFrame(columns = ['Customers'])

scraper = Amazon_all_mobile_scraper()
scraper.load_amazon()
scraper.extract_next_page_url()
URL_TO_NEXT_PAGE = scraper.get_page_link()

# Crawling happens here.
for next_page in URL_TO_NEXT_PAGE:
    # Loading that page
    scraper.setUrl(next_page)
    scraper.load_amazon()
    # Do the scraping for that page
    data = data.append(pd.DataFrame(data = scraper.extract_list_of_mobiles(),
                                    columns = ['Mobile_names']),ignore_index = True)
    #data_link = scraper.extract_url_of_mobiles(data)
    #data_img = scraper.extract_images_of_mobiles()
    deal, retail = scraper.extract_price_of_mobile2()
    rating,count = scraper.extract_rating_n_count()
    deal_price = deal_price.append(pd.DataFrame(data = deal,
                                    columns = ['Deal_price']),ignore_index = True)
    retail_price = retail_price.append(pd.DataFrame(data = retail,
                                    columns = ['Retail_price']),ignore_index = True)
    mobile_rating = mobile_rating.append(pd.DataFrame(data = rating,
                                    columns = ['Mobile_rating']),ignore_index = True)
    customer_count = customer_count.append(pd.DataFrame(data = count,
                                    columns = ['Customers']),ignore_index = True)
    
    
    
    
scraper.exitAmazon()

# Removing commas in mobile names and customers
NUM_OF_MOBILES = len(data)
mobile_names = []
for i in range(NUM_OF_MOBILES):
    data.iloc[i,0] = re.sub(",","",data.iloc[i,0])
    customer_count.iloc[i,0] = re.sub(",","",customer_count.iloc[i,0])
            
        
# combining the scraped data
mobilephone_dataset = pd.DataFrame()
mobilephone_dataset = mobilephone_dataset.assign(
        Mobile_name = data,
        Deal_price = deal_price,
        Retail_price = retail_price,
        Mobile_rating = mobile_rating,
        Customers = customer_count
        )

# converting price columns to int 
try:
    mobilephone_dataset['Deal_price'] = pd.to_numeric(mobilephone_dataset['Deal_price'])
    mobilephone_dataset['Retail_price'] = pd.to_numeric(mobilephone_dataset['Retail_price'])
    mobilephone_dataset['Customers'] = pd.to_numeric(mobilephone_dataset['Customers'])
except:
    print('Data set not proper.\nSome data in price columns are not numeric!')      
        

# saving the dataset
mobilephone_dataset.to_csv('mobilename_link.csv')



