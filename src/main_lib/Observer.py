from abc import abstractmethod


class Observer:
    def __init__(self):
        pass

    """
    This method gets the subject that the message is received from, and the message they needed to notify us
    """

    @abstractmethod
    def update(self, subject, message):
        pass
