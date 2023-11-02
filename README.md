# HUMA-SDK - Python Package for HUMA-API

Huma-SDK is the Huma-API Software Development Kit (SDK) for Python, allowing developers to interact with the Huma-API services in their Python applications.

## Overview

This SDK simplifies the interaction with the HUMA-API, making it easy to integrate into your Python applications. It provides access to various modules, each with its set of functions for specific tasks.

## API Documentation

The API documentation is [here](https://humahq.stoplight.io/).  Please contant your account manager for a login if you do not have one.

## Quickstart

### Asking a Question and Getting the Answer with Polling

1. Make a copy of `sample.env` called `.env`.  Insert an API key which you generate from the developer screen (e.g. Huma Platform > hamburger menu > developer settings)  

2. Insert you question into `python examples/questions.py`

3. Run the [code sample](./docs/questions.md) with `python examples/questions.py`

### Asking a Question and Getting the Answer with a Webhook Callback

You can use ngrok.com to route a publically facing endpoint to your local instance of the code.  Here are some steps to follow for mac os x:

1. Get an account at [ngrok.com](https://ngrok.com).  This will be used to route the webhook request back to your local computer.  In a production environment you would set a public facing server.

2. Install ngrok locally:

    ```bash
    #for mac os x.  For non-mac os x,  see the instructions on the ngrok portal.
    brew install ngrok
    ```

3. From within the ngrok website, find your key.  Next, register your key on your local computer:

    ```bash
     ngrok config add-authtoken <insert your auth-token>  
    Authtoken saved to configuration file: /Users/<username>/Library/Application Support/ngrok/ngrok.yml
    ```

4. We need to run the webhook code locally so that the Huma Platform can call it when needed.  You will ask a question via the API and then receive a call to your public endpoint when the answer is done.  So we need to publish our local port in a way that it can be reached by Huma Platform.  The below command gives us a website url that gets routed to our local computer where we are going to run our code.:

    ```bash
    ngrok http 5001
    ngrok                                                                                                                                                  (Ctrl+C to quit)

    Introducing Always-On Global Server Load Balancer: https://ngrok.com/r/gslb

    Session Status                online
    Account                       Jim Smith (Plan: Free)
    Version                       3.3.5
    Region                        United States (us)
    Latency                       -
    Web Interface                 http://127.0.0.1:4040
    Forwarding                    https:/xx-your-ip.ngrok-free.app -> http://localhost:5000

    Connections                   ttl     opn     rt1     rt5     p50     p90
                                  0       0       0.00    0.00    0.00    0.00
    ```

    Note: On some mac os x computers, port 5000 seems to be takes with a service.  Accordingly, we have used port 5001.  You can use whatever port you think best.
    
5.  Next we need to register a callback address or webhook in the Huma Platform to tell it what publically facing url to call when an answer is done.  We will put the forwarding address from step 4 into the Huma Platform webhook registration.  You'll also need an authorization code that the webhook will use to call your sample code so that the call is secure.  You can make it whatever you want, it just needs to be the same in the webhook registration and in the sample code. Register your webhook with an authorization code in the Huma Platform > Hamburger Menu > Developer Settings screen.  The type of webhook you need for this example is Questions and then a subtype of Computed See instructions [here](https://humahq.stoplight.io/docs/huma-api/branches/main/d77fdd05735ba-quickstart-guide-for-huma-webhook-api).  Insert your authorization code.

6.  Now we need our code sample that will receive the webhook callback to know what the authorization code is that will be submitted by Huma Platform to our locally running sample code.  The sample code will look for an environment variable of API_CALLBACK_AUTH. To set this so the code sees it, run: 

    ```bash
    export API_CALLBACK_AUTH=<insert your authorization code>
    ```

7.  Run the example code on the port specified above.  In the example above it's 5000.

8.  Submit a question via the [REST API](https://humahq.stoplight.io/docs/huma-api/branches/main/fx5wqnfl9etdg-submit-question) and wait for the callback.

## Modules

- [**Questions**](docs/questions.md): Interact with question-related functionalities.
  - `submit_question`: Submit a question for answer calculation.
  - `check_question_status`: Retrieve the status of an answer calculation.
  - `fetch_answer`: Retrieve the calculated answer.

- [**Histories**](docs/histories.md): Access historical question data.
  - `fetch_history`: Retrieve a list of historical questions.
  - `fetch_history_data`: Retrieve detailed data for a historical question.
  - `submit_history_visual`: Initiate the transformation of historical question data into a file format.
  - `check_history_visual_status`: Check the status of the visual conversion process.
  - `fetch_history_visual_result`: Retrieve the outcome of a visual conversion.

- [**Subscriptions**](docs/subscriptions.md): Manage subscriptions to specific questions.
  - `fetch_subscriptions`: Retrieve a list of subscribed questions.
  - `create_subscription`: Subscribe to a question.
  - `fetch_subscription_status`: Get the subscription status of a question.
  - `fetch_subscription_data`: Retrieve detailed data for a subscribed question.
  - `delete_subscription`: Unsubscribe from a question.

- [**Favorites**](docs/favorites.md): Manage favorite questions.
  - `fetch_favorites`: Retrieve a list of favorite questions.
  - `create_favorite`: Mark a question as a favorite.
  - `fetch_favorite_data`: Retrieve detailed data for a favorite question.
  - `delete_favorite`: Remove a question from favorites.

- [**Quicklinks**](docs/quicklinks.md): Access categorized quicklinks for question submission.
  - `fetch_quicklinks`: Enables users to retrieve categorized quicklinks, which are question titles that users can utilize.

- [**Audits**](docs/audits.md): Retrieve audit trail logs.
  - `fetch_audits`: Retrieve audit trail logs.

- [**Aliases**](docs/aliases.md): Manage aliases for rules.
  - `fetch_aliases`: Retrieve aliases.

