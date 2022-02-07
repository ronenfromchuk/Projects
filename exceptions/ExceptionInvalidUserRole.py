class InvalidUserRole(Exception):
    def __init__(self, message="wrong user role, must be between 1 to 3!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'InvalidUserRole: {self.message}'