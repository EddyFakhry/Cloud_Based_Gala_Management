import csv, pyodbc


class mdbextractor:
    def __init__(self,mdb_file):
        self._mdb_file = mdb_file

    def __enter__(self):
        self._mdb = self._mdb_file
        self._drv = '{Microsoft Access Driver (*.mdb)}'
        self._con = pyodbc.connect('DRIVER={};DBQ={};'.format(self._drv,self._mdb))
        self._cur = self._con.cursor()
        return self._cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._con.close()
