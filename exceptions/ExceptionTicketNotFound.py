class TicketNotFound(Exception):
    def __init__(self, message="ticket not found, try again!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'TicketNotFound: {self.message}'