import unittest
from unittest.mock import MagicMock, patch
import client

class TestClient(unittest.TestCase):
    def setUp(self):
        self.control_socket = MagicMock()
        client.socket.socket = MagicMock(return_value=self.control_socket)
        client.send_message = MagicMock()
        client.receive_message = MagicMock()
        client.send_data_from_file = MagicMock()

    def test_get_file(self):
        client.receive_message.return_value = 'FILE testfile.txt 1024'
        client.get_file(self.control_socket, 'testfile.txt')
        client.send_message.assert_any_call(self.control_socket, 'GET testfile.txt')
        client.send_message.assert_any_call(self.control_socket, 'START')
        self.control_socket.recv.assert_called()

    def test_get_file(self):
        client.receive_message.return_value = 'FILE testfile.txt 1024'
        # Simulate the end of file with empty bytes
        self.control_socket.recv = MagicMock(return_value=b'')
        client.get_file(self.control_socket, 'testfile.txt')
        client.send_message.assert_any_call(self.control_socket, 'GET testfile.txt')
        client.send_message.assert_any_call(self.control_socket, 'START')
        self.control_socket.recv.assert_called()


    def test_put_file_file_not_found(self):
        with patch('os.path.isfile', return_value=False):
            client.put_file(self.control_socket, 'nofile.txt')
            print_output = "Error: nofile.txt not found"
            client.send_message.assert_not_called()

    def test_list_files(self):
        client.receive_message.return_value = 'file1.txt file2.txt'
        client.list_files(self.control_socket)
        client.send_message.assert_called_with(self.control_socket, 'LS')
        client.receive_message.assert_called_once()
        self.assertEqual(client.receive_message(), 'file1.txt file2.txt')

if __name__ == '__main__':
    unittest.main()
