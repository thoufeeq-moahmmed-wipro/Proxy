# Secure Gate Proxy

Secure Gate Proxy is a simple HTTP proxy server that filters and forwards web traffic based on URL categorization.

## Steps to Run the Project

### 1. Install Required Packages
Ensure Python 3 is installed. Then install the required dependencies:
```sh
pip install netifaces
```

### 2. Initialize Databases
This step sets up authentication and URL categorization databases.

#### Initialize Authentication Database:
```sh
python3 authentication.py
```
Expected output:
```
[DATABASE] Added User: admin
[DATABASE] Added User: user
```

#### Initialize URL Categorization Database:
```sh
python3 categorization.py
```
Expected output:
```
[DATABASE] Added URL: http://www.example.com/ as ALLOW
[DATABASE] Added URL: http://www.google.com/ as ALLOW
[DATABASE] Added URL: http://www.blockedwebsite.com/ as BLOCK
```

### 3. Start the Proxy Server
Run the proxy and enter the network interface (e.g., `eth0`, `nic0`) when prompted:
```sh
python3 http_proxy.py
```
You will see output similar to:
```
Available interfaces: ['lo', 'eth0']
Enter the network interface to bind (e.g., eth0): eth0
[*] Proxy server listening on 192.168.1.100:8080
```

### 4. Test the Proxy with `curl`

#### Without Proxy:
```sh
curl -vvv http://www.example.com -o /dev/null
```
Expected output:
```
HTTP/1.1 200 OK
```

#### With Proxy:
```sh
curl -vvv -x 192.168.1.100:8080 http://www.example.com -o /dev/null
```
Expected output:
- Allowed URLs return:
```
HTTP/1.0 200 OK
```
- Blocked URLs return:
```
HTTP/1.1 403 Forbidden
```

### 5. Test the Proxy in a Browser
1. Open your browser settings.
2. Navigate to **Proxy Settings**.
3. Set **Manual Proxy Configuration**:
   - **HTTP Proxy**: `192.168.1.100`
   - **Port**: `8080`
4. Open a website.
   - Allowed websites should load normally.
   - Blocked websites should display "403 Forbidden".

### 6. Capture Packets in Wireshark
1. Open **Wireshark**.
2. Select the network interface (e.g., `eth0`).
3. Apply a capture filter:
```sh
tcp.port == 8080
```
4. Start capturing traffic.
5. Run `curl` or open a browser to test:
   - You should see HTTP requests going through the proxy.
   - Blocked sites should show `403 Forbidden` in the captured packets.

## Stopping the Proxy
Press `Ctrl + C` to stop the proxy server.
Expected output:
```
[*] Shutting down the proxy server gracefully...
[*] Proxy server stopped.
```
