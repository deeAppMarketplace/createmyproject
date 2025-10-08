from flask import Flask, render_template, request, jsonify
import os
import requests
import logging

# In local development allow loading .env for convenience. We import here
# so it's optional in production. If python-dotenv is installed and a .env
# file exists, it will populate os.environ.
if os.path.exists('.env'):
    try:
        # python-dotenv is an optional dev dependency; import only if present
        from dotenv import load_dotenv

        load_dotenv('.env')
    except Exception:
        # if dotenv isn't installed, we silently continue — env must be set externally
        pass

app = Flask(__name__)

# basic logging so errors show up in dev logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/jules', methods=['POST'])
def jules_api():
    try:
        # Validate JSON and required fields early to avoid 500s from KeyError/TypeError
        if not request.is_json:
            return jsonify({'error': 'Request must be application/json'}), 400

        data = request.get_json()
        required = ['org', 'repo', 'branch', 'title', 'prompt']
        missing = [k for k in required if not data.get(k)]
        if missing:
            return jsonify({'error': f'Missing required fields: {missing}'}), 400

        api_key = os.environ.get('JULES_API_KEY')
        if not api_key:
            logger.error('JULES_API_KEY not set')
            return jsonify({'error': 'JULES_API_KEY not set'}), 500

        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': api_key
        }

        payload = {
            "prompt": data['prompt'],
            "sourceContext": {
                "source": f"sources/github/{data['org']}/{data['repo']}",
                "githubRepoContext": {
                    "startingBranch": data['branch']
                }
            },
            "title": data['title']
        }

        try:
            response = requests.post('https://jules.googleapis.com/v1alpha/sessions', headers=headers, json=payload)
            response.raise_for_status()
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            logger.exception('Request to Jules API failed')
            return jsonify({'error': str(e)}), 500

    except Exception as e:
        # Catch anything unexpected, log full exception for debugging, and return JSON
        logger.exception('Unhandled exception in jules_api')
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@app.route('/healthz', methods=['GET'])
def healthz():
    """Simple health check for uptime/readiness used by load balancers and monitoring.

    Returns HTTP 200 with a small JSON payload so callers can assert the app is running.
    """
    return jsonify({'status': 'ok'}), 200


@app.route('/favicon.ico')
def favicon():
    # Serve the static favicon so browsers requesting /favicon.ico don't 404
    return app.send_static_file('favicon.ico')


if __name__ == '__main__':
    app.run(debug=True)