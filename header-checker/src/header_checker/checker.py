import sys

import requests

REQUIRED = [
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Content-Security-Policy",
    "Referrer-Policy",
]


def check_url(url):
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        return response.status_code, None

    results = {}
    for name in REQUIRED:
        if name in response.headers:
            results[name] = True
        else:
            results[name] = False
    return response.status_code, results


def main():
    urls = sys.argv[1:]
    if not urls:
        print("Usage: python checker.py <url> [<url> ...]")
        sys.exit(1)

    for url in urls:
        print(url)
        try:
            status, results = check_url(url)
        except requests.exceptions.RequestException:
            print("Error: cannot connect")
            print()
            continue

        if results is None:
            print(f"Skipped: status {status}")
            print()
            continue

        for name, ok in results.items():
            if ok:
                print(f"{name}: OK")
            else:
                print(f"{name}: MISSING")

        print()


if __name__ == "__main__":
    main()
