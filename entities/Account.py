import random

class Account:
    def __init__(self, clientIds, accountType, agency, accountPass):
        self.id = random.randint(10000, 99999)
        self.clientIds = clientIds
        self.accountType = accountType
        self.balance = 0.0
        self.accountTransactions = []
        self.agency = agency
        self.accountPass = accountPass

    def transformToDic(self):
        dic = {
            "id": self.id,
            "clientIds": self.clientIds,
            "accountType": self.accountType,
            "balance": self.balance,
            "accountTransactions": self.accountTransactions,
            "agency": self.agency,
            "accountPass": self.accountPass
        }
        
        return dic