class AdminNotFound(Exception):
    def __init__(self, message="Admin not found!, please check again!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'AdminNotFound: {self.message}'