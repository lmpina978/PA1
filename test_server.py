import unittest
from unittest.mock import MagicMock
import server

class TestServer(unittest.TestCase):
    def setUp(self):
        self.control_socket = MagicMock()
        server.send_message = MagicMock()
        server.receive_message = MagicMock()
        server.send_file = MagicMock()
        server.receive_file = MagicMock()
        server.list_files = MagicMock()

    def test_process_command_quit(self):
        server.process_command(self.control_socket, 'quit')
        server.send_message.assert_called_once_with(self.control_socket, 'Goodbye.')

    def test_process_command_get(self):
        server.receive_message.return_value = 'START'
        server.process_command(self.control_socket, 'get testfile.txt')
        server.send_file.assert_called_once_with(self.control_socket, 'testfile.txt')

    def test_process_command_put(self):
        server.process_command(self.control_socket, 'put testfile.txt')
        server.receive_file.assert_called_once_with(self.control_socket, 'testfile.txt')

    def test_process_command_ls(self):
        server.process_command(self.control_socket, 'ls')
        server.list_files.assert_called_once_with(self.control_socket)

    def test_process_command_invalid(self):
        server.process_command(self.control_socket, 'invalid')
        server.send_message.assert_called_once_with(self.control_socket, 'Invalid command invalid')

if __name__ == '__main__':
    unittest.main()
