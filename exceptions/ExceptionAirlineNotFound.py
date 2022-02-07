class AirlineNotFound(Exception):
    def __init__(self, message="airline not found, please try again!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'AirlineNotFound: {self.message}'