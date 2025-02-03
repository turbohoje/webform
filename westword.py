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
import random
import datetime
import ssl
import sys
import http.client

HOST = '34.134.131.179'
PORT = 8443

server_certificate_pem = """-----BEGIN CERTIFICATE-----
MIIDZzCCAk+gAwIBAgIUSWvO+etC/f2ljFt+LlYfN8UxtdEwDQYJKoZIhvcNAQEL
BQAwQzELMAkGA1UEBhMCdXMxCzAJBgNVBAgMAmNvMQ8wDQYDVQQHDAZkZW52ZXIx
FjAUBgNVBAoMDXJvY2tldHNjaWVuY2UwHhcNMjUwMTI5MDEzNTE3WhcNMjYwMTI5
MDEzNTE3WjBDMQswCQYDVQQGEwJ1czELMAkGA1UECAwCY28xDzANBgNVBAcMBmRl
bnZlcjEWMBQGA1UECgwNcm9ja2V0c2NpZW5jZTCCASIwDQYJKoZIhvcNAQEBBQAD
ggEPADCCAQoCggEBAMFCJ1tkDL0F05N8JZNaoX2o6ZHaWJSbi/WUAUcNPL9qv+jY
nDYGJPpKItb0aZWYMlop4PuN0QfRlrRoXP+I8bbAyRHw0nH7mwORaYcrS893BBca
ptIEecOUcO+G3NLR/t/sbWL3muKDCh3e9lap8EX2uPqctIxcr2osruKta/VH9MVG
uViEptDFk7W80T4svtugIA+iUx4m9OPEJBviFr8kVALGVrmu7D6X9rYp+EAZyeNt
EfoCD0+SWU1BL2o4/Lqqe59YTmd34wPmjNmNSFngIFDjtgRCu1dmkdhfa4NMoqJP
ueaqVbp/oOgx7IVTi1VpOGVVxPVnpQu99as/Eg8CAwEAAaNTMFEwHQYDVR0OBBYE
FBxvkSSz0tt+UVinwDGaSKmwVZjvMB8GA1UdIwQYMBaAFBxvkSSz0tt+UVinwDGa
SKmwVZjvMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBADc2B0z3
AAnRqeMnNWZiRW33EWR4Uzz4m8wTGzQCodXfpk4Lhpdq2zYmabtGZzBFpGgWeqcA
7UUqQdDR+YCf7MaStrJM4iuL/9mMT69Zfo7DGnVdLQ7z/w+41AMNeFVX+Glwq9Z2
iR+TDwgQX2ivzO6Jn+GhvKGq/Agymu6waQx6tJtqA5Xc9ZXiPjO+cCFyPN41MEz1
7eMwXxTmlyVKKMfwlYkjBXa9a0HdzAq5L1gouS8CkXJB0i1zwvJNoQtn/sVbtsMw
FVSD5N/LIupZS4EhfkeKdG2Pj8j23ckw6emMDFAlwY0Oi9NPpYYlIEiWvhITfqYv
ab9n8jLbL1JA8Zk=
-----END CERTIFICATE-----
"""

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations(cadata=server_certificate_pem)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Open an HTTPS connection to the server
conn = http.client.HTTPSConnection(HOST, PORT, context=context)

def generate_timeout():
    now = datetime.datetime.now()
    current_hour = now.hour
    base_timeout = random.random() * 1500  # Base timeout: 0 to 3600 seconds

    # During business hours (9:00 to 17:00), use multiplier 1.
    if 9 <= current_hour < 17:
        multiplier = 1
    elif current_hour < 9:
        # For early morning hours (0 to 8), interpolate multiplier from 5 at midnight to 1 at 9:00.
        # When current_hour is 0, multiplier = 1 + 4 * ((9-0)/9) = 5.
        multiplier = 1 + 5 * ((9 - current_hour) / 9)
    else:  # current_hour >= 17
        # For evening hours (17 to 23), interpolate multiplier from 1 at 17:00 to 5 at 24:00.
        multiplier = 1 + 5 * ((current_hour - 17) / (24 - 17))  # denominator is 7

    return int(base_timeout * multiplier)

