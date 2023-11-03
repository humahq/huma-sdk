## Webhooks

### Prerequists for Receiving Webhooks

To receive answers via a webhook locally, you can use ngrok.com to create a publicly accessible endpoint that routes to your local code instance. This is an alternative to setting up a publically facing server.

Follow these steps to set up the webhook client (for local use):

1. Create an account at [ngrok.com](https://ngrok.com).

2. Install ngrok locally by running the following command (for macOS users; for other platforms, refer to the instructions on the ngrok portal):

    ```bash
    brew install ngrok
    ```

3. Obtain your ngrok authentication token from the ngrok website and register it on your local machine:

    ```bash
    ngrok config add-authtoken <insert your auth-token>  
    Authtoken saved to configuration file: /Users/<username>/Library/Application Support/ngrok/ngrok.yml
    ```

4. To make your local webhook code accessible to the Huma Platform, you need to publish your local port so it can be reached. Use the following command to generate a public URL that routes to your local computer where your code will run:

    ```bash
    ngrok http 5001
    ```

    You will receive a URL that forwards requests to your local server, e.g., `https:/xx-your-ip.ngrok-free.app -> http://localhost:5001

5. Register your webhook at `Huma Platform > Hamburger menu > Developer Settings > Webhooks > Add Webhook`.  
   - In the options box, put callback url as your ngrok url followed by the endpoint address.  So something like `https://xxxx-xx-xx-xx-xx.ngrok-free.app/api/webhook-question-answered`.  Also, put this in your .env file as the value for `API_URL`
   - In the resource box put `Questions`.
   - In the event box put `Computed`
   - In the Authorization box put a made up secret code that you also put in your .env file as the value for the environment variable for `API_CALLBACK_AUTH`
   - Set `FLASK_APP` to your webhooks code.  Something like `FLASK_APP=examples/webhooks:main` which points to the function `main` in the file `examples/webhooks.py`

### Create a Webhook Client Using SDK

With this approach, you can create a webhook client that listens for incoming webhook requests on a static endpoint, "/api/webhook-question-answered." The webhook payload which contains the answer to a question will be displayed in your terminal.

```python
import huma_sdk
webhooks_client = huma_sdk.session(service_name="Webhooks")
```

### Create a Webhook Client (without using SDK)

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

### Ask a Question to Trigger Your Webhook Callback

1. Run your webhook client code.

2. Submit a question using the `submit_question` function and wait for the webhook callback:

    ```python
    import huma_sdk
    questions_client = huma_sdk.session(service_name="Questions")
    submission_status = questions_client.submit_question(question="<write your question>", commands=["<write command_1>", "<write command_2>"])
    print("submission_status:", submission_status)
    ```

By following these steps, you'll have a setup to receive answers through a webhook in a secure and efficient manner.

### Webhook Functions

#### Function 1: `activate_webhook_client`

- **Description**: This function allows users to activate the webhook client locally, enabling it to listen to incoming webhook requests.
- **Parameters**:
  - `debug` (optional): Enabling debug mode provides detailed error messages and allows automatic code reloading when changes are detected. Use this mode in a development environment, not in a production setting.
  - `port` (optional): Defines the port on which the Flask application will listen for incoming requests. By default, the Flask application runs on port 5000.
 
- **Example Usage**:

```python
webhooks_client.activate_webhook_client(debug=True, port=5000)
```


