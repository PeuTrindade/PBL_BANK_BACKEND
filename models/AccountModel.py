from entities.Account import Account
from database.database import database

class AccountModel:
    @staticmethod
    def create(clientIds, accountType, agency, accountPass):
        newAccount = Account(clientIds, accountType, agency, accountPass)

        database['accounts'].append(newAccount.transformToDic())

    @staticmethod
    def accountExists(accountPass):
        accounts = database['accounts']
        acc = None

        for account in accounts:
            if account["accountPass"] == accountPass:
                acc = account
            
        if acc:
            return True
        
        return False
        
    @staticmethod
    def findByAccountPass(accountPass):
        for account in database['accounts']:
            if account["accountPass"] == accountPass:
                return account
            
        return None
    
    @staticmethod
    def transfer(account, value):
        account["balance"] -= value
        
    @staticmethod
    def receive(account, value):
        account["balance"] += value           
        
    @staticmethod
    def deposit(account, amount):
        account['balance'] += amount

    @staticmethod
    def withdraw(account, amount):
        account['balance'] -= amount
