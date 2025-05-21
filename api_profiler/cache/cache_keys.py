def get_cache_key(key):
    return f"API_PROFILER_{key}"

FLAGS = dict()

features = ["sql", "headers", "params", "body", "response", "response-headers"]

for feature in features:
    FLAGS[feature.upper()] = get_cache_key(feature.upper())


LIMIT_SQL_QUERIES = get_cache_key("LIMIT_SQL_QUERIES")