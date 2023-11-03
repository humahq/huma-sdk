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
 
- **Example Usage**:

```python
audits = audits_client.fetch_audits(page=1, limit=20, sort_by=-1, order_by="created_date", endpoint="<write name of the endpoint to search>", content="<write content to search>")
print("audits:", audits)
```