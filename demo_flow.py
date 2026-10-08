import urllib.request
import json

BASE_URL = "http://127.0.0.1:5000"

def send_request(endpoint, method="GET", data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    req_data = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode('utf-8')
            parsed_json = json.loads(body) if body else {}
            return response.status, parsed_json
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
        return e.code, None
    except Exception as e:
        print(f"Connection error: {e}")
        return None, None

def run_demo():
    print("=== BLOCKCHAIN API DEMO FLOW ===")
    
    print("\n[1] Registering Peer Node...")
    status, res = send_request("/nodes/register", method="POST", data={"nodes": ["http://127.0.0.1:5001"]})
    print(f"Status: {status}")
    print(json.dumps(res, indent=4))

    print("\n[2] Submitting New Transaction...")
    tx_data = {
        "sender": "Alice",
        "recipient": "Bob",
        "amount": 500,
        "signature": "mock_sig_hex_12345"
    }
    status, res = send_request("/transactions/new", method="POST", data=tx_data)
    print(f"Status: {status}")
    print(json.dumps(res, indent=4))

    print("\n[3] Mining a New Block...")
    status, res = send_request("/mine", method="POST")
    print(f"Status: {status}")
    print(json.dumps(res, indent=4))

    print("\n[4] Fetching Full Chain...")
    status, res = send_request("/chain", method="GET")
    print(f"Status: {status}")
    print(json.dumps(res, indent=4))

if __name__ == "__main__":
    run_demo()