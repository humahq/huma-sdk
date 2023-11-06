## Webhooks

### Setup for Receiving Webhook Callbacks

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

    You will receive a URL that forwards requests to your local server, e.g. ( `https:/xx-your-ip.ngrok-free.app -> http://localhost:5001)

5. Register your webhook at `Huma Platform > Hamburger menu > Developer Settings > Webhooks > Add Webhook`.  
   - In the options box, put callback url as your ngrok url followed by the endpoint address.  So something like `https://xxxx-xx-xx-xx-xx.ngrok-free.app/api/webhook-question-answered`.  Also, put this in your .env file as the value for `API_URL`
   - In the resource box put `Questions`.
   - In the event box put `Computed`
   - In the authorization box put a made up secret code that you also put in your .env file as the value for the environment variable for `API_CALLBACK_AUTH`
   - Set `FLASK_APP` to your webhooks code.  Something like `FLASK_APP=examples/webhooks:main` which points to the function `main` in the file `examples/webhooks.py`
  
6. Trigger your webhook callback by [submitting a question](../examples/webhooks.py).

### Webhook Events

You can configure a [Webhook](https://humahq.stoplight.io/docs/huma-api/d77fdd05735ba-quickstart-guide-for-huma-webhooks) that triggers when an event occurs. The following events are supported.

| Resource   | Event Name    | Description                                        |
|------------|---------------|----------------------------------------------------|
| Questions  | Computed      | This event is triggered when a question [computation](https://humahq.stoplight.io/docs/huma-api/hg2usrjd5e4yr-get-history-visual), whether successful or unsuccessful, occurs. When this event is triggered, it indicates that the system has processed the question and either successfully provided an answer or encountered an issue in doing so. |
| Histories  | Visualized    | 	This event triggers when a [historical](https://humahq.stoplight.io/docs/huma-api/hg2usrjd5e4yr-get-history-visual) answer, whether successful or failed, is visualized. It retrieves visual representations of answers, such as PDF, CSV, or PPT, providing users access to historical information, regardless of the outcome.|
| Subscriptions | AnswerUpdated | This event is triggered when there is an update to the answer of a question that a user has [subscribed](https://humahq.stoplight.io/docs/huma-api/53obj41n78909-create-subscriptions) to. Subscriptions allow users to receive notifications or updates when there are changes or improvements to the answers related to their specific questions. When this event occurs, it signifies that the answer to a subscribed question has been modified or enhanced in some way.|


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
        ## Add your custom logic here
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
        history_visual = histories_client.fetch_history_visual_result(conversion_id)
        ## Add your custom logic here
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
            ## Add your custom logic here
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
    app.run(debug=True, port=5001)  ## modify port number to your desired port
```

### Triggering Webhook Callbacks

#### Ask a Question to Trigger Your answer computed Webhook Callback

1. Run your webhook client code.

2. Submit a question using the `submit_question` function and wait for the webhook callback:

    ```python
    import huma_sdk
    questions_client = huma_sdk.session(service_name="Questions")
    submission_status = questions_client.submit_question(question="<write your question>", commands=["<write command_1>", "<write command_2>"])
    print("submission_status:", submission_status)
    ```

By following these steps, you'll have a setup to receive answers through a webhook in a secure and efficient manner.

#### Submit request for creating history visual file to Trigger Your history visualized Webhook Callback

1. Run your webhook client code.

2. Submit a request for creating history visual file using the `submit_history_visual` function and wait for the webhook callback:

    ```python
    import huma_sdk
    histories_client = huma_sdk.session(service_name="Histories")
    submission_status = histories_client.submit_history_visual(ticket_number="<write your ticket number>")
    print("submission_status:", submission_status)
    ```

By following these steps, you'll have a setup to receive visuals of history answer through a webhook in a secure and efficient manner.

#### Subscription Updated Webhook are automatically triggered when answer of subscribed question is updated.

1. Run your webhook client code.

2. Subscribe a question using the `create_subscription` function and wait for the webhook callback:

    ```python
    import huma_sdk
    subscription_client = huma_sdk.session(service_name="Subscriptions")
    subscription_status = subscription_client.create_subscription(ticket_number=ticket_number)
    print("subscription_status:", subscription_status)
    ```

By following these steps, you'll have a setup to receive subscribed answer updationsw through a webhook in a secure and efficient manner.

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


