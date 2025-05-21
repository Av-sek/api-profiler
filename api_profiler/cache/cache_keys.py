def get_cache_key(key):
    return f"API_PROFILER_{key}"

CACHE_KEYS = dict(
    SQL=get_cache_key("SQL"),
    HEADERS=get_cache_key("HEADERS"),
    PARAMS=get_cache_key("PARAMS"),
    BODY=get_cache_key("BODY"),
    RESPONSE=get_cache_key("RESPONSE"),
    TIME=get_cache_key("TIME"),
    STATUS=get_cache_key("STATUS"),
)
