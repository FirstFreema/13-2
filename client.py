import socket


def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 12345))
    except ConnectionRefusedError:
        print("Unable to connect to the server. Server might be down.")
        return

    while True:
        message = input("Enter message (type 'exit' to disconnect or 'shutdown' to stop server): ")
        if not message:
            print("Please enter a valid message.")
            continue

        try:
            client_socket.send(message.encode('utf-8'))

            if message.lower() == 'exit':
                print("Disconnecting from server...")
                break

            if message.lower() == 'shutdown':
                print("Requesting server shutdown...")
                response = client_socket.recv(1024).decode('utf-8')
                if not response:
                    print("Server has been shut down. Exiting client.")
                    break
                print("Server response:", response)
                continue

            response = client_socket.recv(1024).decode('utf-8')
            if not response:
                print("Server has disconnected. Exiting.")
                break
            print("Server response:", response)

        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            print("Server has disconnected. Exiting.")
            break

    client_socket.close()
    print("Process finished with exit code 0")


if __name__ == "__main__":
    run_client()
