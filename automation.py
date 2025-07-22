from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
import time
from ABUAUF.Credentials import *
from ABUAUF.Locators import *
from selenium.webdriver.common.keys import Keys
def run_automation(username, password):
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(options=options)

    try:
        driver.get('https://abuauf.com')
        time.sleep(2)

        # Login
        driver.find_element(By.XPATH,CLOSE_BUTTON).click()
        driver.get('https://abuauf.com/login')
        driver.find_element(By.XPATH,EMAIL).send_keys(username)
        driver.find_element(By.XPATH, PASSWORD).send_keys(password)
        driver.find_element(By.XPATH, PASSWORD).send_keys(Keys.RETURN)
        
        

        # Wait for page to load
        time.sleep(3)

        # Add additional automation steps here

        # Example: check for success message
       # success_msg = driver.find_element(By.XPATH, locators.success_message).text

        return f"Automation completed successfully: {success_msg}"
    except Exception as e:
        return f"Error during automation: {str(e)}"
    finally:
        driver.quit()
