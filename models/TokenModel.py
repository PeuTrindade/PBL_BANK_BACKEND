from database.database import database

class TokenModel:
    @staticmethod
    def save(token):
        database['token'] = token

    @staticmethod
    def remove():
        database['token'] = None