class NoMoreTicketsLeft(Exception):
    def __init__(self, message="remaining tickets can't be < 0!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'NoMoreTicketsLeft: {self.message}'