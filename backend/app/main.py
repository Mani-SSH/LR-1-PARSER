import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from .routes.api import api

logging.basicConfig(level=logging.DEBUG)
logging.debug("Logging is configured and working.")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Register blueprints
app.register_blueprint(api, url_prefix='/api')

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.before_request
def handle_options_requests():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

# This will run the Flask app when this script is executed
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
