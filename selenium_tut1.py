# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 22:34:47 2018

@author: SHALOM ALEXANDER
"""

from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://econpy.pythonanywhere.com/ex/001.html")

# Extract list of all buyers and prices
buyers = driver.find_elements_by_xpath('//div[@title = "buyer-name"]')
prices = driver.find_elements_by_xpath('//span[@class = "item-price"]')
bp = driver.find_elements_by_xpath('//div[@title = "buyer-info"]')

# getting those variable values
n = len(buyers)
for i in range(n):
    print(buyers[i].text + ":" + prices[i].text)

# bp is the buyer and price info together taken
m = len(bp)
for i in range(m):
    print(bp[i].text)
    
driver.close()
