# secure_gate_proxy

## Secure Gate Proxy

Secure Gate Proxy is a lightweight MITM (Man-in-the-Middle) HTTP proxy built in Python. It intercepts, filters, and forwards HTTP requests while enforcing authentication and URL categorization.

## Features:
- **Proxy Server (`http_proxy.py`)**:
  - Forwards HTTP requests to target servers.
  - Supports HTTP/1.1.
  - Adds a `Via` header to indicate proxied requests.
  - Runs on a specified network interface (e.g., `eth0/nic0`).
- **Authentication (`authentication.py`)**:
  - Uses a SQLite database (`users.db`) to store and validate users.
  - Supports Basic Authentication via `Authorization` headers.
- **URL Categorization (`categorization.py`)**:
  - Maintains a database of accepted and restricted URLs.
  - Allows only permitted URLs through the proxy.
- **Logging**:
  - Logs accepted connections.
  - Logs proxy startup and shutdown messages.

## Folder Structure:
```
secure_gate_proxy/
├── authentication.py       # Handles user authentication via SQLite database
├── categorization.py       # Manages URL filtering and categorization
├── database_setup.py       # Initializes the user database
├── http_proxy.py           # The core HTTP proxy server
├── users.db                # SQLite database for authentication
└── README.md               # Project documentation (this file)

## Usage:
### Start the Proxy Server:
```sh
python http_proxy.py
```
### Use Proxy with `curl`:
#### Direct Request (Without Proxy):
```sh
curl -vvv http://www.example.com -o /dev/null
```
#### Request via Proxy:
```sh
curl -vvv -x 10.22.185.15:8080 http://www.example.com -o /dev/null
```

## Expected Output:
- **Direct Request:** `HTTP/1.1 200 OK`
- **Proxy Request:** `HTTP/1.0 200 OK` with a `Via` header.

## Notes:
- Ensure the proxy runs on `enp3s0/lo` IP.
- Verify traffic using `tcpdump` or Wireshark.

## License:
This project is open-source under the MIT License.

