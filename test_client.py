import unittest
from unittest.mock import MagicMock, patch, call
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
        self.control_socket.recv = MagicMock(return_value=b'')
        with patch('builtins.print') as mocked_print:
            client.get_file(self.control_socket, 'testfile.txt')
            client.send_message.assert_any_call(self.control_socket, 'GET testfile.txt')
            client.send_message.assert_any_call(self.control_socket, 'START')
            self.control_socket.recv.assert_called()
            # Check all expected print calls
            mocked_print.assert_has_calls([
                call('Receiving testfile.txt (1024 bytes)...'),
                call('testfile.txt received successfully')
            ])

    def test_put_file_file_not_found(self):
        with patch('os.path.isfile', return_value=False), patch('builtins.print') as mocked_print:
            client.put_file(self.control_socket, 'nofile.txt')
            client.send_message.assert_not_called()
            mocked_print.assert_called_once_with('Error: File nofile.txt not found')

    def test_list_files(self):
        client.receive_message.return_value = 'file1.txt file2.txt'
        with patch('builtins.print') as mocked_print:
            client.list_files(self.control_socket)
            client.send_message.assert_called_with(self.control_socket, 'LS')
            client.receive_message.assert_called_once()
            mocked_print.assert_called_once_with('file1.txt file2.txt')

if __name__ == '__main__':
    unittest.main()