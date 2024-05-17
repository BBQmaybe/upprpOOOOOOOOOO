import unittest
from unittest.mock import patch

import socket
import pickle
import io
import sys
from client import register_user, send_message, generate_hamming_code
from server import handle_client,  check_hamming_code


class ClientSocketStub:
    def recv(self, size):
        return pickle.dumps({"action": "register", "name": "test_user"})
    def send(self, data):
        pass

class TestChatFunctions(unittest.TestCase):
    def test_generate_hamming_code(self):
        # Проверяем корректность генерации кода Хэмминга
        data = "Hello"
        hamming_code = generate_hamming_code(data)
        self.assertEqual(hamming_code, '1000100110000111001010110110001110110001101111')

    def test_check_hamming_code_no_error(self):
        # Проверяем функцию проверки кода Хэмминга без ошибок
        code_without_error = '011110011011011011011111'
        corrected_code = check_hamming_code(code_without_error)
        self.assertEqual(corrected_code, code_without_error)

    def test_check_hamming_code_with_error(self):
        # Проверяем функцию проверки кода Хэмминга с одной ошибкой
        code_with_error = '011110011011011011011111'
        corrected_code = check_hamming_code(code_with_error)
        self.assertNotEqual(corrected_code, '011110011011011011011110')


if __name__ == '__main__':
    unittest.main()
