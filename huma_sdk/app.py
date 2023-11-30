from flask import Flask, request, jsonify, copy_current_request_context
import os
import logging
from dotenv import load_dotenv
import huma_sdk
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
import json
import asyncio
from threading import Thread

load_dotenv()

API_CALLBACK_AUTH=os.getenv("API_CALLBACK_AUTH")

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def start_async_task(task_func, payload):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Directly await the coroutine function
    try:
        question=payload.get('question', '')
        loop.run_until_complete(task_func(payload))
        print(f"async pagination to get data on {question} - task completed successfully")
    except Exception as e:
        print(f"error: {str(e)}")
        pass
    finally:
        loop.close()
    pass

async def async_fetch_answer(payload):
    #only applicable if response data is paginated
    page, limit = 1, 100
    max_page_count = 100
    is_batch_pages = bool(max_page_count)

    question_status = payload.get('question_status', '')
    question = payload.get('question', '')
    ticket_number = payload.get("ticket_number")
    try:
        if 'rejected' in question_status:
            print(f'question "{question}" failed to process.')
        elif question_status == 'succeeded':
            questions_client = huma_sdk.session(service_name="Questions")
            print(f"getting result of question with '{ticket_number}' ticket number")
            result_response = questions_client.fetch_answer(ticket_number=ticket_number, page=page, \
                limit=limit, is_batch_pages=is_batch_pages, max_page_count=max_page_count)

            sanitized_question = ''.join(e for e in question if e.isalnum() or e.isspace()).replace(' ', '_')

            # Create 'output' directory if it doesn't exist
            os.makedirs("output", exist_ok=True)

            # Save the result to a JSON file
            with open(f'output/{sanitized_question}_result.json', 'w') as f:
                json.dump(result_response, f, indent=4)
            print(highlight(json.dumps(result_response, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
            print(f"result saved to output/{sanitized_question}_result.json")
        else:
            print(f"unrecognized question status {question_status}")
            print(highlight(json.dumps(result_response, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
    except Exception as e:
        logging.exception("an error occurred in async task")
        return False
    return True
    # end of async_fetch_answer

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
        payload = request.json

        start_async_task(async_fetch_answer, payload)
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
        history_visual = histories_client.fetch_history_visual_result(conversion_id)
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
            subscribed_visual = subscription_client.fetch_subscription_data(subscribed_id=subscribed_id)
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

@app.route('/', methods=['GET'])
def hello():
    return "hello!"

if __name__ == '__main__':
    app.run(debug=True, port=5001)