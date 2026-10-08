# BLCH9X2 — Assignment 8: REST API and Networking Lab
**Student Name:** Olonda Thoba Holizwi Masuku  
**Course:** Master of Financial Engineering (MFE), University of Johannesburg  
**Module:** BLCH9X2 Blockchain 

---

## 1. Architectural Overview
This repository implements a lightweight, production-compliant Flask REST API for an in-memory blockchain ledger. In accordance with course design patterns, the codebase is modularized into three core components:
* **`api.py`**: The Flask application entry point, routing layer, and endpoint controller.
* **`network.py`**: Node directory management, address normalisation, chain validation, and conflict resolution (longest-chain rule).
* **`explorer.py`**: Human-readable terminal and web-based audit view formatting the canonical chain.

---

## 2. API Endpoint Specification

| Method | Path | Purpose / Description | Success Status | Error Status |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/chain` | Returns the full blockchain ledger and current height. | `200 OK` | — |
| `POST` | `/transactions/new` | Submits a new transaction to the local mempool. | `201 Created` | `400 Bad Request` |
| `POST` | `/mine` | Executes Proof-of-Work difficulty search and mines a block. | `200 OK` | — |
| `GET` | `/nodes` | Lists all registered peer node URLs (JSON list). | `200 OK` | — |
| `POST` | `/nodes/register` | Registers new peer node addresses into the local table. | `201 Created` | `400 Bad Request` |
| `GET` | `/explorer` | Minimal HTML block explorer view. | `200 OK` | — |

---

## 3. Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/blch9x2-assignment-8.git](https://github.com/your-username/blch9x2-assignment-8.git)
   cd blch9x2-assignment-8
   ```
2. Install dependencies:
   ```bash
   pip install flask
   ```

---

## 4. Running the Application
To run the live server locally (bound strictly to `127.0.0.1:5000` for security compliance):
```bash
python api.py
```
---

## 5. Demo Execution Commands
### Powershell
```powershell
# 1. Fetch Chain
Invoke-RestMethod [http://127.0.0.1:5000/chain](http://127.0.0.1:5000/chain)

# 2. Submit Transaction
$body = '{"sender":"Alice","recipient":"Bob","amount":10000}'
Invoke-RestMethod -Method Post -Uri [http://127.0.0.1:5000/transactions/new](http://127.0.0.1:5000/transactions/new) -ContentType 'application/json' -Body $body

# 3. Mine Block
Invoke-RestMethod -Method Post -Uri [http://127.0.0.1:5000/mine](http://127.0.0.1:5000/mine)

# 4. Register Nodes
$nodesBody = '{"nodes":["[http://127.0.0.1:5001](http://127.0.0.1:5001)"]}'
Invoke-RestMethod -Method Post -Uri [http://127.0.0.1:5000/nodes/register](http://127.0.0.1:5000/nodes/register) -ContentType 'application/json' -Body $nodesBody
```

### curl (Windows/Command Prompt)
```DOS
curl.exe -s [http://127.0.0.1:5000/chain](http://127.0.0.1:5000/chain)
curl.exe -s -X POST [http://127.0.0.1:5000/transactions/new](http://127.0.0.1:5000/transactions/new) -H "Content-Type: application/json" -d "{\"sender\":\"Alice\",\"recipient\":\"Bob\",\"amount\":10000}"
curl.exe -s -X POST [http://127.0.0.1:5000/mine](http://127.0.0.1:5000/mine)
```

---

## 6. Classroom Assumptions & Policy Notes
* **Mining Policy:** Open classroom mining is permitted exclusively on `127.0.0.1` for local demonstrations and testing. Production deployments would require mutual TLS, API keys, or authenticated consortium consensus.
* **Idempotency:** The transaction endpoint utilizes a naive append approach for classroom clarity, where repeated identical POST requests create distinct mempool entries.
