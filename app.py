from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)

FAKEYOU_INFERENCE_URL = "https://api.fakeyou.com/tts/inference"
FAKEYOU_JOB_URL = "https://api.fakeyou.com/tts/job/"

@app.route('/api/tts', methods=['POST'])
def tts_request():
    data = request.json
    model_token = data.get('modelToken')
    text = data.get('text')

    uuid_token = str(uuid.uuid4())
    payload = {
        "tts_model_token": model_token,
        "uuid_idempotency_token": uuid_token,
        "inference_text": text
    }

    try:
        response = requests.post(FAKEYOU_INFERENCE_URL, json=payload)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tts-status/<job_token>', methods=['GET'])
def tts_status(job_token):
    try:
        response = requests.get(f"{FAKEYOU_JOB_URL}{job_token}")
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
