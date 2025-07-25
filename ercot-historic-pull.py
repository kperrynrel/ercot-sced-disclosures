"""
Selenium driver pulls for historic ERCOT data. This saves all of the ERCOT 
SCED data going back to 2011 to your Downloads/ folder. Essentially we are
simulated a web session via Selenium and pressing every download button for
every file.
"""

from selenium import webdriver
import pandas as pd
from selenium.webdriver.firefox.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

username ="YOUR ERCOT USERNAME"
password = "YOUR ERCOT PASSWORD"
url = "https://data.ercot.com/data-product-archive/NP3-965-ER"

if __name__ == "__main__":
    # Initiate a session via your Selenium driver.
    service = Service(executable_path='geckodriver.exe')
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=service, options=options)
    driver.implicitly_wait(10)
    driver.get(url)
    
    time.sleep(10)
    
    # Login
    username = driver.find_element("id","email")
    username.send_keys(username)
    
    pw = driver.find_element("id","password")
    pw.send_keys(password)
    
    next_page = driver.find_element("id","next")
    ActionChains(driver).move_to_element(next_page).click().perform()
    
    # Accept terms
    time.sleep(10)
    driver.find_element(By.XPATH, '//button[@class="btn btn-primary"]').click()
    
    continue_run = True
    
    while continue_run:
        time.sleep(5)
        elems = driver.find_elements("xpath", "//*[@href]")
        values = [elem.text for elem in elems]
        if "Download" not in values:
            continue_run = False
        # Loop through all of the elements and isolate the "Download" cases
        for elem in elems:
            if elem.text == "Download":
                time.sleep(10)
                # Select the element if "Download" button
                driver.execute_script("arguments[0].click();", elem)
        time.sleep(15)
        next_pages = driver.find_elements(By.CLASS_NAME, "page-link")
        for pager in next_pages:
            print(pager.text)
            [pager.text for pager in next_pages]
            if pager.text == "»":
                driver.execute_script("arguments[0].click();", pager)
                break
    