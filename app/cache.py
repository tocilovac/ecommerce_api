# cache.py — placeholder for caching logic

# You can later integrate Redis or use functools.lru_cache

_cached_products = None

def get_cached_products():
    return _cached_products

def set_cached_products(data):
    global _cached_products
    _cached_products = data

def clear_cached_products():
    global _cached_products
    _cached_products = None
