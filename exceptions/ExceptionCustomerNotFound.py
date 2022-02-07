class CustomerNotFound(Exception):
    def __init__(self, message="customer doesn't exist, please try again!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'CustomerNotFound: {self.message}'