
# Library Management System

This project is a library management system implemented in Python, utilizing various design patterns and a graphical user interface (GUI) for user interaction. The system allows librarians to manage books, track rentals, and handle waiting lists efficiently.

## Features

- User authentication: Librarians can log in and register to access the system.
- Book management: Librarians can add new books, remove books, and update book information.
- Book search: Users can search for books based on title, author, year, or genre.
- Book rental: Users can rent available books and return borrowed books.
- Waiting list: If a book is not available, users can join a waiting list to be notified when the book becomes available.
- Book popularity tracking: The system keeps track of the popularity of each book based on rental history.
- Logging: Important actions and events are logged for monitoring and debugging purposes.

## Design Patterns

The following design patterns have been implemented in this project:

1. **Strategy Pattern**: Used for implementing different search strategies (title, author, year, genre) in the `SearchBooks` class.

2. **Decorator Pattern**: Utilized in the `Logger` class to log method calls and add messages to the log file.

3. **Factory Pattern**: Implemented in the `BooksFactory` class to create new books or update existing book information.

4. **Iterator Pattern**: Used in the `BookIterator` class to navigate through the book collections during search operations.

5. **Observer Pattern**: Applied in the `Subject` and `Observer` classes to notify librarians when a book with a waiting list is returned and to inform them about the next person in line to receive the book.

6. **Singleton Pattern**: The `Library` class is implemented as a singleton, ensuring that only one instance of the library exists throughout the system.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages: pandas, tkinter

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/library-management-system.git
   ```

2. Install the required packages:

   ```bash
   pip install pandas tkinter
   ```

### Usage

1. Navigate to the project directory:

   ```bash
   cd library-management-system
   ```

2. Run the main script:

   ```bash
   python OUR_GUI.py
   ```

3. The library management system GUI will open.

4. Use the provided login credentials or register a new librarian account to access the system.

5. Explore the various features of the system, such as adding books, searching for books, renting books, and managing waiting lists.

6. Log out when finished using the system.

## GUI Walkthrough

1. **Login Screen**:
   - Enter your username and password to log in.
   - If you don't have an account, click the "Register" button to create a new librarian account.

2. **Main Screen**:
   - The main screen provides access to different functionalities of the library management system.
   - Click on the respective buttons to add a book, remove a book, search for a book, view books, or view popular books.
   - Use the "Logout" button to log out of the system.

3. **Search Screen**:
   - Select the search strategy (title, author, year, or genre) using the radio buttons.
   - Enter the search term in the provided entry field.
   - Click the "Search" button to retrieve matching books.
   - The search results will be displayed in a table format.
   - To rent a book, select a book from the table and click the "Lend Book" button.
   - To return a book, select a book from the table and click the "Return Book" button.

4. **Add Book Screen**:
   - Enter the details of the book you want to add, including title, author, number of copies, category, and year.
   - Click the "Add Book" button to add the book to the library.

5. **Remove Book Screen**:
   - Enter the details of the book you want to remove, including title, author, category, and year.
   - Click the "Remove Book" button to remove the book from the library.

6. **Display Books Screen**:
   - Select a category from the dropdown menu to filter the books (All Books, Available Books, Not Available Books, Popular Books, or a specific genre).
   - Click the "Display Books" button to view the books in the selected category.

7. **Popular Books Screen**:
   - This screen displays the top 10 most popular books based on rental history.

8. **Waiting List Entry**:
   - If a book is not available and you want to join the waiting list, you will be prompted with a confirmation dialog.
   - Click "Yes" to proceed to the waiting list form.
   - Enter your name and phone number in the provided fields.
   - Click the "Add to Waiting List" button to join the waiting list for the book.

## File Structure

The project directory contains the following files and folders:

- `OUR_GUI.py`: The main script that runs the library management system GUI.
- `src/main_lib/`: Contains the source code files for the library management system.
  - `Excel_Tables/`: Contains CSV files for storing book, user, and log data.
    - `books.csv`: Stores information about all books in the library.
    - `available_books.csv`: Stores information about currently available books.
    - `not_available_books.csv`: Stores information about currently borrowed books and waiting lists.
    - `users.csv`: Stores user (librarian) information.
    - `logger.log`: Stores log messages for monitoring and debugging purposes.
  - `Library.py`: Defines the `Library` class, which is the central component of the system.
  - `Books.py`: Defines the `Books` class, representing a book in the library.
  - `BooksCategory.py`: Defines the `BooksCategory` enum for book genres.
  - `BooksFactory.py`: Implements the factory pattern for creating and updating books.
  - `BookIterator.py`: Implements the iterator pattern for navigating book collections.
  - `Delete_Books.py`: Provides functionality for deleting books from the library.
  - `LibraryServiceLocator.py`: Implements a service locator for accessing library and rental services.
  - `Logger.py`: Implements the decorator pattern for logging method calls and messages.
  - `Observer.py`: Defines the `Observer` interface for the observer pattern.
  - `Rentals.py`: Manages the rental system for the library.
  - `Search_Books.py`: Implements the search functionality for books.
  - `SearchStrategy.py`: Defines different search strategies using the strategy pattern.
  - `Subject.py`: Defines the `Subject` class for the observer pattern.
  - `Users.py`: Defines the `User` class, representing users (librarians) of the system.

## Contributing

Contributions to the library management system are welcome! If you find any bugs, have suggestions for improvements, or want to add new features, please submit an issue or a pull request on the project's GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Created by:
<b>Itay Segev <br>
Salome Timsit<b/>