import os


class FilesHandle:
    """
    This class handles all the file operations
    In their methods we can get different types of files for any classes.
    """
    @staticmethod
    def get_all_files():
        """
        This method gets all the files in the current working directory
        """
        try:
            filenames = ['Excel_Tables/books.csv', 'Excel_Tables/available_books.csv',
                         'Excel_Tables/not_available_books.csv','Excel_Tables/users.csv','Excel_Tables/logger.log']
            __files = []
            for filename in filenames:
                file_path = os.path.join(os.path.dirname(__file__), filename)
                file_path = os.path.abspath(file_path)

                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"File not found: {file_path}")

                __files.append(file_path)

            return __files
        except FileNotFoundError:
            raise FileNotFoundError("File not found")

    @staticmethod
    def get_file_by_category(types:str):
        """
        This method gets all the files in the current working directory
        :return: the files of the given type
        """
        try:
            files = []
            for file in FilesHandle.get_all_files():
                if types.lower() in file.lower():
                    files.append(file)
            if len(files) == 1:
                return files[0]
            if len(files) == 0:
                raise FileNotFoundError("File not found")
            return files
        except FileNotFoundError:
            raise FileNotFoundError("File not found")


    @staticmethod
    def get_logger_file():
        """
        This method gets all the files in the current working directory
        :return: the file of the logger file
        """
        file_path = os.path.join(os.path.dirname(__file__), 'Excel_Tables/logger.log')
        file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        return file_path




