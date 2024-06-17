from models.TokenModel import TokenModel
from database.database import database
import requests
import time

class TokenController:
    @staticmethod
    def sendToken():
        try:
            while True:
                if database['token']:
                    tokenCoolDown = 5

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
                if database['token']:
                    print(database['transactions'][0])
        except:
            return { "message": "Ocorreu um erro inesperado!", "ok": False }