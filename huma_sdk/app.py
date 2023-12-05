import huma_sdk
import os, logging
import json, threading
import asyncio, timeit
from pygments import highlight
from dotenv import load_dotenv
from pygments.lexers import JsonLexer
from flask import Flask, request, jsonify
from pygments.formatters import TerminalFormatter

load_dotenv()

API_CALLBACK_AUTH=os.getenv("API_CALLBACK_AUTH")

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Constants
PAGE, LIMIT = 1, 100
MAX_PAGE_COUNT = 100
IS_BATCH_PAGES = bool(MAX_PAGE_COUNT)


async def background_task(response):
    module = response.get('module')
    if module in {'question', 'subscription'}:
        payload = response.get('payload')
        async_functions = {
            "question": async_fetch_answer,
            "subscription": subscribed_answer
        }
        async_functions[module](payload)


def start_background_thread(payload):
    background_thread = threading.Thread(target=lambda: asyncio.run(background_task(payload)))
    background_thread.daemon = True
    background_thread.start()


def save_result_to_json(data, filename):
    """Save the result to a JSON file."""

    os.makedirs("output", exist_ok=True)
    with open(f'output/{filename}.json', 'w') as f:
        json.dump(data, f, indent=4)

    print(highlight(json.dumps(data, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
    print(f"Result saved to output/{filename}.json")


def async_fetch_answer(payload):
    """Retrieve answers asynchronously."""
    try:
        question_status = payload.get('question_status', '')
        question = payload.get('question', '')
        ticket_number = payload.get("ticket_number")

        if 'rejected' in question_status:
            print(f'Question with ticket number "{ticket_number}" failed to process.')

        elif question_status == 'succeeded':
            questions_client = huma_sdk.session(service_name="Questions")
            print(f"Getting result of question with ticket number '{ticket_number}'")
            result_response = questions_client.fetch_answer(ticket_number=ticket_number, page=PAGE, \
                limit=LIMIT, is_batch_pages=IS_BATCH_PAGES, max_page_count=MAX_PAGE_COUNT)

            if result_response.get('error_response'):
                print(highlight(json.dumps(result_response, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
                return False

            sanitized_question = ''.join(e for e in question if e.isalnum() or e.isspace()).replace(' ', '_')
            save_result_to_json(result_response, f'{sanitized_question}_result')

        else:
            print(f"Unrecognized question status {question_status}")

    except Exception as e:
        logging.exception("An error occurred in async_fetch_answer")
        return False

    return True


def subscribed_answer(payload):
    """Retrieve subscribed answers asynchronously."""
    try:
        href = payload.get("links", [{}])[0].get('href', "")
        subscribed_id = href.split('/')[-2] if '/' in href else ""

        if not subscribed_id:
            print(f'Subscribed Question with "{subscribed_id}" id Not Found.')

        subscription_client = huma_sdk.session(service_name="Subscriptions")
        print(f"Getting result of subscribed question with ID '{subscribed_id}'")
        subscribed_visual = subscription_client.fetch_subscription_data(subscribed_id=subscribed_id, page=PAGE, \
                limit=LIMIT, is_batch_pages=IS_BATCH_PAGES, max_page_count=MAX_PAGE_COUNT)

        if subscribed_visual.get('error_message'):
            print(highlight(json.dumps(subscribed_visual, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
            return False

        save_result_to_json(subscribed_visual, f'{subscribed_id}_result')

    except Exception as e:
        logging.exception("An error occurred in async_subscribed_answer")
        return False

    return True


@app.route('/api/webhook-question-answered', methods=['POST'])
def question_answered_hook():
    start_time = timeit.default_timer()
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
        payload = request.json
        print(highlight(json.dumps(payload, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
        answer_payload = { "module": "question", "payload": payload }

        # Start the background task when the Flask app starts
        logging.info("Starting background thread for fetching the answer")
        start_background_thread(answer_payload)
        end_time = timeit.default_timer()
        duration = end_time - start_time
        print(f"webhook-question-answered took {duration:.2f} seconds.")
        return jsonify({}), 200

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        # Handle other exceptions
        logging.exception("An error occurred")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/api/webhook-history-visualized', methods=['POST'])
def history_visualized_hook():
    start_time = timeit.default_timer()
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
        end_time = timeit.default_timer()
        duration = end_time - start_time
        print(f"webhook-history-visualized took {duration:.2f} seconds.")
        return jsonify({}), 200

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        # Handle other exceptions
        logging.exception("An error occurred")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/api/webhook-subscription-updated', methods=['POST'])
def subscription_updated_hook():
    start_time = timeit.default_timer()
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
        payload = request.json
        print(highlight(json.dumps(payload, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
        subscription_payload = { "module": "subscription", "payload": payload }

        # Start the background task when the Flask app starts
        logging.info("Starting background thread for fetching the answer")
        start_background_thread(subscription_payload)
        end_time = timeit.default_timer()
        duration = end_time - start_time
        print(f"webhook-subscription-updated took {duration:.2f} seconds.")
        return jsonify({}), 200

    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        # Handle other exceptions
        logging.exception("An error occurred")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route('/', methods=['GET'])
def hello():
    return "hello!"


if __name__ == '__main__':
    import uvicorn
    from asgiref.wsgi import WsgiToAsgi
    from werkzeug.middleware.dispatcher import DispatcherMiddleware

    wsgi_app = DispatcherMiddleware(app)
    asgi_app = WsgiToAsgi(wsgi_app)
    uvicorn.run(asgi_app, host="0.0.0.0", port=5001)