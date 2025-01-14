class Subject:
    def __init__(self):
        self.sub = []

    def subscribe(self, user):
        if user not in self.sub:
            self.sub.append(user)

    def unsubscribe(self, user):
        if user in self.sub:
            self.sub.remove(user)

    def notify(self, message):
        pass