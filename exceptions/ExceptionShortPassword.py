class WrongPassword(Exception):
    def __init__(self, message="password must have at least 6 chars!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'WrongPassword: {self.message}'