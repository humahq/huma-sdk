import json


def parse_json_response(response_text):
    try:
        response_data = json.loads(response_text)
        return response_data
    except json.JSONDecodeError as e:
        return response_text