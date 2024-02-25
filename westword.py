#!/usr/bin/env python3

# Selenium imports.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import re, urllib3, sys, re

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

            #some other fields, fill out a random number of them at random
            i = ["3", "4", "5", "6", "7", "9","10", "11", "12", "13", "15", "16", "17","18","19","21","22","23"]
            for x in range(0,random.randrange(len(i))):
                i.pop(random.randrange(len(i)))
            for id in i:
                print("clicking random "+id)
                driver.execute_script("a = document.evaluate('/html/body/div[3]/div/div[3]/div/div[1]/form/ul[2]/li[6]/ul/li["+id+"]/div[2]/div/div[1]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;")
                driver.execute_script("randElement = a.children[Math.floor(Math.random() * a.children.length)];")
                driver.execute_script("randElement.firstChild.nextSibling.click()")
                time.sleep(1)

            
            print("filling")
            driver.find_element("xpath", '/html/body/div[3]/div/div[3]/div/div[1]/form/div[2]/button').click()
            time.sleep(1)
            print("filling out email")
            time.sleep(3)
                                        #    /html/body/div[4]/div/div[2]/form/div/div[1]/div/input
            #driver.find_element("xpath", '/html/body/div[4]/div/div[2]/form/div/div[1]/div/').click()
            #print("post click, filling")
                                         
            driver.find_element("xpath", '/html/body/div[4]/div/div[2]/form/div/div[1]/div/input').send_keys(e)
            time.sleep(1)
            driver.find_element("xpath", '/html/body/div[4]/div/div[2]/form/div/div[2]/div/input').send_keys(f)
            time.sleep(1)
            driver.find_element("xpath", '/html/body/div[4]/div/div[2]/form/div/div[3]/div/input').send_keys(l)
            time.sleep(2)
            driver.find_element("xpath", '/html/body/div[4]/div/div[2]/form/div/div[5]/div/input').click()
            time.sleep(2)

            self.closeBrowser()

        except ElementClickInterceptedException:
            print("Done CIE")
        except NoSuchElementException:
            print("no such element :thinkies:")
            print("trying other element")
            driver.find_element("xpath", '/html/body/div[5]/div/div[2]/form/div/div[1]/div/input').send_keys(e)
            time.sleep(1)
            driver.find_element("xpath", '/html/body/div[5]/div/div[2]/form/div/div[2]/div/input').send_keys(f)
            time.sleep(1)
            driver.find_element("xpath", '/html/body/div[5]/div/div[2]/form/div/div[3]/div/input').send_keys(l)
            time.sleep(2)
            driver.find_element("xpath", '/html/body/div[5]/div/div[2]/form/div/div[5]/div/input').click()
            time.sleep(2)
            
            return 0
        except StaleElementReferenceException:
            print("Ok stale")
            return 2
        except KeyError:
            print("Key error")
            return 3
        except UnexpectedAlertPresentException:
            print("do nothing")
            return 4
        except UnexpectedAlertPresentException:
            print("weird")
        except UnexpectedAlertPresentException:
            print("weird another one")
            return 5

        return 0

IP = requests.get("https://icanhazip.com").text
print(f"IP is {IP}")

first = []
with open("first-names.txt") as fn:
    for line in fn:
        line = re.sub(r'[\s,]+', '', line)
        first.append(line)

last = []
with open("last-names.txt") as ln:
    for line in ln:
        line = re.sub(r'[\s,]+', '', line)
        last.append(line)



while True:
    w = Westord()
    firstN = random.choice(first)
    lastN  = random.choice(last)
    email = firstN+random.choice(["","_","."])+lastN+"@"+random.choice(["hotmail.com", "gmail.com", "colorado.edu", "colostate.edu", "comcast.net", "centurylink.com"])
    
    print(f"filling form with {firstN} {lastN}  {email}")

    status = w.fill(firstN, lastN, email)
    del(w) 
    
    if status == 0: #expected result, no immediate retry
        sleeptime = 3600
        print(f"sleeping {sleeptime}")
        time.sleep(sleeptime)
    else:
        print(f"failed code {status}")
