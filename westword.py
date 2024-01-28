#!/usr/bin/env python

# Selenium imports.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import re, urllib3

import time, random, requests



class Westord:
    def __init__(self):
        self.driver = webdriver.Chrome()# Selenium imports.
        chrome_options = webdriver.ChromeOptions()

        # Comment the line below to switch OFF incognito mode.
        chrome_options.add_argument("--incognito")
        # Uncomment the line below to not open a browser window.
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def closeBrowser(self):
        self.driver.close()


    def fill(self, f, l, e):
        driver = self.driver

        driver.get("http://www.westword.com/best-of-denver-readers-choice-poll/best-extract-company")
        time.sleep(2)
        try:
            print("clicking via js")
            driver.execute_script("document.getElementById('question-18908674-1').click();")
            time.sleep(1)
            print("filling")
            driver.find_element("xpath", '/html/body/div[3]/div/div[3]/div/div[1]/form/div[2]/button').click()
            time.sleep(1)
            print("filling out email")
            time.sleep(1)
            driver.find_element("xpath", '/html/body/div[5]/div/div[2]/form/div/div[1]/div/input').send_keys(e)
            time.sleep(1)
            driver.find_element("xpath", '/html/body/div[5]/div/div[2]/form/div/div[2]/div/input').send_keys(f)
            time.sleep(1)
            driver.find_element("xpath", '/html/body/div[5]/div/div[2]/form/div/div[3]/div/input').send_keys(l)
            time.sleep(2)
            driver.find_element("xpath", '/html/body/div[5]/div/div[2]/form/div/div[5]/div/input').click()
            time.sleep(2)

            self.closeBrowser()

        except ElementClickInterceptedException:
            print("Done CIE")
        except NoSuchElementException:
            print("no such element :tinkies:")
        except StaleElementReferenceException:
            print("Ok stale")
        except KeyError:
            print("Key error")
        except UnexpectedAlertPresentException:
            print("do nothing")
        except UnexpectedAlertPresentException:
            print("weird")


IP = requests.get("https://icanhazip.com").text
print(f"IP is {IP}")

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
connection_pool = urllib3.PoolManager()
resp = connection_pool.request('GET',word_site )
txt = resp.data
WORDS = txt.splitlines()


while True:
    w = Westord()
    email = bytes(random.choice(WORDS)).decode("UTF-8")+"."+bytes(random.choice(WORDS)).decode("UTF-8") + "@hotmail.com"
    first = bytes(random.choice(WORDS)).decode("UTF-8") 
    last  = bytes(random.choice(WORDS)).decode("UTF-8")
    print(f"filling form with {first}, {last}, {email}")
    w.fill(first, last, email)
    del(w) 
    
    sleeptime = 5 
    print(f"sleeping {sleeptime}")
    time.sleep(sleeptime)
