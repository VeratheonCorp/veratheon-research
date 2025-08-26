#!/usr/bin/env python3
# call_api.py
import argparse
import json
import sys
import time
from urllib import request, error

def call_research_api(base_url: str, symbol: str, timeout: int = 30):
    url = f"{base_url.rstrip('/')}/research"
    payload = json.dumps({"symbol": symbol}).encode("utf-8")
    req = request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, body
    except error.HTTPError as he:
        body = he.read().decode("utf-8") if he.fp else ""
        return he.code, body
    except error.URLError as ue:
        return None, f"Connection error: {ue.reason}"

def main():
    parser = argparse.ArgumentParser(description="Trigger Market Research API")
    parser.add_argument("--base-url", default="http://127.0.0.1:8085", help="Base URL of the API server")
    parser.add_argument("--symbol", default="PG", help="Ticker symbol to analyze")
    args = parser.parse_args()

    print(f"Calling {args.base_url}/research for symbol={args.symbol} ...")
    status, body = call_research_api(args.base_url, args.symbol)
    if status is None:
        print(f"Failed to connect to API: {body}", file=sys.stderr)
        sys.exit(2)

    print(f"HTTP {status}")
    print(body)
    sys.exit(0 if status and 200 <= status < 300 else 1)

if __name__ == "__main__":
    main()