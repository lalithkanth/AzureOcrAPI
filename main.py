from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests
import json

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

@app.route('/')
def home():
    return "Server is running"

@app.route('/process_image', methods=['POST'])
def process_image():
    # Get the environment variables
    endpoint = os.getenv('COMPUTER_VISION_ENDPOINT')
    subscription_key = os.getenv('COMPUTER_VISION_SUBSCRIPTION_KEY')
    ocr_url = endpoint + "vision/v3.1/ocr"

    # Get image URL from the request
    image_url = request.json.get('image_url')

    # Make the OCR API request
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {'language': 'unk', 'detectOrientation': 'true'}
    data = {'url': image_url}
    response = requests.post(ocr_url, headers=headers, params=params, json=data)

    # Check if the request was successful
    response.raise_for_status()

    # Extract text from the OCR analysis
    analysis = response.json()
    extracted_text = []
    for region in analysis.get('regions', []):
        for line in region.get('lines', []):
            for word in line.get('words', []):
                extracted_text.append(word.get('text', ''))

    # Prepare the result in JSON format
    result = {'extracted_text': extracted_text}

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
