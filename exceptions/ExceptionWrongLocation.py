class InvalidLocation(Exception):
    def __init__(self, message="destination country must be different than the origin one!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'InvalidLocation: {self.message}'