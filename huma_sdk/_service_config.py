from huma_sdk._services import _aliases, _audits, _quicklinks, _questions, _histories, _favorites, _subscribes

AVAILABLE_SERVICES = ("Quicklinks", "Aliases", "Audits", "Questions", "Histories", "Favorites", "Subscribes")

SERVICE_MAPPINGS = {
    "Quicklinks": _quicklinks._Quicklinks,
    "Aliases": _aliases._Aliases,
    "Audits": _audits._Audits,
    "Questions": _questions._Questions,
    "Histories": _histories._Histories,
    "Favorites": _favorites._Favorites,
    "Subscribes": _subscribes._Subscribes
}