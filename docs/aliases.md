### Aliases

#### Setting up connection with Aliases

```python
import huma_sdk
aliases_client = huma_sdk.session(service_name="Aliases")
```

#### Function 1: `fetch_aliases`

- **Description**: This Function enables users to retrieve the aliases.
- **Parameters**:
  - `page`(optional): It represents the requested page number in pagination.
  - `limit`(optional): It represents the maximum number of items to be included per page
  - `sort_by`(optional): It represents the specific ordering to retrieve records.
  - `order_by`(optional): It represents the name of the field you wish to use for sorting.
  - `search_for`(optional): It represents a string keyword to performs a "contains" query for finding matches within the `search_by` field.
  - `search_by`(optional): It represents the field in which you wants to search when using the `search_for` parameter.

- **Example Usage**:

```python
aliases = aliases_client.fetch_aliases(page=1, limit=20, sort_by=-1, order_by="created_date", search_for="", search_by="")
print("aliases:", aliases)
```