# Selenium
The ML_acts repository contains the dataset scraped using "web scraper" but in order to automate the scraping procedure I am using selenium.

# Installation
1. Selenium could be installed using<br>
  >> pip install selenium<br>
2. After installing selenium we need to install geckodriver which is the driver for Firefox.<br>
    Here is the link https://github.com/mozilla/geckodriver/releases<br>
    Paste the extracted geckodriver.exe file in your Anaconda3 Script Files so that it comes under the
    path variable.<br>

# Practice
In order to test Selenium I used the following website http://econpy.pythonanywhere.com/ex/001.html which contains the names and prices.
I did the scarping on these website. In the files<br>
1. selenium_tut1.py<br>
2. selenium_tut3.py<br>

# Rules Related to Scraping 
There are rules on scraping. If you don't do it the proper way then your project work could backfire you and you might be facing some litigation issues.<br>
To get the basic idea on the legal and ethical aspects of scraping view these links:<br>
1. https://www.quora.com/Is-scraping-and-crawling-to-collect-data-illegal
2. https://www.datahen.com/legal-ethical-aspects-data-scraping/

# Summary of rules
1. Check that if the website allows scraping.
2. Don't scrap the websites continuosly. Give the servers time to breath.
3. Posess good intensions about using data. This means that don't use the data you collected from the website, again them in a harmful        manner which affects their business.

# Lets Scrap Amazon
In order to scrap Amazon, I have used BeautifulSoup library of python too apart from selenium. Currently the scraping of mobile names and their respective links are done till now. Further work is to be done.
(To understant look amazon_scraper.py)

# Goal
My goal is to achieve an amazon scraper that can scrap the websites review on each mobile automatically for the user and does the analysis let's say emotion analysis.<br>

Stay tuned for more!

