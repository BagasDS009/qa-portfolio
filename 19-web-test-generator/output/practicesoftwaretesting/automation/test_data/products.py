"""Product and search test data."""

SEARCH_QUERIES = {
    "valid_exact": "pliers",
    "valid_partial": "ham",
    "valid_multi": "tool",
    "no_results": "xyznonexistent999",
    "special_chars": "<%>",
    "sql_wildcard": "%",
    "empty": "",
}

SORT_OPTIONS = {
    "name_asc": "Name (A - Z)",
    "name_desc": "Name (Z - A)",
    "price_asc": "Price (Low - High)",
    "price_desc": "Price (High - Low)",
}

CATEGORIES = {
    "hand_tools": {"id": "01J", "name": "Hand Tools"},
    "power_tools": {"id": "02J", "name": "Power Tools"},
}
