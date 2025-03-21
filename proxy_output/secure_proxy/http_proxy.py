import socketserver
import http.server
import socket

PROXY_HOST = "10.22.185.15"  # Replace with eth0/nic0 IP
PROXY_PORT = 8080

class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Handles GET requests and forwards them to the target server."""
        try:
            # Extract the requested URL
            url = self.path

            # Parse hostname and port
            if url.startswith("http://"):
                url = url[7:]
            host, path = url.split("/", 1) if "/" in url else (url, "")

            target_host, target_port = (host.split(":") + ["80"])[:2]  # Default HTTP port is 80
            target_port = int(target_port)

            print(f"[PROXY] Forwarding request to {target_host}:{target_port}")

            # Send request to the target server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
                proxy_socket.connect((target_host, target_port))
                request_line = f"GET /{path} HTTP/1.1\r\n"
                headers = f"Host: {target_host}\r\nConnection: close\r\n\r\n"
                proxy_socket.sendall(request_line.encode() + headers.encode())

                # Get response from the target server
                response_data = proxy_socket.recv(4096)

            # Modify the response headers to indicate the request passed through the proxy
            response_lines = response_data.split(b"\r\n")
            response_lines.insert(1, b"Via: 1.0 SecureGateProxy")

            # Send response back to the client
            self.send_response_only(200)
            self.end_headers()
            self.wfile.write(b"\r\n".join(response_lines))

        except Exception as e:
            self.send_error(500, str(e))

def run_proxy_server(host=PROXY_HOST, port=PROXY_PORT):
    """Starts the HTTP proxy server."""
    with socketserver.TCPServer((host, port), ProxyHTTPRequestHandler) as httpd:
        print(f"[PROXY] Running on {host}:{port}")
        try:
            while True:
                httpd.handle_request()
                print(f"[PROXY] Accepting connection from {host}")
        except KeyboardInterrupt:
            print("\n[PROXY] Shutting down the proxy server")

if __name__ == "__main__":
    run_proxy_server()
