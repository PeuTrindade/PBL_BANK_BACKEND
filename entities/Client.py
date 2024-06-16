import random

class Client:
    def __init__(self, name, email, age):
        self.id = random.randint(10000, 99999)
        self.name = name
        self.email = email
        self.age = age
        
    def transformToDic(self):
        dic = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age
        }
        
        return dic