class UsernameNotFound(Exception):
    def __init__(self, message="username not found, try again!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'UsernameNotFound: {self.message}'