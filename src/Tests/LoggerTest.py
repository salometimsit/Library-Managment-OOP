import unittest
import logging
import os
import tempfile

from src.main_lib.Logger import Logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        """
        creating new logger who will write to a temporary file instead of the main one
        """
        self.test_log_fd, self.test_log_path = tempfile.mkstemp()
        self.original_handlers = logging.getLogger().handlers.copy()
        logging.getLogger().handlers.clear()
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=self.test_log_path,
            filemode='a'
        )

    def tearDown(self):
        os.close(self.test_log_fd)
        os.unlink(self.test_log_path)

        logging.getLogger().handlers.clear()
        for handler in self.original_handlers:
            logging.getLogger().addHandler(handler)

    def read(self):
        with open(self.test_log_path, 'r') as f:
            return f.read()

    def test_log_method_call_success(self):

        @Logger.log_method_call("Test")
        def test_success(self):
            return True

        test_success(self)
        log_content = self.read()
        self.assertIn("Test successfully", log_content)

    def test_log_method_call_failure(self):
        @Logger.log_method_call("Test")
        def test_failure(self):
            return False

        test_failure(self)
        log_content = self.read()
        self.assertIn("Test fail", log_content)

    def test_log_method_call_exception(self):

        @Logger.log_method_call("Test")
        def test_exception(self):
            raise ValueError("")

        with self.assertRaises(ValueError):
            test_exception(self)
        log_content = self.read()
        self.assertIn("Test fail", log_content)

    def test_log_add_message(self):
        test_message = "Test message"
        Logger.log_add_message(test_message)
        log_content = self.read()
        self.assertIn(test_message, log_content)

    def test_log_format(self):
        test_message = "Test format"
        Logger.log_add_message(test_message)
        log_content = self.read()
        self.assertRegex(log_content, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
        self.assertIn(test_message, log_content)

    def test_multiple_logs(self):
        @Logger.log_method_call("Test failure")
        def test_failure(self):
            return False

        @Logger.log_method_call("Test success")
        def test_success(self):
            return True

        @Logger.log_method_call("Test exception")
        def test_exception(self):
            raise ValueError("")

        test_failure(self)
        test_success(self)
        with self.assertRaises(ValueError):
            test_exception(self)
        messages=["Test failure fail", "Test success successfully","Test exception fail"]
        log_content = self.read()
        for msg in messages:
            self.assertIn(msg, log_content)


if __name__ == '__main__':
    unittest.main()