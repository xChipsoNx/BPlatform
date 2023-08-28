


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
    

class Wallet():
    def __init__(self, id, type, bank, holder_name, tariff, balance, bank_id, user_id,share):
        self.id = id
        self.type = type
        self.bank = bank
        self.holder_name = holder_name
        self.tariff = tariff
        self.balance = balance
        self.bank_id = bank_id
        self.user_id = user_id
        self.share = share

    def get_list(self):
        return [self.id, self.type, self.bank ,self.holder_name, self.tariff, self.balance, self.bank_id, self.user_id]
    

class PP():
    def __init__(self, id, date, number, client_name, bank_name,holder_name,sum, tariff, add_tariff, tax, total, close_sum, close_date,client_id, holder_id, bank_id, wallet_id, status ):
        self.id = id
        self.date = date
        self.number = int(number)
        self.client_name = client_name
        self.holder_name = holder_name
        self.bank_name = bank_name
        self.sum = sum
        self.tariff = tariff
        self.add_tariff = add_tariff
        self.tax = tax
        self.total = total
        self.close_sum = close_sum
        self.close_date = close_date
        self.client_id = client_id
        self.holder_id = int(holder_id)
        self.bank_id = int(bank_id)
        self.wallet_id = wallet_id
        self.status = status

    def get_list(self):
        return [self.id, self.date, self.number, self.client_name, self.bank_name, self.holder_name,self.sum, self.tariff, self.add_tariff, self.tax, self.total, self.close_sum, self.close_date,self.client_id, self.holder_id, self.bank_id, self.wallet_id, self.status]
    

class Cash():
    def __init__(self, id, type, holder_name, bank_name,  sum, wallet_id, bank_id, status):
        self.id = id
        self.type = type
        self.bank_name = bank_name
        self.holder_name = holder_name
        self.sum = sum
        self.bank_id = bank_id
        self.wallet_id = wallet_id
        self.status = status

    def get_list(self):
        return [self.id, self.type, self.bank_name ,self.holder_name, self.sum, self.wallet_id, self.bank_id, self.status]
