from huma_sdk._resources import _Services
from huma_sdk._services._paginator import _Paginator


class _Audits(_Services):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _handle_pagination(self, caller_function, page, limit, is_batch_pages, max_page_count, *args, **kwargs):
        paginator = _Paginator(self, module="audit_trail", is_answer_data=False)
        if is_batch_pages:
            return paginator.paginate_result(max_page_count, caller_function, limit, *args, **kwargs)
        else:
            kwargs.update({"page": page, "limit": limit})
            return caller_function(*args, **kwargs)

    def _fetch_audits(self, **params):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/audits"
        return self._make_request(method="GET", url=url, headers=headers, params=params)

    def fetch_audits(self, page: int=1, limit: int=20, sort_by: int=-1, order_by: str="created", endpoint: str="", content: str="", is_batch_pages: bool=False, max_page_count: int=10):
        params = {"sort_by": sort_by, "order_by": order_by, "endpoint": endpoint, "content": content}
        audits = self._handle_pagination(self._fetch_audits, page, limit, is_batch_pages, max_page_count, **params)
        return audits