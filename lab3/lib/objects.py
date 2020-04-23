class Bank(object):
    def __init__(self, name, bik, accountNumber):
        self.name = name
        self.bik = bik
        self.accountNumber = accountNumber

class Provider(object):
    def __init__(self, name, inn, kpp, accountNumber):
        self.name = name
        self.inn = inn
        self.kpp = kpp
        self.accountNumber = accountNumber
    
    def setInfo(self, address, phoneNumber):
        self.info = '%s, ИНН %s, КПП %s, %s, тел.: %s' % (self.name, self.inn, self.kpp, address, phoneNumber)

class Document(object):
    def __init__(self, number, date, contract):
        self.number = number
        self.date = date
        self.contract = contract

class Client(object):
    def __init__(self, name, inn, kpp, address, phoneNumber):
        self.info = '%s, ИНН %s, КПП %s, %s, тел.: %s' % (name, inn, kpp, address, phoneNumber)

class Item(object):
    def __init__(self, index, name, amount, unit, price, total):
        self.index = index
        self.name = name
        self.amount = "%.2f" % amount if amount != None else ''
        self.unit = unit if amount != None else ''
        self.price = "%.2f" % price
        self.total = "%.2f" % total

class Bill(object):
    def __init__(self, countService, total, tax):
        self.countService = countService
        self.total = total
        self.tax = "%d%%" % tax
        self.payment = "%.2f" % (total*(100+tax)/100)