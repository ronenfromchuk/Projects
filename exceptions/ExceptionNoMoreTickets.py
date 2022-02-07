class NoMoreTicketsLeft(Exception):
    def __init__(self, message="no more available tickets!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'NoMoreTicketsLeft: {self.message}'