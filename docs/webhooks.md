### Webhooks

#### Creating a Webhook Client Using Our Function

With this approach, you can create a webhook client that listens for incoming webhook requests on a static endpoint, "/api/webhook-question-answered." The webhook payload, which contains the answer to a question, will be displayed in your terminal.

```python
import huma_sdk
webhooks_client = huma_sdk.session(service_name="Webhooks")
```

#### Function 1: `activate_webhook_client`

- **Description**: This function allows users to activate the webhook client locally, enabling it to listen to incoming webhook requests.
- **Parameters**:
  - `debug` (optional): Enabling debug mode provides detailed error messages and allows automatic code reloading when changes are detected. Use this mode in a development environment, not in a production setting.
  - `port` (optional): Defines the port on which the Flask application will listen for incoming requests. By default, the Flask application runs on port 5000.
 
- **Example Usage**:

```python
webhooks_client.activate_webhook_client(debug=True, port=5000)
```

#### Creating Your Own Webhook Client

To create your own custom webhook client in Python, you can use the following example code:

```python
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

API_CALLBACK_AUTH = os.getenv("API_CALLBACK_AUTH")

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET'])
def hello():
    return "Hello!"

@app.route('/api/webhook-question-answered', methods=['POST'])
def question_answered_hook():
    logging.info("Received the webhook callback for a question answered")

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
        ## Add your custom logic here
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
    app.run(debug=True, port=5001)  ## modify port number to your desired port
```

By following these guidelines, you can set up a webhook client for receiving answers and handle incoming webhook requests with your custom logic.