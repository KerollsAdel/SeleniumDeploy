from flask import Flask, render_template, request, jsonify
import os
import logging
import traceback
from automation import run_automation, test_chrome_availability

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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
                                    result="❌ Error: Username and password are required")
            
            # Log environment info for debugging
            logger.info(f"Chrome binary: {os.environ.get('GOOGLE_CHROME_BIN', 'Not set')}")
            logger.info(f"ChromeDriver path: {os.environ.get('CHROMEDRIVER_PATH', 'Not set')}")
            
            # Run automation with provided credentials
            logger.info("Starting automation...")
            result = run_automation(username, password)
            logger.info(f"Automation completed with result: {result}")
            
            return render_template('index.html', result=result)
            
        except Exception as e:
            logger.error(f"Error in index route: {str(e)}")
            logger.error(traceback.format_exc())
            return render_template('index.html', 
            result=f"❌ Server Error: {str(e)}")
    
    return render_template('index.html')

@app.route('/test-chrome')
def test_chrome():
    """Test endpoint to check if Chrome is working"""
    try:
        logger.info("Testing Chrome availability...")
        result = test_chrome_availability()
        
        # Get environment information
        env_info = {
            'GOOGLE_CHROME_BIN': os.environ.get('GOOGLE_CHROME_BIN', 'Not set'),
            'CHROMEDRIVER_PATH': os.environ.get('CHROMEDRIVER_PATH', 'Not set'),
            'PATH': os.environ.get('PATH', 'Not set')[:200] + '...' if len(os.environ.get('PATH', '')) > 200 else os.environ.get('PATH', 'Not set'),
            'DISPLAY': os.environ.get('DISPLAY', 'Not set'),
            'USER': os.environ.get('USER', 'Not set')
        }
        
        # Check if files exist
        chrome_bin = os.environ.get('GOOGLE_CHROME_BIN')
        chromedriver_path = os.environ.get('CHROMEDRIVER_PATH', '/usr/local/bin/chromedriver')
        
        file_status = {
            'chrome_exists': os.path.exists(chrome_bin) if chrome_bin else False,
            'chromedriver_exists': os.path.exists(chromedriver_path),
            'chrome_executable': os.access(chrome_bin, os.X_OK) if chrome_bin and os.path.exists(chrome_bin) else False,
            'chromedriver_executable': os.access(chromedriver_path, os.X_OK) if os.path.exists(chromedriver_path) else False
        }
        
        return jsonify({
            'success': '✅' in result,
            'message': result,
            'environment': env_info,
            'file_status': file_status
        })
        
    except Exception as e:
        logger.error(f"Chrome test error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False, 
            'error': str(e),
            'traceback': traceback.format_exc()
        })

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        # Basic health check
        health_data = {
            'status': 'healthy',
            'environment': 'railway' if os.environ.get('RAILWAY_ENVIRONMENT') else 'local',
            'python_version': os.sys.version,
            'chrome_available': bool(os.environ.get('GOOGLE_CHROME_BIN')),
            'chromedriver_available': bool(os.environ.get('CHROMEDRIVER_PATH'))
        }
        
        return jsonify(health_data)
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return render_template('index.html', 
                        result="❌ Internal server error occurred. Please check the logs.")

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask app on port {port}, debug={debug_mode}")
    logger.info(f"Environment: {'Railway' if os.environ.get('RAILWAY_ENVIRONMENT') else 'Local'}")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)