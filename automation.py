from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import logging

# Import your locators and credentials
from ABUAUF.Credentials import *
from ABUAUF.Locators import *

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_automation(username, password):
    """
    Run automation with improved error handling and Railway compatibility
    """
    driver = None
    try:
        logger.info("Starting automation...")
        
        # Chrome options for Railway environment
        options = webdriver.ChromeOptions()
        
        # Essential options for Railway/Docker
        #options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-features=VizDisplayCompositor')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--remote-debugging-port=9222')
        
        # Additional stability options
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')
        options.add_argument('--disable-javascript')  # Remove if your site needs JS
        options.add_argument('--disable-css')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=NetworkService')
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-renderer-backgrounding')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-client-side-phishing-detection')
        options.add_argument('--disable-crash-reporter')
        options.add_argument('--disable-oopr-debug-crash-dump')
        options.add_argument('--no-crash-upload')
        options.add_argument('--disable-low-res-tiling')
        options.add_argument('--disable-logging')
        options.add_argument('--disable-login-animations')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-permissions-api')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-print-preview')
        options.add_argument('--disable-prompt-on-repost')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-speech-api')
        options.add_argument('--disable-sync')
        options.add_argument('--disable-web-resources')
        options.add_argument('--hide-scrollbars')
        options.add_argument('--ignore-gpu-blacklist')
        options.add_argument('--metrics-recording-only')
        options.add_argument('--mute-audio')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--no-first-run')
        options.add_argument('--no-pings')
        options.add_argument('--no-zygote')
        options.add_argument('--single-process')
        options.add_argument('--use-gl=swiftshader')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Set Chrome binary path
        chrome_bin = os.environ.get('GOOGLE_CHROME_BIN')
        if chrome_bin:
            options.binary_location = chrome_bin
            logger.info(f"Using Chrome binary: {chrome_bin}")
        
        # User agent to avoid detection
        options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        logger.info("Creating Chrome driver...")
        driver = webdriver.Chrome(options=options)
        
        # Set timeouts
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        
        logger.info("Navigating to website...")
        driver.get('https://abuauf.com')
        
        logger.info("Page loaded, looking for close button...")
        
        # Use WebDriverWait for more reliable element finding
        wait = WebDriverWait(driver, 20)
        
        # Try to close any popup/modal
        try:
            close_button = wait.until(EC.element_to_be_clickable((By.XPATH, CLOSE_BUTTON)))
            close_button.click()
            logger.info("Closed popup/modal")
            time.sleep(2)
        except Exception as e:
            logger.warning(f"Could not find/click close button: {e}")
        
        logger.info("Navigating to login page...")
        driver.get('https://abuauf.com/login')
        time.sleep(3)
        
        logger.info("Looking for email field...")
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, EMAIL)))
        email_field.clear()
        email_field.send_keys(username)
        logger.info("Entered email")
        
        logger.info("Looking for password field...")
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, PASSWORD)))
        password_field.clear()
        password_field.send_keys(password)
        logger.info("Entered password")
        
        # Submit form
        password_field.send_keys(Keys.RETURN)
        logger.info("Submitted login form")
        
        # Wait for login to process
        time.sleep(5)
        
        # Check current URL to see if login was successful
        current_url = driver.current_url
        logger.info(f"Current URL after login: {current_url}")
        
        # Basic success check
        if 'login' not in current_url.lower():
            return f"Login successful! Current page: {current_url}"
        else:
            return "Login may have failed - still on login page"
            
    except Exception as e:
        logger.error(f"Error during automation: {str(e)}")
        return f"Error during automation: {str(e)}"
    
    finally:
        if driver:
            try:
                logger.info("Closing browser...")
                driver.quit()
            except Exception as e:
                logger.error(f"Error closing driver: {e}")

def test_chrome_availability():
    """Test function to check if Chrome is available"""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.google.com')
        title = driver.title
        driver.quit()
        return f"Chrome test successful. Google page title: {title}"
    except Exception as e:
        return f"Chrome test failed: {str(e)}"