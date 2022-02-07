class InvalidTime(Exception):
    def __init__(self, message="departure must be before landing time, try again!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'InvalidTime: {self.message}'