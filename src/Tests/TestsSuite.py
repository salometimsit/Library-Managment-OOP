import unittest
from BooksFactoryTest import BooksFactoryTest
from BookTest import BookTest
from DeleteBooksTest import DeleteBooksTest
from Factory_of_ItemsTest import FactoryOfItemsTest
from FilesHandleTest import FilesHandleTest
from LibraryTest import LibraryTest
from LoggerTest import TestLogger
from RentalsTest import RentalsTest
from SearchStrategyTest import TestSearchStrategies
from UsersTest import UsersTest
from src.Tests.BookIteratorTest import TestBookIterator
from src.Tests.ObserverTest import ObserverTest
from src.Tests.Search_BooksTest import SearchBooksTest
from src.Tests.SubjectTest import SubjectTests



def create_test_suite():
    test_suite = unittest.TestSuite()
    test_classes = [TestBookIterator,BooksFactoryTest,BookTest,DeleteBooksTest,FactoryOfItemsTest,FilesHandleTest,
                    LibraryTest,TestLogger,ObserverTest,RentalsTest,SearchBooksTest,TestSearchStrategies,
                    SubjectTests,UsersTest]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = create_test_suite()
    runner.run(test_suite)