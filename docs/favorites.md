### Favorites

#### Setting up connection with Favorites

```python
import huma_sdk
self.favorites_client = huma_sdk.session(service_name="Favorites")
```

#### Function 1: `fetch_favorites`

- **Description**: This Function retrieves a list of questions that a user has marked as favorite.
- **Parameters**:
  - `page`(optional): It represents the requested page number in pagination.
  - `limit`(optional): It represents the maximum number of items to be included per page
  - `question`(optional): It serves as a search query for users to find specific questions based on keywords.
  - `sort_by`(optional): It represents the specific ordering to retrieve records.
  - `order_by`(optional): It represents the name of the field you wish to use for sorting.
 
- **Example Usage**:

```python
favorites = self.favorites_client.fetch_favorites(page=1, limit=20, question="<write your keyword to search>", order_by="created_date", sort_by=-1)
print("favorites:", favorites)
```

#### Function 2: `create_favorite`

- **Description**: This Function allows users to mark a question as favorite.
- **Parameters**:
  - `ticket_number`: A unique identifier associated with a specific answer calculation process.
 
- **Example Usage**:

```python
creation_status = self.favorites_client.create_favorite(ticket_number="<write your ticket number>")
print("creation_status:", creation_status)
```

#### Function 3: `fetch_favorite_data`

- **Description**: This Function enables users to obtain detailed data for a specific question associated with a ticket_number.
- **Parameters**:
  - `ticket_number`: A unique identifier associated with a specific answer calculation process.
  - `page`(optional): It represents the requested page number in pagination.
  - `limit`(optional): It represents the maximum number of items to be included per page
  - `type`(optional): It represents the format of the particular visualisation type in which the response data is expected. This field accepts one of the possible_types associated with the ticket_number returned by the fetch_subscribes. (visit documentation for more details)
 
- **Example Usage**:

```python
favorites_data = self.favorites_client.fetch_favorite_data(ticket_number="<write your ticket_number>", page=1, limit=20, type="<write your required visual data type>")
print("favorites_data:", favorites_data)
```

#### Function 4: `delete_favorite`

- **Description**: This Function allows users to remove an item from their favorites list.
- **Parameters**:
  - `ticket_number`: A unique identifier associated with a specific answer calculation process.

- **Example Usage**:

```python
self.favorites_client.delete_favorite(ticket_number="<write your ticket_number>")
```