### Questions

#### Setting up Connection with Questions

```python
import huma_sdk
questions_client = huma_sdk.session(service_name="Questions")
```

#### Function 1: `submit_question`

- **Description**: This Function initiates the answer calculation process by sending a question to the server.
- **Parameters**:
  - `question`:A string representing the question you want to ask.
  - `commands`(optional): An array of reserved phrases that instruct the server on how to process the question. (visit documentation for more details)

- **Example Usage**:

```python
submission_status = questions_client.submit_question(question="<write your question>", commands=["<write command_1>", "<write command_2>"])
print("submission_status:", submission_status)
```

#### Function 2: `check_question_status`

- **Description**: This Function retrieves the status of the answer calculation process using the ticket number.
- **Parameters**:
  - `ticket_number`: A unique identifier associated with a specific answer calculation process, returned by submit_question function.

- **Example Usage**:

```python
calculation_status = questions_client.check_question_status(ticket_number="<write ticket number returned from submit question>")
print("calculation_status:", calculation_status)
```

#### Function 3: `fetch_answer`

- **Description**: This Function retrieves the calculated question result based on the provided ticket number, This function also supports pagination but only in case of the answer data format that supports table visual.
- **Parameters**:
  - `ticket_number`: A unique identifier associated with a specific answer calculation process, returned by submit_question function.
  - `page`(optional): It represents the requested page number in pagination.
  - `limit`(optional): It represents the maximum number of items to be included per page

- **Example Usage**:

```python
answer = questions_client.fetch_answer(ticket_number="<write ticket number returned from submit question>", page=1, limit=20)
print("answer:", answer)
```

- ### Setting Up Webhook to Receiving Answers Callback

To receive answers via a webhook, you can use ngrok.com to create a publicly accessible endpoint that routes to your local code instance. Follow these steps to set up the webhook:

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
    ngrok http 5000
    ```

    You will receive a URL that forwards requests to your local server, e.g., `https:/xx-your-ip.ngrok-free.app -> http://localhost:5000`.

5. Register a callback address or webhook in the Huma Platform. Provide the forwarding address obtained in step 4 and an authorization code, which the webhook will use to securely call your sample code. This authorization code should match what you set in your webhook registration and your sample code. Register your webhook with an authorization code in the Huma Platform under the Hamburger Menu > Developer Settings. For this example, you need to create a webhook of type "Questions" and a subtype of "Computed." Detailed instructions can be found [here](https://humahq.stoplight.io/docs/huma-api/branches/main/d77fdd05735ba-quickstart-guide-for-huma-webhook-api).

6. Configure your code to recognize the authorization code submitted by the Huma Platform during webhook callbacks. Set an environment variable `API_CALLBACK_AUTH` with your authorization code:

    ```bash
    export API_CALLBACK_AUTH=<insert your authorization code>
    ```

7. Run your [webhook handler code](./webhooks.md) on the port specified in step 4. In the example above, it's running on port 5000.

8. Submit a question using the `submit_question` function and wait for the webhook callback:

    ```python
    import huma_sdk
    questions_client = huma_sdk.session(service_name="Questions")
    submission_status = questions_client.submit_question(question="<write your question>", commands=["<write command_1>", "<write command_2>"])
    print("submission_status:", submission_status)
    ```

By following these steps, you'll have a setup to receive answers through a webhook in a secure and efficient manner.

