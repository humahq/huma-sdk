from huma_sdk._services import _aliases, _quicklinks, _questions, _histories, _favorites, _subscriptions, _webhooks
from huma_sdk._async_services import _questions as _questions_async, _threads

AVAILABLE_SERVICES = ("Quicklinks", "Aliases", "Audits", "Questions", "Histories", "Favorites", "Subscriptions", "Webhooks")

SERVICE_MAPPINGS = {
    "QuicklinksSync": _quicklinks._Quicklinks,
    "AliasesSync": _aliases._Aliases,
    "QuestionsSync": _questions._Questions,
    "HistoriesSync": _histories._Histories,
    "FavoritesSync": _favorites._Favorites,
    "SubscriptionsSync": _subscriptions._Subscriptions,
    "WebhooksSync": _webhooks._Webhooks,
    "QuestionsAsync": _questions_async._AsyncQuestions,
    "ThreadsAsync": _threads._Threads
}