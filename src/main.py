from src.main_lib.Notifications import Notifications
from main_lib.Users import User
from main_lib.Books import Books
def main():
    ##title,author,is_loaned,copies,genre,year
    books= Books("THE","arthur",2,3,"comedy",2012)
    Books.add_to_library(books)
    print(books)
   # Create a notification manager
    notification_manager = Notifications()
    #
    # # Create users
    # user1 = User("alice", "password123", "member")
    # user2 = User("bob", "securepass456", "librarian")
    #
    # # Display user details
    # print("Created Users:")
    # print(user1)
    # print(user2)
    #
    # # Register users
    # print("\nRegistering Users:")
    # user1.register()
    # user2.register()

    # # Subscribe users to notifications
    # print("\nSubscribing Users to Notifications:")
    # notification_manager.sub(user1)
    # notification_manager.sub(user2)
    #
    # # Notify all users
    # print("\nSending Notification to All Subscribers:")
    # notification_manager.notify("The book '1984' is now available.")
    #
    # # Unsubscribe a user
    # print("\nUnsubscribing a User:")
    # notification_manager.unsubscribe(user1)
    #
    # # Notify remaining users
    # print("\nSending Notification to Remaining Subscribers:")
    # notification_manager.notify("The book 'Brave New World' is now available.")

if __name__ == "__main__":
    main()
