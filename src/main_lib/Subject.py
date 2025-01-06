class Subject:
    """
    Represents a subject in the Observer design pattern.
    Subjects manage a list of observers and notify them of changes.

    Attributes:
        sub (list): A list of observers subscribed to the subject.
    """

    def __init__(self):
        """
        Initializes a Subject instance.
        """
        self.sub = []

    def sub(self, user):
        """
        Subscribes an observer to the subject.

        Args:
            user (Observer): The observer to subscribe.
        """
        if user not in self.sub:
            self.sub.append(user)

    def unsubscribe(self, user):
        """
        Unsubscribes an observer from the subject.

        Args:
            user (Observer): The observer to unsubscribe.
        """
        if user in self.sub:
            self.sub.remove(user)

    def notify(self, message):
        """
        Notifies all subscribed observers with a message.

        Args:
            message (str): The message to send to all observers.
        """
        for subscriber in self.sub:
            subscriber.update(message)
