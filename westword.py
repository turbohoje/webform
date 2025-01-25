#!/usr/bin/env python3

# Selenium imports.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

        driver.get("https://www.westword.com/best-of-denver-readers-choice-poll/best-new-cannabis-product")
        time.sleep(5)
        try:
            page_height = driver.execute_script("return document.documentElement.scrollHeight;")
            driver.set_window_size(800, page_height)

            print("closing popup")
            first_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/form/div[1]/a[2]"))
            )
            first_element.click()
            time.sleep(1)
            
            print("filling best extract company")
            first_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'BEST EXTRACT COMPANY')]"))
            )
            first_element.click()
            time.sleep(1)

            print("clicking mhx")
            input_element = WebDriverWait(driver, 50).until(
                EC.presence_of_all_elements_located((By.XPATH, "//input[@value='Mile High Xtractions']"))
            )
            driver.execute_script("arguments[0][0].click();", input_element)
                        
            #driver.find_element("xpath", '/html/body/div[3]/div/div[3]/div/div/form/ul[2]/li[7]/ul/li[11]/div[2]/div/div[1]/').click()
            print("done")
            time.sleep(2)

            #<button class="fdn-best-of-poll-success-button" type="button" uk-toggle="target:#fdn-best-of-poll-submit-form">Submit Your Ballot</button>
            
            submit_button = WebDriverWait(driver, 50).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'fdn-best-of-poll-success-button') and text()='Submit Your Ballot']"))
            )
            submit_button[0].click()
            time.sleep(1)
            
            #<input type="email" id="best-of-submit-email" name="" required="">
            email_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "best-of-submit-email"))
            )
            email_input.send_keys(e)
            f_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "best-of-submit-first-name"))
            )
            f_input.send_keys(f)

            l_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "best-of-submit-last-name"))
            )
            l_input.send_keys(l)
            #   <input type="submit" name="submit" value="Yes, Submit My Ballot">
            
            time.sleep(1)
            s_button = WebDriverWait(driver, 50).until(
                EC.presence_of_all_elements_located((By.XPATH, "//input[@type='submit' and @name='submit' and @value='Yes, Submit My Ballot']"))
            )
            s_button[0].click()

            #self.closeBrowser()
            print("waiting to do it again")
            time.sleep(1)

            try:
                # Wait for the element to be present and visible
                confirmation_message = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//h3[contains(@class, 'fdn-best-of-poll-header-complete-subheader') and text()='Your Ballot Has Been Submitted!']"))
                )
                print("Confirmation message is visible on the page!")
            except:
                print("Confirmation message did not render within the timeout.")

            driver.quit()

        except ElementClickInterceptedException:
            print("Done CIE")
        except NoSuchElementException:
            print("no such element :thinkies:")
            print("trying other element")
            
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
    #firstN = random.choice(first)
    #lastN  = random.choice(last)
    #email = firstN+random.choice(["","_","."])+lastN+"@"+random.choice(["hotmail.com", "gmail.com", "colorado.edu", "colostate.edu", "comcast.net", "centurylink.com"])
    
    firstN = "justin"
    lastN = "russell"
    email = "hector@justinrmeyer.com"

    print(f"filling form with {firstN} {lastN}  {email}")

    status = w.fill(firstN, lastN, email)
    del(w) 
    
    if status == 0: #expected result, no immediate retry
        sleeptime = 3600
        print(f"sleeping {sleeptime}")
        time.sleep(sleeptime)
    else:
        print(f"failed code {status}")
