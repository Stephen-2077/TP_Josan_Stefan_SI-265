import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]

from urllib.parse import urljoin

def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    return urljoin(host, path)

import re

def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return re.split(':', url) == "https"
    pass


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    response = requests.get(url, timeout=10)
    print("Status: ", response.status_code)
    print("Content-Type: ", response.headers['Content-Type'])
    pass


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    results = {}
    response = requests.get(url, timeout=5)
    results["status"] = response.status_code
    results["content-type"] = requests.headers['Content-Type']
    results["length"] = len(response.text)
    return results
    pass


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []

    for url in SITES:
        results.append(check_site(url))

    successful = [r for r in results if r["status"] == 200]
    successful.sort(key=lambda r: r["length"], reverse=True)

    for site in successful:
        print(f'{site["url"]} -> {site["status"]}, {site["length"]} octeți')

    failed = len(results) - len(successful)
    print(f"Reușite: {len(successful)} | Eșuate: {failed}")

def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        r = requests.get(url, timeout=5)
        present = [h for h in SECURITY_HEADERS if h.lower() in r.headers]
        missing = [h for h in SECURITY_HEADERS if h not in present]
        return {
            "present": present,
            "missing": missing,
            "score": int(len(present) / len(SECURITY_HEADERS) * 100)
        }
    except requests.RequestException:
        return {"status": None, "error": "Site inaccesibil"}

def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    
    results = {}
    results["status"] = None
    results["attempts"] = 0

    for i in range(attempts):
        response = requests.get(url)
        results["status"] = response.status_code
        results["attempts"] = results["attempts"] + 1
        if response.status_code == 200:
            break

        if response.status_code >= 400:
            results["error"] = f"Eroare la incercarea {results["attempts"]}, cu codul {response.status_code}"

    return results
    pass
