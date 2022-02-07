class WrongPassword(Exception):
    def __init__(self, message="wrong password!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'WrongPassword: {self.message}'