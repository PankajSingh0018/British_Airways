import os 
import openpyxl 
import pandas as pd 
import numpy as np 
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep 
import re

# importing selenium dependencies 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 

user_agent= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"


# Base url 
base_url = "https://www.airlinequality.com/airline-reviews/british-airways/page/1/"

# Setting up the selenium chrome options 
def set_chrome()-> Options:
    chrome_options = Options()
    chrome_options.headless = True

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
    chrome_options.add_argument('--disable-usb-discovery')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_prefs={}
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--disable-features=InterestCohort')
    chrome_options.experimental_options["prefs"]= chrome_prefs
    chrome_prefs["profile.default_content_settings"]={"images":2}
    
    return chrome_options

details= []

# Let's create a scrape function 
def scrape_web(url):
    driver = webdriver.Chrome(options=set_chrome())
    base_url = url
    driver.get(base_url)

    # getting the all the elements within the single page
    elements = driver.find_elements(By.CLASS_NAME,"body")
    tbody= driver.find_element(By.XPATH,'//*[@id="anchor 862044"]/div/div[2]/table/tbody')
    for element in elements:
        try:
            title = driver.find_element(By.CLASS_NAME,"text_header")
            Title = title.text

        except:
            Title= "NA"

        
        try:
            user_name = driver.find_element(By.XPATH, '//*[@id="anchor862044"]/h3/span/span')
            review_Name = user_name.text

        except:
            review_Name= "NA"


        try:
            Location = driver.find_element(By.XPATH, '//*[@id="anchor862044"]/h3')
            loca= Location.text
            start_index = data.find('(') + 1
            end_index = data.find(')')
            country = data[start_index:end_index]
        except:
            country= "NA"

        

        try:
            # Use regular expression to find the date pattern
            date_pattern = r'\d{1,2}(?:st|nd|rd|th) [A-Za-z]+ \d{4}'
            match = re.search(date_pattern, loca)

            if match:
                date = match.group()
                # print(date)  # Output: '9th July 2023'
        
        except:
            date="NA"
        
        try:
            trip = driver.find_element(By.CLASS_NAME,'text_content').text.split("|")
            trip_verified = trip[0]
        
        except:
            trip_verified= "Not_Verified"


        try:
            main_review= trip[1]
        
        except:
            main_review= " "


        try:
        

        details.append({
                    "Title" : Title,
                    "Reviewer" :review_Name,
                    "Country" : country,
                    "Date_posted" :date,
                    "Trip_Verified": trip_verified,
                    "Comments" :main_review
        })

        for tr in tbody.find_elements(By.XPATH,'.//tr')




