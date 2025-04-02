# http_proxy.py

import socket
import threading
import re
from categorization import URLCategorization

# Proxy settings (listening on eth0/nic0)
PROXY_HOST = "0.0.0.0"  # Listen on all network interfaces
PROXY_PORT = 8080

# Initialize URL categorization
url_filter = URLCategorization()

def extract_hostname(url):
    """Extract hostname from URL."""
    match = re.search(r'http[s]?://([^/]+)', url)
    if match:
        return match.group(1)
    return url

def handle_client(client_socket):
    """Handles incoming client requests."""
    try:
        request = client_socket.recv(4096).decode(errors="ignore")
        if not request:
            return

        # Parse HTTP request
        request_line = request.split("\n")[0]
        method, url, _ = request_line.split()
        hostname = extract_hostname(url)
        print(f"[*] Received {method} request for {hostname}")

        # URL Categorization
        if url_filter.is_blocked(hostname):
            response = "HTTP/1.1 403 Forbidden\r\nContent-Length: 18\r\n\r\n403 Forbidden"
            client_socket.send(response.encode())
            client_socket.close()
            return

        if not url_filter.is_allowed(hostname):
            response = "HTTP/1.1 403 Forbidden\r\nContent-Length: 18\r\n\r\n403 Forbidden"
            client_socket.send(response.encode())
            client_socket.close()
            return

        # Connect to target server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((hostname, 80))
        server_socket.send(request.encode())

        # Receive response from server
        response = b""
        while True:
            chunk = server_socket.recv(4096)
            if not chunk:
                break
            response += chunk

        # Add Via header
        response = response.replace(b"\r\n", b"\r\nVia: 1.1 secure_gate_proxy\r\n", 1)

        # Send response back to client
        client_socket.send(response)
        server_socket.close()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_proxy():
    """Start the proxy server."""
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind((PROXY_HOST, PROXY_PORT))
    proxy_socket.listen(5)

    print(f"[*] Proxy server listening on {PROXY_HOST}:{PROXY_PORT}")

    while True:
        client_socket, addr = proxy_socket.accept()
        print(f"[*] Accepting connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    try:
        start_proxy()
    except KeyboardInterrupt:
        print("\n[*] Shutting down the proxy server")
