


class User():
    

    def __init__(self, id, role, name, phone, balance, comment):
        self.id = id
        self.role = role
        self.name = name
        self.phone = phone
        self.balance = balance
        self.comment = comment

    def get_list(self):
        return [self.id, self.role, self.name, self.phone, self.balance, self.comment]