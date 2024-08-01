from flask import Flask, request, jsonify, render_template
from google.cloud import vision

app = Flask(__name__)
client = vision.ImageAnnotatorClient()

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
    app.run(debug=True)

