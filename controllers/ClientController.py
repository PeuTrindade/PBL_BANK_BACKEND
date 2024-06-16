from models.ClientModel import ClientModel
from database.database import database

class ClientController:
    @staticmethod
    def create(name, email, age):
        if (name == None or email == None or age == None):
            return { "message": "Campos em branco foram enviados", "ok": False }
        
        elif ClientModel.clientExists(email) == True:
            return { "message": "Cliente já cadastrado com este email!", "ok": False }

        ClientModel.create(name, email, age)
        
        return { "message": "Cliente cadastrado com sucesso!", "ok": True }
    
    @staticmethod
    def list():
        return { "clients": database['clients'] }