from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse


def build_url(base_url: str, params: dict[str, str] | None = None) -> str:
    if not params:
        return base_url

    url_parts = list(urlparse(base_url))
    query = dict(parse_qsl(url_parts[4]))  # preserve existing query params
    query.update(params)
    url_parts[4] = urlencode(query, doseq=True)  # doseq=True supports lists

    return urlunparse(url_parts)


def has_rel(link, rel: str) -> bool:
    """True when *link* carries the relation *rel*.

    A link's ``rel`` is one relation or a list of them (RWPM), and *link* may
    be a ``Link`` model or the dict it serialises to, so every lookup gets the
    list case right instead of only the ones that remembered it.
    """
    value = link.get("rel") if isinstance(link, dict) else getattr(link, "rel", None)
    if not value:
        return False
    return rel in value if isinstance(value, list) else value == rel
