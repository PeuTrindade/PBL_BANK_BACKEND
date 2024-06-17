from flask import Flask, jsonify, request
from controllers.TokenController import TokenController
import threading
from database.database import database
from controllers.ClientController import ClientController
from controllers.AccountController import AccountController

app = Flask(__name__)

def send_token():
    TokenController.sendToken()


def do_transactions():
    TokenController.doTransactions()


@app.route('/receiveToken', methods=['POST'])
def receive_token():
    try:
        data = request.json
        token = data.get('token')

        controllerResponse = TokenController.saveToken(token)

        if controllerResponse['ok'] == False:
            return jsonify({ "message": controllerResponse['message'] }), 400
  
        return jsonify({ "message": controllerResponse['message'] }), 200

    except Exception as e:
        return jsonify({ "message": "Ocorreu um erro interno: " + str(e)  }), 500


@app.route('/client', methods=['POST'])
def createClient():
    try:
        requestBody = request.json
        
        name = requestBody.get('name')
        email = requestBody.get('email')
        age = requestBody.get('age')
        
        controllerResponse = ClientController.create(name=name, email=email, age=age)
        
        if controllerResponse['ok']:
            return jsonify({ "message": controllerResponse['message'] }), 201
        else:
            return jsonify({ "message": controllerResponse['message'] }), 400
        
    except Exception as e:
        return jsonify({ "message": "Ocorreu um erro interno: " + str(e)  }), 500
    

@app.route('/client', methods=['GET'])
def listClients():
    try:
        clients = ClientController.list()
        
        return jsonify({ "clients": clients['clients'] }), 200
    
    except Exception as e:
        return jsonify({ "message": "Ocorreu um erro interno: " + str(e)  }), 500

  
@app.route('/account', methods=['POST'])
def createAccount():
    try:
        requestBody = request.json
        
        clientIds = requestBody.get('clientIds')
        accountType = requestBody.get('accountType')
        agency = requestBody.get('agency')
        accountPass = requestBody.get('accountPass')
        
        controllerResponse = AccountController.create(clientIds, accountType, agency, accountPass)
        
        if controllerResponse['ok']:
            return jsonify({ "message": controllerResponse['message'] }), 201
        else:
            return jsonify({ "message": controllerResponse['message'] }), 400
        
    except Exception as e:
        return jsonify({ "message": "Ocorreu um erro interno: " + str(e)  }), 500


@app.route('/account', methods=['GET'])
def listAccounts():
    try:
        accounts = AccountController.list()
        
        return jsonify({ "accounts": accounts['accounts'] }), 200
    
    except Exception as e:
        return jsonify({ "message": "Ocorreu um erro interno: " + str(e)  }), 500
    

@app.route('/account/auth', methods=['POST'])
def authAccount():
    try:
        requestBody = request.json
 
        accountPass = requestBody.get('accountPass')
        verifyAuth = AccountController.auth(accountPass)

        if verifyAuth['ok'] == False:
            return jsonify({ "message": verifyAuth['message'] }), 400
        
        return jsonify({ "account": verifyAuth['account'] }), 200

    except Exception as e:
        return jsonify({ "message": "Ocorreu um erro interno: " + str(e)  }), 500


@app.route('/account/transfer/<string:fromAccountPass>', methods=['POST'])
def transfer(fromAccountPass):
    try:
        requestBody = request.json
 
        toAccountPass = requestBody.get('to')
        value = requestBody.get('amount')
        toAgency = requestBody.get('agency')

        controllerResponse = AccountController.addTransaction(fromAccountPass, toAccountPass, toAgency, value)

        if controllerResponse['ok'] == False:
            return jsonify({ "message": controllerResponse['message'] }), 400
        
        return jsonify({ "account": controllerResponse['message'] }), 200

    except Exception as e:
        return jsonify({ "message": "Ocorreu um erro interno: " + str(e)  }), 500
    

@app.route('/account/deposit/<string:accountPass>', methods=['PATCH'])
def deposit(accountPass):
    try:
        requestBody = request.json
        amount = requestBody.get('amount')

        controllerResponse = AccountController.deposit(accountPass, amount)

        if controllerResponse['ok'] == False:
            return jsonify({ "message": controllerResponse['message'] }), 400
        
        return jsonify({ "account": controllerResponse['message'] }), 200

    except Exception as e:
        return jsonify({ "message": "Ocorreu um erro interno: " + str(e)  }), 500

   
@app.route('/account/withdraw/<string:accountPass>', methods=['PATCH'])
def withdraw(accountPass):
    try:
        requestBody = request.json
        amount = requestBody.get('amount')

        controllerResponse = AccountController.withdraw(accountPass, amount)

        if controllerResponse['ok'] == False:
            return jsonify({ "message": controllerResponse['message'] }), 400
        
        return jsonify({ "account": controllerResponse['message'] }), 200

    except Exception as e:
        return jsonify({ "message": "Ocorreu um erro interno: " + str(e)  }), 500


if __name__ == '__main__':
    apiPort = input('Qual a porta do seu Banco?: ')

    database['apiPort'] = int(apiPort)

    # Inicia uma thread para enviar o token de forma assíncrona
    sender_thread = threading.Thread(target=send_token, daemon=True)
    sender_thread.start()

    # Inicia uma thread para realizar transações quando há o token
    sender_thread = threading.Thread(target=do_transactions, daemon=True)
    sender_thread.start()

    app.run(debug=False, port=apiPort)