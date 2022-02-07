class UserAlreadyExists(Exception):
    def __init__(self, message="user already exist, try something else!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'UserAlreadyExists: {self.message}'