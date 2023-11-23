from huma_sdk._resources import _Services
from huma_sdk._services._paginator import _Paginator


class _Favorites(_Services):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _handle_pagination(self, caller_function, page, limit, is_batch_pages, max_page_count, is_answer_data:bool= True, *args, **kwargs):
        paginator = _Paginator(self, module="favorites", is_answer_data=is_answer_data)
        if is_batch_pages:
            return paginator.paginate_result(max_page_count, caller_function, limit, *args, **kwargs)
        else:
            kwargs.update({"page": page, "limit": limit})
            return caller_function(*args, **kwargs)

    def _fetch_favorites(self, **params):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/favorites"
        return self._make_request(method="GET", url=url, headers=headers, params=params)

    def _create_favorite(self, **payload):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/favorites"
        return self._make_request(method="POST", url=url, headers=headers, json=payload)

    def _fetch_favorite_data(self, ticket_number, **params):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/favorites/{ticket_number}/data"
        return self._make_request(method="GET", url=url, headers=headers, params=params)

    def _delete_favorite(self, ticket_number):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/favorites/{ticket_number}/delete"
        return self._make_request(method="DELETE", url=url, headers=headers)

    def fetch_favorites(self, page: int=1, limit: int=50, sort_by: int=-1, order_by: str="created", question: str="", is_batch_pages: bool=False, max_page_count: int=10):
        params = {"sort_by": sort_by, "order_by": order_by, "question": question}
        favorites = self._handle_pagination(self._fetch_favorites, page, limit, is_batch_pages, max_page_count, False, **params)
        return favorites

    def create_favorite(self, ticket_number: str=""):
        favorite = self._create_favorite(ticket_number=ticket_number)
        return favorite

    def fetch_favorite_data(self, ticket_number: str="", page: int=1, limit: int=20, type: str="", is_batch_pages: bool=False, max_page_count: int=10):
        args, params = (ticket_number, ), {"type": type}
        favorite = self._handle_pagination(self._fetch_favorite_data, page, limit, is_batch_pages, max_page_count, True, *args, **params)
        return favorite

    def delete_favorite(self, *args,**kwargs):
        favorite = self._delete_favorite(*args,**kwargs)
        return favorite