class Customer:
    def __init__(self, id, fname, lname, address, mobile):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.address = address
        self.mobile = mobile

    def __repr__(self):
        return f'id= {self.id}, fname= {self.fname}, lname= {self.lname}' +\
        f'address= {self.address}, mobile number= {self.mobile}'

    def __str__(self):
        return f'id= {self.id}, fname= {self.fname}, lname= {self.lname}' + \
               f'address= {self.address}, mobile number= {self.mobile}'