from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
import time
from ABUAUF.Credentials import *
from ABUAUF.Locators import *
from selenium.webdriver.common.keys import Keys
import os

def run_automation(username, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--remote-debugging-port=9222')
    
    # Set Chrome binary path for Railway
    chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', '/usr/bin/google-chrome')
    options.binary_location = chrome_bin
    
    driver = webdriver.Chrome(options=options)

    try:
        driver.get('https://abuauf.com')
        time.sleep(2)

        # Login
        driver.find_element(By.XPATH, CLOSE_BUTTON).click()
        driver.get('https://abuauf.com/login')
        driver.find_element(By.XPATH, EMAIL).send_keys(username)
        driver.find_element(By.XPATH, PASSWORD).send_keys(password)
        driver.find_element(By.XPATH, PASSWORD).send_keys(Keys.RETURN)
        
        # Wait for page to load
        time.sleep(3)

        # Add additional automation steps here
        return "Automation completed successfully"
    except Exception as e:
        return f"Error during automation: {str(e)}"
    finally:
        driver.quit()