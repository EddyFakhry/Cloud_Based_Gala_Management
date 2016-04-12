import pymongo
import constants

class Mongo:
    def __init__(self,config={}):
        self._config = config

    def __enter__(self):
        self._client = pymongo.MongoClient()
        return self._client["galadb"]

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.close()
