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


@app.route('/api/webhook-history-visualized', methods=['POST'])
def history_visualized_hook():
    logging.info("Received the webhook callback for history answer visualized")

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
        histories_client = huma_sdk.session(service_name="Histories")
        payload = request.json
        conversion_id = payload.get("conversion_id")
        history_visual = histories_client.fetch_history_visual_result(conversion_id=conversion_id)
        # print(history_visual['answer']['data'])
        # pprint.pprint(history_visual['answer']['data'], indent=4)
        print(f'Copy the link from the result and paste in your favorite browser for downloading the visual file')
        print(highlight(json.dumps(history_visual, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
        return jsonify({}), 200

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400
        
    except Exception as e:
        # Handle other exceptions
        logging.exception("An error occurred")
        return jsonify({"error": "An error occurred"}), 500


@app.route('/api/webhook-subscription-updated', methods=['POST'])
def subscription_updated_hook():
    logging.info("Received the webhook callback for subscription answer updated")

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
        subscription_client = huma_sdk.session(service_name="Subscriptions")
        payload = request.json
        href = payload.get("links", [{}])[0].get('href',"")
        subscribed_id = href.split('/')[-2] if '/' in href else ""
        if subscribed_id:
            subscribed_visual = subscription_client.fetch_subscription_data(conversion_id=conversion_id)
            # print(subscribed_visual['answer']['data'])
            # pprint.pprint(subscribed_visual['answer']['data'], indent=4)
            print(highlight(json.dumps(subscribed_visual, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
        else:
            print('Ticket Number Not Found')
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