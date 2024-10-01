import unittest
import socket
import threading
import time
from extended_server import run_server as run_extended_server

class TestEchoServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Запускаем сервер в отдельном потоке
        cls.server_thread = threading.Thread(target=run_extended_server, daemon=True)
        cls.server_thread.start()
        time.sleep(1)  # Даем серверу время для запуска

    def test_echo_message(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        client_socket.send("Hello".encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        self.assertEqual(response, "Echo: Hello\n")
        client_socket.send("exit".encode('utf-8'))
        client_socket.close()

    def test_shutdown_server(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        client_socket.send("shutdown".encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        self.assertIn("Server is shutting down", response)
        client_socket.close()

if __name__ == "__main__":
    unittest.main()
