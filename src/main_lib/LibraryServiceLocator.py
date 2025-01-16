class LibraryServiceLocator:
    """
    A service locator class for managing instances of library-related services.

    This class uses a singleton-like pattern to provide access to global instances
    of library and rental services.

    Attributes:
        _rentals_instance: A static variable to store the instance of the rentals service.
        _library_instance: A static variable to store the instance of the library service.
    """
    _rentals_instance = None
    _library_instance = None

    @staticmethod
    def get_rentals():
        """
        Retrieves the current instance of the rentals service.

        Returns:
            The rentals service instance, or None if it has not been set.
        """
        return LibraryServiceLocator._rentals_instance

    @staticmethod
    def set_rentals(rentals):
        """
        Sets the instance of the rentals service.

        Args:
            rentals: The instance of the rentals service to be set.
        """
        LibraryServiceLocator._rentals_instance = rentals

    @staticmethod
    def get_library():
        """
       Retrieves the current instance of the library service.

       Returns:
           The library service instance, or None if it has not been set.
       """
        return LibraryServiceLocator._library_instance

    @staticmethod
    def set_library(library):
        """
        Sets the instance of the library service.

        Args:
            library: The instance of the library service to be set.
        """
        LibraryServiceLocator._library_instance = library