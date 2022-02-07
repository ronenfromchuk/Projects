class InvalidCountry(Exception):
    def __init__(self, message="wrond country id, make sure u set the right ID!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'InvalidCountry: {self.message}'