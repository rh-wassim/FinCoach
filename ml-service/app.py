from flask import Flask, jsonify
from model import load_model

app = Flask(__name__)

# Load (or train) model at startup
load_model()


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "ml-service"})


if __name__ == '__main__':
    app.run(port=5001, debug=False)
