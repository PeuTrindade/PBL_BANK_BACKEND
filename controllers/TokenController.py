from models.TokenModel import TokenModel
from controllers.AccountController import AccountController
from database.database import database
import requests
import time

class TokenController:
    @staticmethod
    def sendToken():
        try:
            while True:
                if database['token'] and database['doingTransaction'] == False:
                    tokenCoolDown = 30

                    time.sleep(tokenCoolDown)

                    currentApiIndex = database['apisList'].index(database['apiPort'])
                    nextPort = None
                    
                    if len(database['apisList']) == int(currentApiIndex) + 1:
                        nextPort = database['apisList'][0]
                    else:
                        nextPort = database['apisList'][int(currentApiIndex) + 1]

                    try:
                        tokenShareRequest = requests.post(f'http://localhost:{nextPort}/receiveToken', json={'token': database['token'] })
                        
                        if tokenShareRequest.status_code == 200:
                            TokenController.removeToken()

                            print(f'Token enviado com sucesso para localhost:{nextPort}!')
                        else:
                            print(f'Falha ao enviar token para localhost:{nextPort}! Tentaremos novamente em {tokenCoolDown} segundos.')

                    except requests.exceptions.RequestException as e:
                        print(f'Falha ao enviar token para localhost:{nextPort}! Tentaremos novamente em {tokenCoolDown} segundos.')
        except:
            return { "message": "Ocorreu um erro inesperado!", "ok": False }

    @staticmethod
    def saveToken(token):
        try:
            if token == None:
                return { "message": "Token inexistente", "ok": False }
            
            TokenModel.save(token)

            return { "message": "Token salvo com sucesso!", "ok": True }
        except Exception as e:
            return { "message": "Ocorreu um erro inesperado! " + str(e), "ok": False }
    
    @staticmethod
    def removeToken():
        try:  
            TokenModel.remove()

            return { "message": "Token removido com sucesso!", "ok": True }
        except:
            return { "message": "Ocorreu um erro inesperado!", "ok": False }
        
    @staticmethod
    def doTransactions():
        try:
            while True:
                for transaction in database['transactions']:
                    if database['token']:
                        database['doingTransaction'] = True

                        if type(transaction) is list:
                            for subTransaction in transaction:
                                AccountController.transfer(subTransaction['from'], subTransaction['to'], subTransaction['agency'], subTransaction['value'], subTransaction['toReceive'])
                            
                            database['doingTransaction'] = False
                           
                            database['transactions'].remove(transaction)
                        else:
                            AccountController.transfer(transaction['from'], transaction['to'], transaction['agency'], transaction['value'], transaction['toReceive'])

                            database['doingTransaction'] = False

                            database['transactions'].remove(transaction)
                    else:
                        break
        except:
            return { "message": "Ocorreu um erro inesperado!", "ok": False }