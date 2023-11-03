from flask import Flask, request, jsonify
import os
import logging
from dotenv import load_dotenv
import huma_sdk
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
import pprint
import json

load_dotenv()

API_CALLBACK_AUTH=os.getenv("API_CALLBACK_AUTH")

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET'])
def hello():
    return "hello!"

@app.route('/api/webhook-question-answered', methods=['POST'])
def question_answered_hook():
    logging.info("Received the webhook callback for question answered")

    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header.split(" ")[1] != API_CALLBACK_AUTH:
        logging.warning("Unauthorized access attempt")
        return jsonify({"error": "Unauthorized"}), 401
    
    auth_parts = auth_header.split(" ")
    if len(auth_parts) < 2 or auth_parts[1] != API_CALLBACK_AUTH:
        logging.warning("Unauthorized access attempt")
        return jsonify({"error": "Unauthorized"}), 401

    try:
        logging.info(f"Webhook processed successfully with payload {request.json}\n")
        questions_client = huma_sdk.session(service_name="Questions")
        payload = request.json
        ticket_number = payload.get("ticket_number")
        answer_payload = questions_client.fetch_answer(ticket_number=ticket_number)
        # print(answer_payload['answer']['data'])
        # pprint.pprint(answer_payload['answer']['data'], indent=4)
        print(highlight(json.dumps(answer_payload, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
        return jsonify({}), 200

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400
        
    except Exception as e:
        # Handle other exceptions
        logging.exception("An error occurred")
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)