import time
from huma_sdk.utils._log_utils import get_logger


class _Paginator:
    def __init__(self, resource_client, module, is_answer_data):
        self.resource_client = resource_client
        self.module = module
        self.is_answer_data = is_answer_data
        self.logger = get_logger(__name__)

    def _call_api(self, caller_function, page=1, limit=10, *args, **kwargs):
        kwargs.update({'page': page, "limit": limit})
        return caller_function(*args, **kwargs)

    def _validate_max_page_count(self, max_page_count):
        return max_page_count if isinstance(max_page_count, int) else 10

    def _log_total_records_info(self, total_records_present):
        self.logger.info(f"Total records present: {total_records_present}")

    def _calculate_pages_and_records(self, max_page_count, limit, result_response):
        pages_to_fetch = min(max_page_count, result_response['metadata'].get('page_count', 0))
        total_records = min(pages_to_fetch * int(limit), result_response['metadata'].get('total_count', 0))
        return pages_to_fetch, total_records

    def _log_restricting_info(self, start_index, end_index, max_page_count, limit):
        self.logger.info(f"Fetching records  {start_index} to {end_index} records index due to max_page_count {max_page_count} with per page limit {limit}.")

    def _log_fetch_info(self, next_page, limit, total_records):
        self.logger.info(f"Successfully fetched {limit} records out of {total_records}. Fetching records for page {next_page}.")

    def _log_fetch_page_info(self, page, page_limit, pages_to_fetch, total_records=None):
        start_record_index =  ((page-1)*page_limit)+1
        if page != pages_to_fetch:
            self.logger.info(f"Fetched records from index {start_record_index} to {page*page_limit} on page {page}.")
        else:
            self.logger.info(f"Fetched records from index {start_record_index} to {((page-1)*page_limit)+total_records} on page {page}.")
            self.logger.info(f"Successfully fetched all the records of this batch.")

    def fetch_answer_data(self, result_response, caller_function, next_page, limit, pages_to_fetch, *args, **kwargs):
        answer_key = self.module if self.module == "subscriptions" else "answer"
        answer_data = result_response.get(answer_key, {}).get('data', [])
        for page in range(next_page, pages_to_fetch+1):
            result_response = self._call_api(caller_function, page, limit, *args, **kwargs)
            new_data = result_response.get(answer_key, {}).get('data', [])
            answer_data.extend(new_data)

            self._log_fetch_page_info(page, limit, pages_to_fetch, total_records=len(new_data))

        # Update the response structure
        result_response[answer_key]['data'] = answer_data
        return result_response

    def fetch_records(self, result_response, caller_function, next_page, limit, pages_to_fetch, *args, **kwargs):
        answer_data = result_response.get(self.module, {})
        for page in range(next_page, pages_to_fetch+1):
            result_response = self._call_api(caller_function, page, limit, *args, **kwargs)
            new_data = result_response.get(self.module, {})
            answer_data.extend(new_data)

            self._log_fetch_page_info(page, limit, pages_to_fetch, total_records=len(new_data))

        # Update the response structure
        result_response[self.module] = answer_data
        return result_response

    def paginate_result(self, max_page_count, caller_function, page, limit, *args, **kwargs):
        try:
            result_response = self._call_api(caller_function, page, limit, *args, **kwargs)

            if 'metadata' in result_response and result_response['metadata'].get('has_next_page'):
                max_page_count = self._validate_max_page_count(max_page_count)
                total_records_present = result_response['metadata'].get('total_count', 0)

                self._log_total_records_info(total_records_present)
                pages_to_fetch, total_records = self._calculate_pages_and_records((page-1)+max_page_count, limit, result_response)

                start_record_index =  ((page-1)*limit)+1
                self.logger.info(f"Index Range of Records to be fetched in this batch: {start_record_index}-{total_records}")
                self._log_fetch_page_info(page, limit, pages_to_fetch)

                # Fetch additional pages
                my_args = (result_response, caller_function, page+1, limit, pages_to_fetch, *args)
                result_response = self.fetch_answer_data(*my_args, **kwargs) if self.is_answer_data else self.fetch_records(*my_args, **kwargs)

            return result_response

        except Exception as e:
            self.logger.error(f'Failed to fetch paginated record because {e}')