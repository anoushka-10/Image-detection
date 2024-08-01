from flask import Flask, request, jsonify, render_template
from google.cloud import vision
import os
import json
import base64

app = Flask(__name__)

def get_client():
    # Get Base64 encoded credentials from environment variable
    base64_credentials = os.getenv('GOOGLE_CREDENTIALS_BASE64')
    if not base64_credentials:
        raise ValueError('Environment variable GOOGLE_CREDENTIALS_BASE64 not set')

    # Decode the Base64 credentials
    credentials_json = base64.b64decode(base64_credentials).decode('utf-8')

    # Create a client with the credentials
    return vision.ImageAnnotatorClient.from_service_account_info(json.loads(credentials_json))

client = get_client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'foodImage' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['foodImage']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    content = file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    dish_names = [label.description for label in labels]
    return jsonify({'dishes': dish_names})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
