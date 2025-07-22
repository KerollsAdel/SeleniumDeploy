from flask import Flask, render_template, request, redirect, url_for
from automation import run_automation
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Run automation with provided credentials
        result = run_automation(username, password)
        return render_template('index.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)