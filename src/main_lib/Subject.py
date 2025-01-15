class Subject:
    """
    This class is implementation of subject class for observer
    for the subscriber list will be added only the login users
    """
    def __init__(self):
        self._sub = []

    def subscribe(self, user):
        if user not in self._sub:
            self._sub.append(user)

    def unsubscribe(self, user):
        if user in self._sub:
            self._sub.remove(user)

    def notify(self, message):
        """
        Needed to be implemented in child class
        :param message: the message to send to the user
        """
        pass