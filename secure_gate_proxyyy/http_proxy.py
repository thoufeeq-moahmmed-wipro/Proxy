import socket
import threading
import netifaces
from categorization import is_url_allowed, is_url_blocked

BUFFER_SIZE = 8192
PORT = 8080

def get_available_interfaces():
    """Get a list of available network interfaces."""
    return netifaces.interfaces()

def get_interface_ip(interface):
    """Get the IP address of the selected network interface."""
    try:
        return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    except (KeyError, ValueError):
        return None  # Return None if interface has no IPv4 address

def handle_client(client_socket):
    """Handle client requests, check URL filtering, and forward allowed traffic."""
    try:
        request = client_socket.recv(BUFFER_SIZE).decode()

        if not request:
            return
        
        # Extract first line of the request
        first_line = request.split("\n")[0]
        parts = first_line.split()
        
        if len(parts) < 2:
            print("[ERROR] Invalid HTTP request format")
            client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\nInvalid Request")
            return
        
        method, url = parts[0], parts[1]

        print(f"[*] Received request: {method} {url}")

        # URL Filtering
        if is_url_blocked(url):
            print(f"[BLOCKED] {url} (Returning 403 Forbidden)")
            response = "HTTP/1.1 403 Forbidden\r\n\r\nAccess Denied!"
            client_socket.sendall(response.encode())
            return

        if not is_url_allowed(url):
            print(f"[DENIED] {url} (Not in allowed list, Returning 403 Forbidden)")
            response = "HTTP/1.1 403 Forbidden\r\n\r\nURL Not Allowed!"
            client_socket.sendall(response.encode())
            return

        print(f"[*] Forwarding request to {url}")

        # Extract hostname from URL
        http_pos = url.find("://")  
        temp = url[(http_pos+3):] if http_pos != -1 else url  
        server_pos = temp.find("/")  
        host = temp[:server_pos] if server_pos != -1 else temp
        port = 80

        # Connect to the destination server
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[*] Connecting to {host}:{port}...")
        remote_socket.connect((host, port))
        remote_socket.sendall(request.encode())

        # Forward the response back to the client
        while True:
            response = remote_socket.recv(BUFFER_SIZE)
            if len(response) > 0:
                client_socket.sendall(response)
            else:
                break

    except Exception as e:
        print(f"[ERROR] {e}")
    
    finally:
        client_socket.close()

def start_proxy():
    """Start the proxy server."""
    interfaces = get_available_interfaces()
    print("Available interfaces:", interfaces)

    selected_interface = input("Enter the network interface to bind (e.g., enp3s0): ").strip()
    bind_ip = get_interface_ip(selected_interface)

    if not bind_ip:
        print(f"[ERROR] Could not determine IP for {selected_interface}. Exiting.")
        return

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((bind_ip, PORT))
    server_socket.listen(5)

    print(f"[*] Proxy server listening on {bind_ip}:{PORT}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.daemon = True  # Ensures the thread exits when the program stops
            client_handler.start()

    except KeyboardInterrupt:
        print("\n[*] Shutting down the proxy server gracefully...")

    finally:
        server_socket.close()
        print("[*] Proxy server stopped.")

if __name__ == "__main__":
    start_proxy()

