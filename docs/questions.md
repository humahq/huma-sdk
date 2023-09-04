### Questions

#### Setting up Connection with Questions

```python
import huma_sdk
self.questions_client = huma_sdk.session(service_name="Questions")
```

#### Function 1: `submit_question`

- **Description**: This Function initiates the answer calculation process by sending a question to the server.
- **Parameters**:
  - `question`:A string representing the question you want to ask.
  - `commands`(optional): An array of reserved phrases that instruct the server on how to process the question. (visit documentation for more details)

- **Example Usage**:

```python
submission_status = self.questions_client.submit_question(question="<write your question>", commands=["<write command_1>", "<write command_2>"])
print("submission_status:", submission_status)
```

#### Function 2: `check_question_status`

- **Description**: This Function retrieves the status of the answer calculation process using the ticket number.
- **Parameters**:
  - `ticket_number`: A unique identifier associated with a specific answer calculation process, returned by submit_question function.

- **Example Usage**:

```python
calculation_status = self.questions_client.check_question_status(ticket_number="<write your ticket number>")
print("calculation_status:", calculation_status)
```

#### Function 3: `fetch_answer`

- **Description**: This Function retrieves the calculated question result based on the provided ticket number, This function also supports pagination but only in case of the answer data format that supports table visual.
- **Parameters**:
  - `ticket_number`: A unique identifier associated with a specific answer calculation process, returned by submit_question function.
  - `page`(optional): It represents the requested page number in pagination.
  - `limit`(optional): It represents the maximum number of items to be included per page

- **Example Usage**:

```python
answer = self.questions_client.fetch_answer(ticket_number="<write your ticket number>", page=1, limit=20)
print("answer:", answer)
```