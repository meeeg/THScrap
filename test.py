from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
from arr import *
import numpy as np
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#setting up executable service for scraping, if downloaded, change path to your used path for folder
driver_service = Service(executable_path="C:/Users/Meg/Desktop/pyth")
website = ' '

#variables we're going to use to store the data scraped
arrnames = []
arrpoints = []
arrcerts = []
arrurl = []
arrcertnum = []

#selectors we're going to use to scrape our data
nameselector = '''return document.querySelector("#profile-sections-container > div:nth-child(1) > tbme-about-me").shadowRoot.querySelector("lwc-tbui-card > div.heading > div.details > h1")'''
pointselector = '''return document.querySelector("#profile-sections-container > div:nth-child(2) > tbme-rank").shadowRoot.querySelector("lwc-tds-theme-provider > lwc-tbui-card > div.stats-container > lwc-tbui-tally:nth-child(2)").shadowRoot.querySelector("span > span.tally__count.tally__count_success")'''
urlselector = '''return document.querySelector("#profile-sections-container > div:nth-child(1) > tbme-about-me").shadowRoot.querySelector("lwc-tbui-card > div.footer > div.slug > a")'''
certsselector = '//*[@id="aura-directive-id-4"]/c-lwc-certifications/c-lwc-card/article/div/slot/c-lwc-achievements-certification-item/c-lwc-media/div/div/slot/h4/a'
viewmoreselector = '//*[@id="aura-directive-id-4"]/c-lwc-certifications/c-lwc-card/article/footer/slot/c-lwc-card-footer-link/button'

#iterable on a list provided at arr.py (already imported), keys are equal to the trailhead profiles
for key in arr:
            website = key
            driver = webdriver.Chrome(service=driver_service)
            #setting implicit wait for browser to not close before charging data
            driver.implicitly_wait(2)
            driver.get(website)
            try:
                certs = driver.find_elements(By.XPATH, certsselector)
                #join cert elements detected to create a list of certifications 
                certstostring = ', '.join([str(elem.text) for elem in certs])
                #If we have more than 3 certifications trailblazer site doesn't show all until we click on 'View More' button
                #adding logic to enter 'View More' and charge all certifications
                if len(certs)>=3:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, viewmoreselector))).click()
                    certs = driver.find_elements(By.XPATH, certsselector)
                    certstostring = ', '.join([str(elem.text) for elem in certs])
                    x=[i for i in arrcerts]
                #retrieve name, points and url from selectors
                name = driver.execute_script(nameselector)
                points = driver.execute_script(pointselector)
                url = driver.execute_script(urlselector)
                #if we dont have certs, but we have a name, we assign "N/A"
                if certs == [] and not name =="" and not points =="":
                    certsnotapplicable = "N/A"
                    certstostring = certsnotapplicable
                #checking if trailblazer url is valid, if so, pushing the values to our collection
                if not name == "":
                    arrnames.append(name.text.strip())
                    arrcerts.append(certstostring)
                    arrpoints.append(points.text)
                    arrurl.append(url.text)
                    arrcertnum.append(len(certs))
                driver.close()
                #debug info
                print(url.text)
                print(name.text)
                print(points.text)
                if certs == "N/A":
                    print(certs)
                else:
                    print(certstostring)
            except:
                #checking for ways to close driver when invalid record comes up
                continue


#table setup for csv
result = {'Name':arrnames, 'Number of Certifications':arrcertnum, 'Certifications': arrcerts, 'Points': arrpoints, 'URL': arrurl}
archive = pd.DataFrame.from_dict(result)
archive.to_csv('trailhead.csv')
#final debug
print(archive)



