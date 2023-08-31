from huma_sdk._services import _aliases, _audits, _quicklinks

AVAILABLE_SERVICES = ("Quicklinks", "Aliases", "Audits")

SERVICE_MAPPINGS = {
    "Quicklinks": _quicklinks._Quicklinks,
    "Aliases": _aliases._Aliases,
    "Audits": _audits._Audits
}