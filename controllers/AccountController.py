from models.AccountModel import AccountModel
from models.ClientModel import ClientModel
from database.database import database
import socket

class AccountController:
    @staticmethod
    def verifyClientIds(clientIds):
        for id in clientIds:
            if ClientModel.clientExistsById(id) == False:
                return False
            
        return True

    @staticmethod
    def create(clientIds, accountType, agency, accountPass):
        if (clientIds == None or clientIds == [] or accountType == None or agency == None or accountPass == None):
            return { "message": "Campos em branco foram enviados", "ok": False }
        
        elif AccountModel.accountExists(accountPass) == True:
            return { "message": "Conta já cadastrada com este código!", "ok": False }
        
        elif AccountController.verifyClientIds(clientIds) == False:
            return { "message": "Clientes inexistentes!", "ok": False }

        AccountModel.create(clientIds, accountType, agency, accountPass)
        
        return { "message": "Conta cadastrada com sucesso!", "ok": True }
    
    @staticmethod
    def list():
        return { "accounts": database['accounts'] }
    
    @staticmethod
    def auth(accountPass):
        account = AccountModel.findByAccountPass(accountPass)

        if account:
            return { "account": account, "ok": True }
        
        return { "message": "Conta não existente!", "ok": False }
    
    @staticmethod
    def addTransaction(fromAccountPass, toAccountPass, toAgency, value):
        if fromAccountPass == None or toAccountPass == None or toAgency == None or value == None:
            return { "message": "Campos inválidos enviados!", "ok": False }

        transactionObj = {
            "from": fromAccountPass,
            "to": toAccountPass,
            "agency": toAgency,
            "value": value
        }

        database['transactions'].append(transactionObj)

        return { "message": "Transferência adicionada à fila com sucesso!", "ok": True }
    
    @staticmethod
    def transfer(fromAccountPass, toAccountPass, toAgency, value):
        fromAccount = AccountModel.findByAccountPass(fromAccountPass)
        toAccount = AccountModel.findByAccountPass(toAccountPass)

        if fromAccount:
            if float(fromAccount['balance']) >= float(value):
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                agency = ip_address.split(".")[-1]

                if str(toAgency) == str(agency):
                    if toAccount:
                        AccountModel.transfer(account=fromAccount, value=value)
                        AccountModel.receive(account=toAccount, value=value)

                        return { "message": "Transferência realizada com sucesso!", "ok": True }
                    else:
                        return { "message": "Conta destino não encontrada!", "ok": False }
                else:
                    # Lógica para transferências entre bancos distintos.
                    return { "message": "Transferência realizada para outro banco com sucesso!", "ok": True }
            else:
                return { "message": "Saldo insuficiente!", "ok": False }
        
        else:
            return { "message": "Conta remetente não encontrada!", "ok": False }
        
    @staticmethod
    def deposit(accountPass, amount):
        account = AccountModel.findByAccountPass(accountPass)

        if account:
            AccountModel.deposit(account, amount)
            
            return { "message": "Depósito realizado com sucesso!", "ok": True }

        return { "message": "Conta não encontrada!", "ok": False }
    
    @staticmethod
    def withdraw(accountPass, amount):
        account = AccountModel.findByAccountPass(accountPass)

        if account:
            if account['balance'] >= amount:
                AccountModel.withdraw(account, amount)
            
                return { "message": "Saque realizado com sucesso!", "ok": True }
            
            return { "message": "Saldo insuficiente!", "ok": False }

        return { "message": "Conta não encontrada!", "ok": False }