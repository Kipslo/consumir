import sqlite3 as sql

class connect():
    def __init__(self):
        
        self.connected = {}
        self.cursor = {}
        self.dbs = {"contas":"sql", "comandas":"commands", "produtos":"products", "historico":"his", "clientes":"clients", "configuracoes":"config", "temporario":"temp", "impressora":"printer"}
    def connect(self, name):
        name = self.dbs[name]
        self.connected[name] = sql.connect(name + ".db")
        self.cursor[name] = self.connected[name].cursor()
    def desconnect(self, name):
        name = self.dbs[name]
        self.connected[name].commit()
        self.connected[name].close()
    def execute(self, name, cod):
        name = self.dbs[name]
        self.name.execute(cod)