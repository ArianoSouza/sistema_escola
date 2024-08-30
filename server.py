from pymongo import MongoClient

class mongoConect():
    def __init__(self) -> None:
        self.mongo_string = "mongodb+srv://arianosouza:84puZBDDakKooXtf@cluster0.hkwcy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.colection = "database_escola"
    def conection(self):
        self.conect = MongoClient(self.mongo_string)
    def get_mongo_db(self):
        self.db_mongo = self.conect['escola']
        return self.db_mongo
    

