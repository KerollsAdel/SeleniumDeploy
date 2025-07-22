import time
import os
from dotenv import load_dotenv
from selenium_logic import perform_login
from flask import Flask, render_template

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

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('results.html')

@app.route('/run-tests')
def run_tests():
    # Get credentials from environment variables
    login_url = os.getenv('LOGIN_URL', 'https://sale-sucre.pages.dev/')
    username = os.getenv('USERNAME', 'your_username')
    password = os.getenv('PASSWORD', 'your_password')
    
    # Perform the login
    result = perform_login(login_url, username, password)
    
    return render_template('results.html', 
                         success=result['success'],
                         message=result.get('message', ''),
                         error=result.get('error', ''),
                         current_url=result.get('current_url', ''),
                         page_title=result.get('page_title', ''))

if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))