# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 20:26:40 2018

@author: SHALOM ALEXANDER
"""

from selenium import webdriver

MAX_PAGE_NUM = 1
MAX_NUM_DIG = 3
driver = webdriver.Firefox()

f = open('dataset.csv','w')
f.write('buyer,price\n')
f.close()
f = open('dataset.csv','a')

for i in range(MAX_PAGE_NUM):
    num = "0"*(MAX_NUM_DIG - len(str(i))) + str(i+1)
    url = "http://econpy.pythonanywhere.com/ex/" + num + ".html"
    driver.get(url)
                                            
    buyer = driver.find_elements_by_xpath('//div[@title = "buyer-name"]')
    price = driver.find_elements_by_xpath('//span[@class = "item-price"]')
    n = len(buyer)
    for j in range(n):
        print(buyer[j].text + "," + price[j].text + "\n")
        f.write(buyer[j].text + "," + price[j].text + "\n")
        
f.close()
driver.close()
