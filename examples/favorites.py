import huma_sdk
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError


class HumaSDKFavoritesClient:
    def __init__(self):
        self.favorites_client = huma_sdk.session(service_name="Favorites")

    def handle_exception(self, exception):
        if isinstance(exception, UnauthorizedException):
            print("Unauthorized:", exception)
        elif isinstance(exception, ResourceNotExistsError):
            print("Resource Not Exists:", exception)
        else:
            print("An unexpected error occurred:", exception)

    def fetch_favorites(self, page: int=1, limit: int=50, sort_by: int=-1, order_by: str="", question: str=""):
        try:
            favorites = self.favorites_client.fetch_favorites(page=page, limit=limit, sort_by=sort_by, order_by=order_by, question=question)
            print(favorites)
        except Exception as e:
            self.handle_exception(e)

    def create_favorite(self, ticket_number: str=""):
        try:
            favorite = self.favorites_client.create_favorite(ticket_number=ticket_number)
            print(favorite)
        except Exception as e:
            self.handle_exception(e)

    def fetch_favorite_data(self, ticket_number: str="", page: int=1, limit: int=20, type: str=""):
        try:
            favorite = self.favorites_client.fetch_favorite_data(ticket_number, page=page, limit=limit, type=type)
            print(favorite)
        except Exception as e:
            self.handle_exception(e)

    def delete_favorite(self, ticket_number: str=""):
        try:
            favorite = self.favorites_client.delete_favorite(ticket_number)
            print(favorite)
        except Exception as e:
            self.handle_exception(e)


def main():
    favorites_client = HumaSDKFavoritesClient()

    # Example usage
    favorites_client.fetch_favorites(page=1, limit=50, sort_by=-1, order_by="", question="")
    
    ticket_number = "<write your ticket number>" # will be included in 'fetch_favorites'
    favorites_client.create_favorite(ticket_number=ticket_number)

    type: str = "<write one of the possible types>" # will be included in resonse payload of 'fetch_favorites', visit documentation for more details
    favorites_client.fetch_favorite_data(ticket_number, page=1, limit=10, type=type)
    favorites_client.delete_favorite(ticket_number)

if __name__ == "__main__":
    main()
