### Quicklinks

#### Setting up connection with Quicklinks

```python
import huma_sdk
quicklinks_client = huma_sdk.session(service_name="Quicklinks")
```

#### Function 1: `fetch_quicklinks`

- **Description**: This Function enables users to retrieve categorized quicklinks, which are question titles that users can utilize via the  `submit_question` function.
 
- **Example Usage**:

```python
quicklinks = quicklinks_client.fetch_quicklinks()
print("quicklinks:", quicklinks)
```