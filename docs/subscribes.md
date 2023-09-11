### Subscribes

#### Setting up connection with Subscribes

```python
import huma_sdk
self.subscribes_client = huma_sdk.session(service_name="Subscription")
```

#### Function 1: `fetch_subscription`

- **Description**: This Function retrieves a list of questions that a user is currently subscribed to.
- **Parameters**:
  - `page`(optional): It represents the requested page number in pagination.
  - `limit`(optional): It represents the maximum number of items to be included per page
  - `question`(optional): It serves as a search query for users to find specific questions based on keywords.
  - `sort_by`(optional): It represents the specific ordering to retrieve records.
  - `order_by`(optional): It represents the name of the field you wish to use for sorting.
 
- **Example Usage**:

```python
subscription = self.subscribes_client.fetch_subscription(page=1, limit=20, question="<write your keyword to search>", order_by="created_date", sort_by=-1)
print("subscription:", subscription)
```

#### Function 2: `create_subscription`

- **Description**: This Function allows users to subscribe to a specific question.
- **Parameters**:
  - `ticket_number`: A unique identifier associated with a specific answer calculation process.
 
- **Example Usage**:

```python
creation_status = self.subscribes_client.create_subscription(ticket_number="<write your ticket number>")
print("creation_status:", creation_status)
```

#### Function 3: `fetch_subscription_status`

- **Description**: This Function provides the subscription status of a particular question.
- **Parameters**:
  - `question`: A string field that represents the question the user wants to get subscription status of.
 
- **Example Usage**:

```python
subscription_status = self.subscribes_client.fetch_subscription_status(question="<write your question>")
print("subscription_status:", subscription_status)
```

#### Function 4: `fetch_subscription_data`

- **Description**: This Function enables users to obtain detailed subscribed data for a specific question associated with a subscribed id.
- **Parameters**:
  - `subscribed_id`: Subscribed Id is a unique identifier or reference number associated with the subscribed question.
  - `page`(optional): It represents the requested page number in pagination.
  - `limit`(optional): It represents the maximum number of items to be included per page
  - `type`(optional): It represents the format of the particular visualisation type in which the response data is expected. This field accepts one of the possible_types associated with the ticket_number returned by the fetch_subscribes. (visit documentation for more details)
 
- **Example Usage**:

```python
subscription_data = self.subscribes_client.fetch_subscription_data(subscribed_id="<write subscribed_id of question>", page=1, limit=20, type="<write your required visual data type>")
print("subscription_data:", subscription_data)
```

#### Function 5: `delete_subscription`

- **Description**: This Function allows users to unsubscribe from a specific question.
- **Parameters**:
  - `subscribed_id`: Subscribed Id is a unique identifier or reference number associated with the subscribed question.
 
- **Example Usage**:

```python
self.subscribes_client.delete_subscription(subscribed_id="<write subscribed_id of your question>")
```