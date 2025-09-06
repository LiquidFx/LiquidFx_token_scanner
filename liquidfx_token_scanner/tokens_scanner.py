"""
tokens_scanner.py

Scanner for new ERC-20 tokens on Ethereum and Polygon networks.
Logs token contract addresses, symbols, and names.
"""

import requests
import time

API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjVlMjZjZmUxLTc5ZjItNGJkMC1hYjc5LWUwZDE3NDFlNDA4YyIsIm9yZ0lkIjoiNDY5MzEzIiwidXNlcklkIjoiNDgyODAzIiwidHlwZUlkIjoiZGMxNmViNzItNTAwYy00YzBlLWI4ZDctYTc0ODVmNTMyZGRhIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NTcwOTk1ODAsImV4cCI6NDkxMjg1OTU4MH0.7fvXPyNzRRbNrxU3JL0QPX6C_qoMtjPOu2WlucP2cmg'
GITHUB_USERNAME = 'LiquidFx'

ETHEREUM_API_URL = 'https://api.mobula.watch/v1/ethereum/new-tokens'
POLYGON_API_URL = 'https://api.mobula.watch/v1/polygon/new-tokens'

HEADERS = {'Authorization': f'Bearer {API_KEY}'}
LOG_FILE = f'new_tokens_log_{GITHUB_USERNAME}.txt'

def fetch_new_tokens(api_url):
    try:
        response = requests.get(api_url, headers=HEADERS)
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.RequestException as e:
        print(f"API request error: {e}")
        return []

def log_tokens(tokens, network):
    with open(LOG_FILE, 'a') as f:
        for token in tokens:
            line = f"{network} | {token['contract_address']} | {token['symbol']} | {token['name']}\n"
            f.write(line)
            print(line.strip())

def main(poll_interval=60):
    print("Starting new token scanner...")
    seen_tokens = set()
    while True:
        eth_tokens = fetch_new_tokens(ETHEREUM_API_URL)
        poly_tokens = fetch_new_tokens(POLYGON_API_URL)
        new_tokens = [t for t in eth_tokens + poly_tokens if t['contract_address'] not in seen_tokens]
        for token in new_tokens:
            seen_tokens.add(token['contract_address'])
        if new_tokens:
            log_tokens(new_tokens, 'Ethereum/Polygon')
        time.sleep(poll_interval)

if __name__ == "__main__":
    main()

