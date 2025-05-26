def get_cache_key(key):
    return f"API_PROFILER_{key}"

FLAGS = dict()

features = ["sql", "headers", "params", "body", "response", "response-headers", 'all']

for feature in features:
    if feature != 'all':
        FLAGS[feature.upper()] = get_cache_key(feature.upper())


LIMIT_SQL_QUERIES = get_cache_key("LIMIT_SQL_QUERIES")