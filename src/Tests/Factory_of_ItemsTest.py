
from src.Tests.TestFileManager import LibraryTestCase
from src.main_lib.Books import Books
from src.main_lib.Factory_of_Items import Factory_of_Items


class FactoryOfItemsTest(LibraryTestCase):
    def setUp(self):
        super().setUp()
        self.__files = [
            f"{self.test_dir}/BookTest.csv",
            f"{self.test_dir}/Available_BookTest.csv",
            f"{self.test_dir}/NotAvailable_BookTest.csv"
        ]

    def test_create_book(self):
        result1=(Factory_of_Items.factory_of_items
              ("book","Test Book","Test Book",3,"Fiction",2024,self.__files))
        result2 = (Factory_of_Items.factory_of_items
                   ("book", "Test Book", "Test Book", 3, "Fiction", 2024, self.__files))
        self.assertTrue(result1)
        self.assertFalse(result2)

    def test_sensitive_to_uppercase(self):
        result1 = (Factory_of_Items.factory_of_items
                   ("BOOK", "Test BOOk", "Test BOok", 3, "FiCTion", 2024, self.__files))
        result2 = (Factory_of_Items.factory_of_items
                   ("book", "Test Book", "Test Book", 3, "Fiction", 2024, self.__files))
        self.assertTrue(result1)
        self.assertFalse(result2)

    def test_create_not_book(self):
        result1 = (Factory_of_Items.factory_of_items
                   ("disc", "Test BOOk", "Test BOok", 3, "FiCTion", 2024, self.__files))
        self.assertIsNone(result1)


    def test_not_exist_files(self):
        files = [f"{self.test_dir}/NonExistentBook.csv",f"{self.test_dir}/Invalid.csv",f"{self.test_dir}/NotFound.csv"]
        with self.assertRaises(FileNotFoundError):
            result = Factory_of_Items.factory_of_items(
                "book", "Test Book", "Test Author", 3, "Fiction", 2024,files)

    def test_empty_parameters(self):
        result1 = Factory_of_Items.factory_of_items(
            "book", "", "Test Author", 3, "Fiction", 2024, self.__files)
        result2 = Factory_of_Items.factory_of_items(
            "book", "Test Book", "", 3, "Fiction", 2024, self.__files)
        self.assertIsNone(result1)
        self.assertIsNone(result2)

    def test_space_sensitive(self):
            result1 = Factory_of_Items.factory_of_items(
                "book", "  Test Book  ", "  Test Author  ", 3, "Fiction", 2024, self.__files)
            result2 = Factory_of_Items.factory_of_items(
                "book", "Test Book", "Test Author", 3, "Fiction", 2024, self.__files)
            self.assertTrue(result1)
            self.assertFalse(result2)

    def test_negative_copies(self):
        result = Factory_of_Items.factory_of_items(
            "book", "Test Book", "Test Author", -1, "Fiction", 2024, self.__files)
        self.assertIsNone(result)

    def test_future_year(self):
        future_year = 2500
        result = Factory_of_Items.factory_of_items(
            "book", "Test Book", "Test Author", 3, "Fiction", future_year, self.__files)
        self.assertIsNone(result)


