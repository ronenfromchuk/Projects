class User:

    def __init__(self, id_, public_id, username, password):
        self.id_ = id_
        self.public_id = public_id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'user id={self.id_}, public id="{self.public_id}, "username="{self.username}", "password="{self.password})'

    def __str__(self):
        return f'user id={self.id_}, public id="{self.public_id}, "username="{self.username}", "password="{self.password})'
