from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/jules', methods=['POST'])
def jules_api():
    data = request.json
    api_key = os.environ.get('JULES_API_KEY')

    if not api_key:
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
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)