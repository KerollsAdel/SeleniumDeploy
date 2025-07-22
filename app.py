from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from selenium_logic import perform_login

load_dotenv()
app = Flask(__name__)  # Critical: This must be named 'app'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_automation():
    login_url = request.form.get('login_url') or os.getenv('LOGIN_URL')
    username = request.form.get('username') or os.getenv('USERNAME')
    password = request.form.get('password') or os.getenv('PASSWORD')
    
    result = perform_login(login_url, username, password)
    return render_template('results.html', **result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 8000))