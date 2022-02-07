class InvalidToken(Exception):
    def __init__(self, message="Issues with the login token, ask for help!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'InvalidToken: {self.message}'