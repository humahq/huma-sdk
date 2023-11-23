from huma_sdk._resources import _Services
from huma_sdk._services._paginator import _Paginator


class _Aliases(_Services):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _handle_pagination(self, caller_function, page, limit, is_batch_pages, max_page_count, *args, **kwargs):
        paginator = _Paginator(self, module="aliases", is_answer_data=False)
        if is_batch_pages:
            return paginator.paginate_result(max_page_count, caller_function, limit, *args, **kwargs)
        else:
            kwargs.update({"page": page, "limit": limit})
            return caller_function(*args, **kwargs)

    def _fetch_aliases(self, **params):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/aliases"
        return self._make_request(method="GET", url=url, headers=headers, params=params)

    def fetch_aliases(self, page: int=None, limit: int=None, sort_by: int=-1, order_by: str="", search_by: str="", search_for: str="", is_batch_pages: bool=False, max_page_count: int=10):
        params = {"sort_by": sort_by, "order_by": order_by, "search_by": search_by, "search_for": search_for}
        aliases = self._handle_pagination(self._fetch_aliases, page, limit, is_batch_pages, max_page_count, **params)
        return aliases