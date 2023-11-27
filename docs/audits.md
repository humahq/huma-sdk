### Audits

#### Setting up connection with Audits

```python
import huma_sdk
audits_client = huma_sdk.session(service_name="Audits")
```

#### Function 1: `fetch_audits`

- **Description**: This Function enables users to retrieve the audit trail log.
- **Parameters**:
  - `page`(optional): It represents the requested page number in pagination.
  - `limit`(optional): It represents the maximum number of items to be included per page
  - `sort_by`(optional): It represents the specific ordering to retrieve records.
  - `order_by`(optional): It represents the name of the field you wish to use for sorting.
  - `endpoint`(optional): It represents the name of the endpoint you want to search the audit-logs for.
  - `content`(optional): It represents the string keyword user wants to search in content field.
  - `is_batch_pages`(optional): It Specifies whether records should be fetched in aggregated batch pages. When set to `True`, The function retrieves data in smaller, paginated chunks, starting from the specified page (`page` parameter) and continuing up to a total of `max_page_count` pages, each containing a maximum of `limit` items.
  - `max_page_count`(optional): It Represents the maximum number of pages to be fetched in one function call when `is_batch_pages` is set to `True`.

- **Example Usage**:

```python
# Retrieve aliases with traditional pagination
audits = audits_client.fetch_audits(page=1, limit=20, sort_by=-1, order_by="created_date", endpoint="<write name of the endpoint to search>", content="<write content to search>")
print("audits:", audits)

# Retrieve aliases with aggregated batch pages
audits = audits_client.fetch_audits(page=1, limit=20, sort_by=-1, order_by="created_date", endpoint="<write name of the endpoint to search>", content="<write content to search>" is_batch_pages=True, max_page_count=10)
print("audits (Batch Pages):", audits)
```


**Notes**:
- When using `is_batch_pages=True`, the function fetches data in aggregated batch pages, each containing a maximum of `limit` items.
- The parameter `max_page_count` defines the maximum number of pages to be fetched in one function call when using batch pages. This allows you to control the total number of pages retrieved, providing a more efficient way to manage large datasets.
- For more information about pagination [see here](pagination.md).