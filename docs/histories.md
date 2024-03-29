### Histories

#### Setting up connection with Histories

```python
import huma_sdk
histories_client = huma_sdk.session(service_name="Histories")
```

#### Function 1: `fetch_history`

- **Description**: This Function enables users to retrieve a paginated list of their historical questions.
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
history = histories_client.fetch_history(page=1, limit=20, question="<write your keyword to search>", order_by="created_date", sort_by=-1)
print("history:", history)

# Retrieve aliases with aggregated batch pages
history = histories_client.fetch_history(page=1, limit=20, question="<write your keyword to search>", order_by="created_date", sort_by=-1, is_batch_pages=True, max_page_count=10)
print("history (Batch Pages):", history)
```

#### Function 2: `fetch_history_data`

- **Description**: This Function enables users to retrieve a paginated list of their historical questions.
- **Parameters**:
  - `ticket_number`: A unique identifier associated with a specific answer calculation process, you can find the ***ticket_number*** in response payload of `fetch_history`.
  - `page`(optional): It represents the requested page number in pagination.
  - `limit`(optional): It represents the maximum number of items to be included per page
  - `type`(optional): It represents the format of the particular visualisation type in which the response data is expected. This field accepts one of the possible_types associated with the ticket_number returned by the fetch_history. (visit documentation for more details)
  - `is_batch_pages`(optional): It Specifies whether records should be fetched in aggregated batch pages. When set to `True`, The function retrieves data in smaller, paginated chunks, starting from the specified page (`page` parameter) and continuing up to a total of `max_page_count` pages, each containing a maximum of `limit` items.
  - `max_page_count`(optional): It represents the maximum number of pages to be fetched in one function call when `is_batch_pages` is set to `True`.

- **Example Usage**:

```python
# Retrieve aliases with traditional pagination
history = histories_client.fetch_history_data(ticket_number="<write your ticket number>", page=1, limit=20, type="<write required visual data type>")
print("history:", history)

# Retrieve aliases with aggregated batch pages
history = histories_client.fetch_history_data(ticket_number="<write your ticket number>", page=1, limit=20, type="<write required visual data type>", is_batch_pages=True, max_page_count=10)
print("history (Batch Pages):", history)
```

#### Function 3: `submit_history_visual`

- **Description**: This Function serves as the initial step in transforming an answer's visual representation into a file format.
- **Parameters**:
  - `ticket_number`: A unique identifier associated with a specific answer calculation process.
  - `file_type`: It represents the format of the file required by the user. Available file_types are "pdf", "csv" and "pptx".
  - `visual_type`(optional): It represents the format of the particular visualisation type in which the file is expected. This field accepts one of the possible_types associated with the ticket_number returned by the fetch_history. (visit documentation for more details)

- **Example Usage**:

```python
submission_status = histories_client.submit_history_visual(ticket_number="<write your ticket number>", file_type="<write your required file type>",visual_type="<write your required visual type>")
print("submission_status:", submission_status)
```

#### Function 4: `check_history_visual_status`

- **Description**: This Function returns the current status of the history visual creation, allowing users to monitor the progress and take action when the status indicates completion.
- **Parameters**:
  - `conversion_id`: It is a Unique reference id of the conversion process, returned by the `submit_history_visual`.

- **Example Usage**:

```python
conversion_status = histories_client.check_history_visual_status(conversion_id="<write conversion id returned from submit_history_visual>")
print("conversion_status:", conversion_status)
```

#### Function 5: `fetch_history_visual_result`

- **Description**: This Function empowers users to seamlessly obtain the outcome of a visual conversion job and access the converted file for download.
- **Parameters**:
  - `conversion_id`: It is a Unique reference id of the conversion process, returned by the `submit_history_visual`.

- **Example Usage**:

```python
result = histories_client.fetch_history_visual_result("<write conversion id returned from submit_history_visual>")
print("result:", result)
```

**Notes**:
- When using `is_batch_pages=True`, the function fetches data in aggregated batch pages, each containing a maximum of `limit` items.
- The parameter `max_page_count` defines the maximum number of pages to be fetched in one function call when using batch pages. This allows you to control the total number of pages retrieved, providing a more efficient way to manage large datasets.
- For more information about pagination [see here](pagination.md).