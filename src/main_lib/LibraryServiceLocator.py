class LibraryServiceLocator:
    _rentals_instance = None
    _library_instance = None

    @staticmethod
    def get_rentals():
        return LibraryServiceLocator._rentals_instance

    @staticmethod
    def set_rentals(rentals):
        LibraryServiceLocator._rentals_instance = rentals

    @staticmethod
    def get_library():
        return LibraryServiceLocator._library_instance

    @staticmethod
    def set_library(library):
        LibraryServiceLocator._library_instance = library