class Westord:
    def __init__(self):
        self.driver = webdriver.Chrome()# Selenium imports.
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--mute-audio")
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
            driver.execute_script("document.body.style.zoom='10%';")
            print("closing popup")
            first_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/form/div[1]/a[2]"))
            )
            first_element.click()
            time.sleep(1)

            #write in
            print(f"filling write in")
            first_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), 'BEST CANNABIS VAPE')]"))
            )
            first_element.click()
            time.sleep(1)
            #//div[contains(text(), 'BEST CANNABIS VAPE')]/parent::div/parent::li//input[@type='radio' and contains(@id, 'write-in')]
            print(f"clicking radio")
            input_element = WebDriverWait(self.driver, 50).until(
                EC.presence_of_all_elements_located((By.XPATH, f"//div[contains(text(), 'BEST CANNABIS VAPE')]/parent::div/parent::li//input[@type='radio' and contains(@id, 'write-in')]"))
            )
            self.driver.execute_script("arguments[0][0].click();", input_element)
            #//div[contains(text(), 'BEST CANNABIS VAPE')]/parent::div/parent::li//input[@type='text' and contains(@data-name, 'write-in')]
            text_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'BEST CANNABIS VAPE')]/parent::div/parent::li//input[@type='text' and contains(@data-name, 'write-in')]"))
            )

            rand = random.choice(["Mile high Xtractions","Mile high extractions","Mile high xtracts","Mile high extracts","MHX"])
            text_field.send_keys(rand)
            print(f"write in {rand} complete")
            time.sleep(1)
            #end write in

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
            print("submit clicked, waiting for output")
            time.sleep(1)

            try:
                # Wait for the element to be present and visible
                confirmation_message = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//h3[contains(@class, 'fdn-best-of-poll-header-complete-subheader') and text()='Your Ballot Has Been Submitted!']"))
                )
                print("Confirmation message is visible on the page!")

                try:
                    IP = requests.get("https://icanhazip.com").text.rstrip('\n')
                    payload = f"{IP},{f},{l},{e}"

                    headers = {"Content-Type": "text/plain"}
                    conn.request("POST", "/prepend", body=payload, headers=headers)

                    resp = conn.getresponse()
                    print(f"Response status: {resp.status} {resp.reason}")
                    print(resp.read().decode())
                except:
                    print("unable to phone home to mothership")
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
# url = "https://troutlake.co/gray/names.csv"

# Check if the file exists locally
if not os.path.exists(file_name):
    print(f"{file_name} not found locally. Downloading from {url}...")
    try:
        # # Download the file
        # response = requests.get(url, stream=True)
        # response.raise_for_status()  # Raise an error for bad status codes
        
        # # Save the file locally
        # with open(file_name, 'wb') as file:
        #     for chunk in response.iter_content(chunk_size=8192):
        #         file.write(chunk)
        
        # print(f"{file_name} downloaded successfully.")

        conn.request("GET", "/download-file")
        resp = conn.getresponse()

        print(f"Response status: {resp.status} {resp.reason}")
        if resp.status == 200:
            file_contents = resp.read()
            #print("File contents:")
            #print(file_contents.decode())
            with open(file_name, 'wb') as file:
                file.write(file_contents)
        else:
            print(resp.read().decode())
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {file_name}: {e}")
else:
    print(f"{file_name} already exists locally.")

# ip
IP = requests.get("https://icanhazip.com").text.rstrip('\n')
print(f"IP is {IP}")


while True:
    w = Westord()
  
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
    
    
    if status == 0: #expected result, no immediate retry
        sleeptime = generate_timeout()
        print(f"sleeping {sleeptime}")
        time.sleep(sleeptime)
    else:
        print(f"failed code {status}")
    del(w) 
