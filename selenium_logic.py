from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from ABUAUF.Credentials import*
from ABUAUF.Locators import*
def create_driver():
    """Create and return a Chrome WebDriver instance"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    return webdriver.Firefox(options=options)

def perform_login(login_url, username, password):
    """
    Performs login automation on a website
    
    Args:
        login_url (str): The login page URL
        username (str): Username for login
        password (str): Password for login
        
    Returns:
        dict: Result with success status and message
    """
    driver = None
    
    try:
        print("Creating browser...")
        driver = create_driver()
        
        print(f"Opening login page: {login_url}")
        driver.get(login_url)
        # Wait for page to load
        time.sleep(3)
        area_menu_close_button= driver.find_element(By.XPATH,CLOSE_BUTTON)
        area_menu_close_button.click()
        driver.get(LoginForm)
        print("Looking for username field...")
        # Try common username field selectors
        email_field=driver.find_element(By.XPATH,EMAIL) 
        
        
        print("Looking for password field...")
        # Try common password field selectors
        password_field=driver.find_element(By.XPATH,PASSWORD)
        
        print("Entering credentials...")
        # Enter credentials
        email_field.clear()
        email_field.send_keys(username)
        
        password_field.clear()
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        print("Looking for submit button...")
        # Try to find and click submit button
        # Check if login was successful
        current_url = driver.current_url
        page_title = driver.title
        
        print(f"Current URL after login: {current_url}")
        print(f"Page title: {page_title}")
        
        # Check for success indicators
        success_indicators = [
            "dashboard" in current_url.lower(),
            "home" in current_url.lower(),
            "profile" in current_url.lower(),
            "welcome" in page_title.lower(),
            "dashboard" in page_title.lower()
        ]
        
        # Check for error indicators
        error_indicators = [
            "login" in current_url.lower(),
            "error" in page_title.lower(),
            "invalid" in page_title.lower()
        ]
        
        if any(success_indicators):
            return {
                "success": True, 
                "message": f"Login successful! Redirected to: {current_url}",
                "current_url": current_url,
                "page_title": page_title
            }
        elif any(error_indicators):
            return {
                "success": False, 
                "error": f"Login failed - still on login page: {current_url}"
            }
        else:
            return {
                "success": True, 
                "message": f"Login completed. Current page: {page_title}",
                "current_url": current_url,
                "page_title": page_title
            }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Login automation failed: {str(e)}"
        }
        
    finally:
        if driver:
            print("Closing browser...")
            driver.quit()