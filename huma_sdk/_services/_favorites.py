from huma_sdk._resources import _Services


class _Favorites(_Services):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def fetch_favorites(self, page: int=1, limit: int=50, sort_by: int=-1, order_by: str="created", question: str=""):
        params = {"page": page, "limit": limit, "sort_by": sort_by, "order_by": order_by, "question": question}
        favorites = self._fetch_favorites(**params)
        return favorites
    
    def create_favorite(self, ticket_number: str=""):
        favorite = self._create_favorite(ticket_number=ticket_number)
        return favorite
    
    def fetch_favorite_data(self, ticket_number: str="", page: int=1, limit: int=20, type: str=""):
        params = {"page": page, "limit": limit, "type": type}
        favorite = self._fetch_favorite_data(ticket_number, **params)
        return favorite
    
    def delete_favorite(self, *args):
        favorite = self._delete_favorite(*args)
        return favorite