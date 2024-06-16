from entities.Client import Client
from database.database import database

class ClientModel:
    @staticmethod
    def create(name, email, age):
        newClient = Client(name, email, age)
        
        database['clients'].append(newClient.transformToDic())

    @staticmethod
    def clientExists(email):
        clients = database['clients']
        client = None

        for c in clients:
            if c["email"] == email:
                client = c
            
        if client:
            return True
        
        return False
    
    @staticmethod
    def clientExistsById(id):
        clients = database['clients']
        client = None

        for c in clients:
            if c["id"] == id:
                client = c
            
        if client:
            return True
        
        return False