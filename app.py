import time
import os
from dotenv import load_dotenv
from selenium_logic import perform_login

# Load environment variables
load_dotenv()

def main():
    """Main automation script"""
    print("Starting login automation...")
    
    # Get credentials from environment variables
    login_url = os.getenv('LOGIN_URL', 'https://abuauf.com')
    username = os.getenv('USERNAME', 'testrigor@mitchdesigns.com')
    password = os.getenv('PASSWORD', 'Koko5699#')
    
    print(f"Login URL: {login_url}")
    print(f"Username: {username}")
    
    try:
        # Perform the login
        result = perform_login(login_url, username, password)
        
        if result['success']:
            print("✓ Login successful!")
            print(f"✓ {result['message']}")
            
            # Add your post-login automation here
            # For example: scrape data, download files, etc.
            
        else:
            print("✗ Login failed!")
            print(f"✗ Error: {result['error']}")
            
    except Exception as e:
        print(f"✗ Script error: {str(e)}")
    
    # Keep the script running (for Railway deployment)
    print("Automation completed. Keeping container alive...")
    while True:
        time.sleep(60)  # Sleep for 1 minute
        print("Script is still running...")

if __name__ == '__main__':
    main()