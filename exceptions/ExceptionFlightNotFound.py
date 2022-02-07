class FlightNotFound(Exception):
    def __init__(self, message="flight not exist, please try again!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'FlightNotFound: {self.message}'