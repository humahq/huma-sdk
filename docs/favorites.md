### Favorites

#### Setting up connection with Favorites

```python
import huma_sdk
favorites_client = huma_sdk.session(service_name="Favorites")
```

#### Function 1: `fetch_favorites`

- **Description**: This Function retrieves a list of questions that a user has marked as favorite.
- **Parameters**:
  - `page`(optional): It represents the requested page number in pagination.
  - `limit`(optional): It represents the maximum number of items to be included per page
  - `question`(optional): It serves as a search query for users to find specific questions based on keywords.
  - `sort_by`(optional): It represents the specific ordering to retrieve records.
  - `order_by`(optional): It represents the name of the field you wish to use for sorting.
  - `is_batch_pages`(optional): It Specifies whether records should be fetched in aggregated batch pages. When set to `True`, the function retrieves data in multiple smaller pages, each containing a maximum of `limit` items, up to a total of `max_page_count` pages.
  - `max_page_count`(optional): It Represents the maximum number of pages to be fetched in one function call when `is_batch_pages` is set to `True`.

- **Example Usage**:

```python


# Retrieve aliases with traditional pagination
favorites = favorites_client.fetch_favorites(page=1, limit=20, question="<write your keyword to search>", order_by="created_date", sort_by=-1)
print("favorites:", favorites)

# Retrieve aliases with aggregated batch pages
favorites = favorites_client.fetch_favorites(limit=20, question="<write your keyword to search>", order_by="created_date", sort_by=-1, is_batch_pages=True, max_page_count=10)
print("favorites (Batch Pages):", favorites)
```

#### Function 2: `create_favorite`

- **Description**: This Function allows users to mark a question as favorite.
- **Parameters**:
  - `ticket_number`: A unique identifier associated with a specific answer calculation process, you can find the ***ticket_number*** in response payload of `fetch_favorites`.

- **Example Usage**:

```python
creation_status = favorites_client.create_favorite(ticket_number="<write your ticket number>")
print("creation_status:", creation_status)
```

#### Function 3: `fetch_favorite_data`

- **Description**: This Function enables users to obtain detailed data for a specific question associated with a ticket_number.
- **Parameters**:
  - `ticket_number`: A unique identifier associated with a specific answer calculation process.
  - `page`(optional): It represents the requested page number in pagination.
  - `limit`(optional): It represents the maximum number of items to be included per page
  - `type`(optional): It represents the format of the particular visualisation type in which the response data is expected. This field accepts one of the `possible_types` associated with the `ticket_number` returned by the `fetch_favorites`. (visit documentation for more details)
  - `is_batch_pages`(optional): It specifies whether records should be fetched in aggregated batch pages. When set to `True`, the function retrieves data in multiple smaller pages, each containing a maximum of `limit` items, up to a total of `max_page_count` pages.
  - `max_page_count`(optional): It represents the maximum number of pages to be fetched in one function call when `is_batch_pages` is set to `True`.

- **Example Usage**:

```python
# Retrieve aliases with traditional pagination
favorites_data = favorites_client.fetch_favorite_data(ticket_number="<write your ticket_number>", page=1, limit=20, type="<write your required visual data type>")
print("favorites_data:", favorites_data)

# Retrieve aliases with aggregated batch pages
favorites_data = favorites_client.fetch_favorite_data(ticket_number="<write your ticket_number>", page=1, limit=20, type="<write your required visual data type>", is_batch_pages=True, max_page_count=10)
print("favorites_data (Batch Pages):", favorites_data)
```

#### Function 4: `delete_favorite`

- **Description**: This Function allows users to remove an item from their favorites list.
- **Parameters**:
  - `ticket_number`: A unique identifier associated with a specific answer calculation process.

- **Example Usage**:

```python
favorites_client.delete_favorite(ticket_number="<write your ticket_number>")
```

**Notes**:
- When using `is_batch_pages=True`, the function fetches data in aggregated batch pages, each containing a maximum of `limit` items.
- The parameter `max_page_count` defines the maximum number of pages to be fetched in one function call when using batch pages. This allows you to control the total number of pages retrieved, providing a more efficient way to manage large datasets.