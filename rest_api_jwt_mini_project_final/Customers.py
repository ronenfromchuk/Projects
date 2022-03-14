class Customer:

    def __init__(self, id_, name, location):
        self.id_ = id_
        self.name = name
        self.location = location

    def __repr__(self):
        return f'customer id={self.id_}, name="{self.name}", location="{self.location}")'

    def __str__(self):
        return f'customer id_={self.id_}, name="{self.name}", location="{self.location}"]'