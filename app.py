
# import streamlit as st
# import os
# import json
# from flask import Flask, request, jsonify, render_template
# from google.cloud import vision
# from google.oauth2 import service_account

# app = Flask(__name__)

# # Load credentials from Streamlit secrets
# def get_vision_client():
#     secrets = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
    
#     # Convert TOML values to dictionary
#     # credentials_info = {
#     #     "type": secrets["type"],
#     #     "project_id": secrets["project_id"],
#     #     "private_key_id": secrets["private_key_id"],
#     #     "private_key": secrets["private_key"].replace("\\n", "\n"),
#     #     "client_email": secrets["client_email"],
#     #     "client_id": secrets["client_id"],
#     #     "auth_uri": secrets["auth_uri"],
#     #     "token_uri": secrets["token_uri"],
#     #     "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
#     #     "client_x509_cert_url": secrets["client_x509_cert_url"],
#     #     "universe_domain": secrets["universe_domain"]
#     # }
    
#     client = vision.ImageAnnotatorClient(credentials=secrets)
#     return client

# client = get_vision_client()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/detect', methods=['POST'])
# def detect():
#     if 'foodImage' not in request.files:
#         return jsonify({'error': 'No file part'}), 400

#     file = request.files['foodImage']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     content = file.read()
#     image = vision.Image(content=content)
#     response = client.label_detection(image=image)
#     labels = response.label_annotations

#     dish_names = [label.description for label in labels]
#     return jsonify({'dishes': dish_names})

# if __name__ == '__main__':
#     app.run(debug=True)
