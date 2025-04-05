import os
import re
import sys
import socket
import logging
import threading
import sqlite3

# Enable logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_PATH = 'proxy_db.sqlite'
SELECTED_IP_FILE = 'selected_ip.txt'  # <--- NEW

# Function to get network interfaces and IPs
def get_interfaces():
    interfaces = []
    result = os.popen('ifconfig').read()
    interface_pattern = re.compile(r'([a-zA-Z0-9]+):.*?inet\s([\d.]+)', re.DOTALL)
    matches = interface_pattern.findall(result)

    for interface_name, ip_address in matches:
        if interface_name != 'lo':
            interfaces.append((interface_name, ip_address))
    return interfaces

def select_management_ip():
    interfaces = get_interfaces()
    if not interfaces:
        logging.error("No valid interfaces found.")
        sys.exit(1)

    print("Available interfaces:")
    for idx, (iface, ip) in enumerate(interfaces):
        print(f"[{idx}] {iface} : {ip}")
    
    selected_idx = int(input("Select interface index: "))
    if selected_idx < 0 or selected_idx >= len(interfaces):
        logging.error("Invalid selection.")
        sys.exit(1)
    
    selected_iface, selected_ip = interfaces[selected_idx]
    logging.info(f"Selected {selected_iface} with IP {selected_ip}")

    # ✅ Write selected IP to file for multi_curl.sh
    with open(SELECTED_IP_FILE, 'w') as f:
        f.write(selected_ip.strip())
    
    return selected_ip

# Function to check URL in DB
def check_url_status(url):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM urls WHERE url = ?", (url,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0].strip().upper()
    return "ALLOW"  # default to allow

# Forward request to original server
def forward_request(client_socket, request, host, port):
    try:
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect((host, port))
        remote.sendall(request)

        while True:
            data = remote.recv(4096)
            if not data:
                break
            # Inject VIA header
            if b"HTTP/" in data:
                headers, _, body = data.partition(b"\r\n\r\n")
                if b"Via:" not in headers:
                    headers += b"\r\nVia: 1.1 secure_gate_proxy"
                    data = headers + b"\r\n\r\n" + body
            client_socket.send(data)
        remote.close()
    except Exception as e:
        logging.error(f"Error forwarding: {e}")

def handle_client(client_socket):
    try:
        request = client_socket.recv(8192)
        if not request:
            return
        
        request_line = request.split(b"\r\n")[0].decode()
        method, url, _ = request_line.split()

        logging.info(f"[*] Received request for URL: {url}")
        
        # Check if it's a full URL or relative
        if url.startswith("http://"):
            match = re.match(r"http://([^/]+)(/.*)?", url)
            if not match:
                client_socket.close()
                return
            host_port = match.group(1)
            path = match.group(2) or "/"
            if ':' in host_port:
                host, port = host_port.split(":")
                port = int(port)
            else:
                host = host_port
                port = 80
        else:
            logging.warning("Invalid URL format")
            client_socket.close()
            return

        # URL filtering
        base_url = f"http://{host}"
        status = check_url_status(base_url)
        if status == "BLOCK":
            response = b"HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\n\r\n"
            client_socket.send(response)
            logging.info(f"[*] BLOCKED: {base_url}")
        else:
            logging.info(f"[*] ALLOWED: {base_url} -> forwarding to {host}:{port}")
            forward_request(client_socket, request, host, port)
    except Exception as e:
        logging.error(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_proxy_server():
    management_ip = select_management_ip()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((management_ip, 8080))
    server_socket.listen(50)
    logging.info(f"[*] Proxy server listening on {management_ip}:8080")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            logging.info(f"[*] Accepting connection from {client_address}")
            threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
    except KeyboardInterrupt:
        logging.info("Shutting down the proxy server")
        server_socket.close()
        sys.exit(0)

if __name__ == "__main__":
    start_proxy_server()
