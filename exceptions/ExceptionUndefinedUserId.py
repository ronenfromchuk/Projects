class UndefinedUserID(Exception):
    def __init__(self, message="this user's role undefined, please check again!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'UndefinedUserID: {self.message}'