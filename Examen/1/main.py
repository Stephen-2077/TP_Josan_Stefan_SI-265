from checker import build_url, is_https, show_response, check_site,
scan_sites, check_headers, retry_check

# Partea 1
print(build_url("example.com", "login"))
print(build_url("example.com", "/login"))
print(is_https("https://example.com"))
print(is_https("http://example.com"))

# Partea 2
show_response("https://example.com"))

# Partea 3
check_site("https://example.com")

# Partea 4
scan_sites()

# Partea 5
check_headers("https://example.com")

# Partea 6
retry_check("https://example.com")
