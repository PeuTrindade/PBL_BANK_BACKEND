from models.AccountModel import AccountModel
from models.ClientModel import ClientModel
from database.database import database
import socket
import requests

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
    def verifyAccountExists(accountPass, accounts):
        if len(accounts) > 0:
            print(accounts)
            for account in accounts:
                if account['accountPass'] == accountPass:
                    return True
                
            return False
        
        return False
    
    @staticmethod
    def addTransaction(fromAccountPass, toAccountPass, toAgency, value, toReceive):
        if fromAccountPass == None or toAccountPass == None or toAgency == None or value == None:
            return { "message": "Campos inválidos enviados!", "ok": False }
        
        if toReceive == 0:
            fromAccount = AccountModel.findByAccountPass(fromAccountPass)
            toAccount = AccountModel.findByAccountPass(toAccountPass)
            agency = str(database['apiPort'])[0]

            if fromAccount == None:
                return { "message": "Conta remetente não encontrada!", "ok": False }
            
            if str(agency) == str(toAgency):
                if toAccount == None:
                    return { "message": "Conta destino não encontrada!", "ok": False }
            else:
                bankPort = int(toAgency) * 1000
        
                accountListRequest = requests.get(f'http://localhost:{bankPort}/account')
            
                if accountListRequest.status_code == 200:
                    accounts = accountListRequest.json()

                    if AccountController.verifyAccountExists(accountPass=toAccountPass, accounts=accounts['accounts']) == False:
                        return { "message": "Conta destino não encontrada no banco de destino!", "ok": False }
                else:
                    return { "message": "Erro ao buscar conta destino em outro banco!", "ok": False }

            if float(fromAccount['balance']) < float(value):
                return { "message": "Saldo insuficiente!", "ok": False }

        transactionObj = {
            "from": fromAccountPass,
            "to": toAccountPass,
            "agency": toAgency,
            "value": value,
            "toReceive": toReceive
        }

        database['transactions'].append(transactionObj)

        return { "message": "Transferência adicionada à fila com sucesso!", "ok": True }
    
    @staticmethod
    def addTransactions(fromAccountPass, transactions):
        if len(transactions) == 0:
            return { "message": "Pacote vazio!", "ok": False }

        transactions_formatted = []

        for transaction in transactions:
            obj = {
                "from": fromAccountPass,
                "to": transaction['to'],
                "agency": transaction['agency'],
                "value": transaction['amount'],
                "toReceive": transaction['toReceive']
            }

            transactions_formatted.append(obj)


        for t in transactions_formatted:
            if t['toReceive'] == 0:
                fromAccount = AccountModel.findByAccountPass(fromAccountPass)
                toAccount = AccountModel.findByAccountPass(t['to'])
                agency = str(database['apiPort'])[0]

                if fromAccount == None:
                    return { "message": "Conta remetente não encontrada!", "ok": False }
                
                if str(agency) == str(t['agency']):
                    if toAccount == None:
                        return { "message": "Conta destino não encontrada!", "ok": False }
                else:
                    bankPort = int(t['agency']) * 1000

                    accountListRequest = requests.get(f'http://localhost:{bankPort}/account')

                    if accountListRequest.status_code == 200:
                        accounts = accountListRequest.json()

                        if AccountController.verifyAccountExists(accountPass=t['to'], accounts=accounts['accounts']) == False:
                            return { "message": "Conta destino não encontrada no banco de destino!", "ok": False }
                    else:
                        return { "message": "Erro ao buscar conta destino em outro banco!", "ok": False }

                if float(fromAccount['balance']) < float(t['value']):
                    return { "message": "Saldo insuficiente!", "ok": False }

        database['transactions'].append(transactions_formatted)

        return { "message": "Pacote de transferências adicionados à fila com sucesso!", "ok": True }
    
    @staticmethod
    def transfer(fromAccountPass, toAccountPass, toAgency, value, toReceive):
        fromAccount = AccountModel.findByAccountPass(fromAccountPass)
        toAccount = AccountModel.findByAccountPass(toAccountPass)

        if toReceive == 1:
            if toAccount:
                AccountModel.receive(account=toAccount, value=value)

                print("Transferência recebida com sucesso!")
            else:
                print("Conta destino não encontrada!")
        else:
            if fromAccount:
                if float(fromAccount['balance']) >= float(value):
                    agency = str(database['apiPort'])[0]

                    if str(toAgency) == str(agency):
                        if toAccount:
                            AccountModel.transfer(account=fromAccount, value=value)
                            AccountModel.receive(account=toAccount, value=value)

                            print("Transferência realizada com sucesso!")
                        else:
                            print("Conta destino não encontrada!")
                    else:
                        if toReceive == 0:
                            bankPort = int(toAgency) * 1000

                            try:
                                transferRequest = requests.post(f'http://localhost:{bankPort}/account/transfer/{fromAccountPass}', json={ "to": toAccountPass, "amount": value, "agency": toAgency, "toReceive": 1 })

                                if transferRequest.status_code == 200:
                                    AccountModel.transfer(account=fromAccount, value=value)
                    
                                    print("Transferência realizada para outro banco com sucesso!")
                                else:
                                    print("Transferência para outro banco falhou!")
                            except requests.exceptions.RequestException as e:
                                print(f'Falha ao transferir para localhost:{bankPort}!')
                else:
                    print("Saldo insuficiente!")
            
            else:
                print("Conta remetente não encontrada!")
        
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