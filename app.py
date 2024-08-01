from flask import Flask, request, jsonify, render_template
from google.cloud import vision
import os
import json

app = Flask(__name__)

# Load credentials from environment variables
def load_credentials():
    return {
        "type": os.getenv('GOOGLE_TYPE'),
        "project_id": os.getenv('GOOGLE_PROJECT_ID'),
        "private_key_id": os.getenv('GOOGLE_PRIVATE_KEY_ID'),
        "private_key": os.getenv('GOOGLE_PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": os.getenv('GOOGLE_CLIENT_EMAIL'),
        "client_id": os.getenv('GOOGLE_CLIENT_ID'),
        "auth_uri": os.getenv('GOOGLE_AUTH_URI'),
        "token_uri": os.getenv('GOOGLE_TOKEN_URI'),
        "auth_provider_x509_cert_url": os.getenv('GOOGLE_AUTH_PROVIDER_X509_CERT_URL'),
        "client_x509_cert_url": os.getenv('GOOGLE_CLIENT_X509_CERT_URL'),
        "universe_domains":os.getenv('GOOGLE_DOMAIN')
    }

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

    credentials = load_credentials()
    client = vision.ImageAnnotatorClient.from_service_account_info(credentials)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    dish_names = [label.description for label in labels]
    return jsonify({'dishes': dish_names})

if __name__ == '__main__':
    app.run(debug=True)
