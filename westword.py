#!/usr/bin/env python3

# Selenium imports.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException, ElementNotInteractableException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re, urllib3, sys, re, os, csv, time, random, requests, random



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

    def question(self, key, value):
        print(f"filling {key}")
        first_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{key}')]"))
        )
        first_element.click()
        time.sleep(1)
        print(f"clicking {value}")
        input_element = WebDriverWait(self.driver, 50).until(
            EC.presence_of_all_elements_located((By.XPATH, f"//input[@value='{value}']"))
        )
        self.driver.execute_script("arguments[0][0].click();", input_element)            
        print("done")
        time.sleep(2)
    
    def question_random(self, key):
        print(f"randoming {key}")
        first_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{key}')]"))
        )
        first_element.click()
        time.sleep(1)
        print(f"clicking first element")
        input_element = WebDriverWait(self.driver, 50).until(
            EC.presence_of_all_elements_located((By.XPATH, f"//div[contains(text(), '{key}')]/parent::div/parent::li//input[@type='radio'][1]"))
        )
        self.driver.execute_script("arguments[0][0].click();", input_element)            
        print("done")
        time.sleep(1)

    def fill(self, f, l, e):
        driver = self.driver

        driver.get("https://www.westword.com/best-of-denver-readers-choice-poll/best-new-cannabis-product")
        time.sleep(5)
        try:
            #page_height = driver.execute_script("return document.documentElement.scrollHeight;")
            #driver.set_window_size(1000, 100000)
            driver.execute_script("document.body.style.zoom='25%';")
            print("closing popup")
            first_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/form/div[1]/a[2]"))
            )
            first_element.click()
            time.sleep(1)

            #randoms
            random_question_names = ["BEST MUSHROOM COMPANY", "BEST INFUSED BEVERAGE COMPANY", "BEST MEDICAL DISPENSARY", "BEST EDIBLES COMPANY", "BEST HEAD SHOP", "BEST DISPENSARY - DENVER", "BEST CBN, CBG OR THCV PRODUCT", "BEST MEDICAL MARIJUANA DOCTOR", "BEST CANNABIS VAPE", "BEST NEW DISPENSARY", "BEST SOLVENTLESS HASH COMPANY", "BEST DISPENSARY CHAIN", "BEST FLOWER BRAND", "BEST IN-HOUSE FLOWER AT A DISPENSARY", "BEST CBD PRODUCT", "BEST DISPENSARY FOR A CONNOISSEUR", "BEST PRE-ROLL", "BEST NON-CANDY EDIBLE", "BEST CBD PET PRODUCT COMPANY", "BEST DISPENSARY - LAKEWOOD", "BEST VALUE AT A DISPENSARY", "BEST CUSTOMER SERVICE AT A DISPENSARY"]

            sub = random.sample(random_question_names, 6)

            for q in sub:
                self.question_random(q)

            


            #extract company
            self.question("BEST EXTRACT COMPANY", "Mile High Xtractions")

            #best new cannabis product
            self.question("BEST NEW CANNABIS PRODUCT", "\"Hunny Tokes\" by Mile High Xtractions")


            #submit
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
            time.sleep(10)

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

## Main code
# get names files
file_name = "names.csv"
url = "https://troutlake.co/gray/names.csv"

# Check if the file exists locally
if not os.path.exists(file_name):
    print(f"{file_name} not found locally. Downloading from {url}...")
    try:
        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Save the file locally
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"{file_name} downloaded successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {file_name}: {e}")
else:
    print(f"{file_name} already exists locally.")

# ip
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
    
    try:
        # Open the file and read the lines
        with open(file_name, mode="r") as file:
            reader = list(csv.reader(file))
            
            # Ensure the file is not empty
            if not reader:
                print("The CSV file is empty.")
            else:
                # Choose a random line from the file
                random_line = random.choice(reader)
                
                # Extract email, first name, and last name
                email, firstN, lastN = random_line
                print(f"Randomly selected entry:")
                print(f"Email: {email}")
                print(f"First Name: {firstN}")
                print(f"Last Name: {lastN}")

    except FileNotFoundError:
        print(f"Error: The file '{file_name}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    print(f"filling form with {firstN} {lastN}  {email}")

    status = w.fill(firstN, lastN, email)
    del(w) 
    
    if status == 0: #expected result, no immediate retry
        sleeptime = 3600
        print(f"sleeping {sleeptime}")
        time.sleep(sleeptime)
    else:
        print(f"failed code {status}")
