from flask import Flask, render_template, request, jsonify
import os
import logging
import traceback
from automation import run_automation, test_chrome_availability

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            
            logger.info(f"Received login request for username: {username}")
            
            if not username or not password:
                return render_template('index.html', 
                                    result="Error: Username and password are required")
            
            # Run automation with provided credentials
            logger.info("Starting automation...")
            result = run_automation(username, password)
            logger.info(f"Automation completed with result: {result}")
            
            return render_template('index.html', result=result)
            
        except Exception as e:
            logger.error(f"Error in index route: {str(e)}")
            logger.error(traceback.format_exc())
            return render_template('index.html', 
            result=f"Server Error: {str(e)}")
    
    return render_template('index.html')

@app.route('/test-chrome')
def test_chrome():
    """Test endpoint to check if Chrome is working"""
    try:
        logger.info("Testing Chrome availability...")
        result = test_chrome_availability()
        return jsonify({
            'success': True, 
            'message': result,
            'environment': {
                'GOOGLE_CHROME_BIN': os.environ.get('GOOGLE_CHROME_BIN', 'Not set'),
                'PATH': os.environ.get('PATH', 'Not set')[:200] + '...'
            }
        })
    except Exception as e:
        logger.error(f"Chrome test error: {str(e)}")
        return jsonify({
            'success': False, 
            'error': str(e),
            'traceback': traceback.format_exc()
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'environment': 'railway' if os.environ.get('RAILWAY_ENVIRONMENT') else 'local'
    })

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return render_template('index.html', 
                        result="Internal server error occurred. Please check the logs.")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask app on port {port}, debug={debug_mode}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)