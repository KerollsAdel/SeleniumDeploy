from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from selenium_logic import perform_login
import time

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    """Show the dashboard interface"""
    return render_template('index.html',
                        login_url=os.getenv('LOGIN_URL', ''),
                        username=os.getenv('USERNAME', ''))

@app.route('/run', methods=['POST'])
def run_automation():
    """Handle form submission and run Selenium"""
    # Get credentials from form or env vars
    login_url = request.form.get('login_url') or os.getenv('LOGIN_URL')
    username = request.form.get('username') or os.getenv('USERNAME')
    password = request.form.get('password') or os.getenv('PASSWORD')
    
    if not all([login_url, username, password]):
        return render_template('results.html', 
                            error="Missing credentials!")
    
    result = perform_login(login_url, username, password)
    
    return render_template('results.html',
                        success=result['success'],
                        message=result.get('message', ''),
                        error=result.get('error', ''),
                        current_url=result.get('current_url', ''),
                        page_title=result.get('page_title', ''))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 8000))