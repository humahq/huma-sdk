### Subscriptions

#### Setting up connection with Subscriptions

```python
import huma_sdk
subscriptions_client = huma_sdk.session(service_name="Subscriptions")
```

#### Function 1: `fetch_subscriptions`

- **Description**: This Function retrieves a list of questions that a user is currently subscribed to.
- **Parameters**:
  - `page`(optional): It represents the requested page number in pagination.
  - `limit`(optional): It represents the maximum number of items to be included per page
  - `question`(optional): It serves as a search query for users to find specific questions based on keywords.
  - `sort_by`(optional): It represents the specific ordering to retrieve records.
  - `order_by`(optional): It represents the name of the field you wish to use for sorting.
  - `is_batch_pages`(optional): It Specifies whether records should be fetched in aggregated batch pages. When set to `True`, The function retrieves data in smaller, paginated chunks, starting from the specified page (`page` parameter) and continuing up to a total of `max_page_count` pages, each containing a maximum of `limit` items.
  - `max_page_count`(optional): It represents the maximum number of pages to be fetched in one function call when `is_batch_pages` is set to `True`.

- **Example Usage**:

```python
# Retrieve aliases with traditional pagination
subscriptions = subscriptions_client.fetch_subscriptions(page=1, limit=20, question="<write your keyword to search>", order_by="created_date", sort_by=-1)
print("subscription:", subscriptions)

# Retrieve aliases with aggregated batch pages
subscriptions = subscriptions_client.fetch_subscriptions(page=1, limit=20, question="<write your keyword to search>", order_by="created_date", sort_by=-1, is_batch_pages=True, max_page_count=10)
print("subscription (Batch Pages):", subscriptions)
```

#### Function 2: `create_subscription`

- **Description**: This Function allows users to subscribe to a specific question.
- **Parameters**:
  - `ticket_number`: A unique identifier associated with a specific answer calculation process.

- **Example Usage**:

```python
creation_status = subscriptions_client.create_subscription(ticket_number="<write your ticket number>")
print("creation_status:", creation_status)
```

#### Function 3: `fetch_subscription_status`

- **Description**: This Function provides the subscription status of a particular question.
- **Parameters**:
  - `question`: A string field that represents the question the user wants to get subscription status of.

- **Example Usage**:

```python
subscription_status = subscriptions_client.fetch_subscription_status(question="<write your question>")
print("subscription_status:", subscription_status)
```

#### Function 4: `fetch_subscription_data`

- **Description**: This Function enables users to obtain detailed subscribed data for a specific question associated with a subscribed id.
- **Parameters**:
  - `subscribed_id`: Subscribed Id is a unique identifier or reference number associated with the subscribed question.
  - `page`(optional): It represents the requested page number in pagination.
  - `limit`(optional): It represents the maximum number of items to be included per page
  - `type`(optional): It represents the format of the particular visualisation type in which the response data is expected. This field accepts one of the possible_types associated with the ticket_number returned by the fetch_subscribes. (visit documentation for more details)
  - `is_batch_pages`(optional): It Specifies whether records should be fetched in aggregated batch pages. When set to `True`, The function retrieves data in smaller, paginated chunks, starting from the specified page (`page` parameter) and continuing up to a total of `max_page_count` pages, each containing a maximum of `limit` items.
  - `max_page_count`(optional): It represents the maximum number of pages to be fetched in one function call when `is_batch_pages` is set to `True`.

- **Example Usage**:

```python
# Retrieve aliases with traditional pagination
subscription_data = subscriptions_client.fetch_subscription_data(subscribed_id="<write subscribed_id of question>", page=1, limit=20, type="<write your required visual data type>")
print("subscription_data:", subscription_data)

# Retrieve aliases with aggregated batch pages
subscription_data = subscriptions_client.fetch_subscription_data(subscribed_id="<write subscribed_id of question>", page=1, limit=20, type="<write your required visual data type>", is_batch_pages=True, max_page_count=10)
print("subscription_data (Batch Pages):", subscription_data)
```

#### Function 5: `delete_subscription`

- **Description**: This Function allows users to unsubscribe from a specific question.
- **Parameters**:
  - `subscribed_id`: Subscribed Id is a unique identifier or reference number associated with the subscribed question.

- **Example Usage**:

```python
subscriptions_client.delete_subscription(subscribed_id="<write subscribed_id of your question>")
```

**Notes**:
- When using `is_batch_pages=True`, the function fetches data in aggregated batch pages, each containing a maximum of `limit` items.
- The parameter `max_page_count` defines the maximum number of pages to be fetched in one function call when using batch pages. This allows you to control the total number of pages retrieved, providing a more efficient way to manage large datasets.
- For more information about pagination [see here](pagination.md).