import socket


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Extended server started, waiting for clients...")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Client {address} connected.")
        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    client_socket.send("Please enter a valid message.\n".encode('utf-8'))
                    continue

                if data.lower().strip() == 'exit':
                    print(f"Client {address} disconnected.")
                    break

                if data.lower().strip() == 'shutdown':
                    print("Shutting down server.")
                    client_socket.send("Server is shutting down.\n".encode('utf-8'))
                    server_socket.close()
                    return

                client_socket.send(f"Echo: {data}\n".encode('utf-8'))

            except (ConnectionResetError, BrokenPipeError):
                print(f"Client {address} disconnected unexpectedly.")
                break

        client_socket.close()


if __name__ == "__main__":
    run_server()
