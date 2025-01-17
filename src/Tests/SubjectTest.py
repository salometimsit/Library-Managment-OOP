from unittest.mock import MagicMock
from src.Tests.TestFileManager import LibraryTestCase
from src.main_lib.Subject import Subject


class SubjectTests(LibraryTestCase):
    def setUp(self):
        super().setUp()
        self.subject = Subject()
        self.observer1 = MagicMock()
        self.observer2 = MagicMock()

    def test_subscriber_management(self):
        self.subject.subscribe(self.observer1)
        self.assertIn(self.observer1, self.subject._sub)
        self.subject.subscribe(self.observer1)
        self.assertEqual(self.subject._sub.count(self.observer1), 1)
        self.subject.unsubscribe(self.observer1)
        self.assertNotIn(self.observer1, self.subject._sub)
