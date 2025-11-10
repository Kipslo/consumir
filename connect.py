import sqlite3 as sql

class connect():
    def __init__(self):
        
        self.connected = {}
        self.cursor = {}
        self.dbs = {"contas":"sql", "comandas":"commands", "produtos":"products", "historico":"his", "clientes":"clients", "configuracoes":"config", "temporario":"temp", "impressora":"printer"}
    def connect(self, db):
        self.connected[db] = sql.connect(self.dbs[db] + ".db")
        self.cursor[db] = self.connected[db].cursor()
    def desconnect(self, db):
        self.connected[db].commit()
        self.connected[db].close()
    def execute(self, db, cod, fordata = False):
        self.connect(db)
        if fordata:
            temp = self.cursor[db].execute(cod)
            listen = []
            for i in temp:
                listen.append(i)
            return listen
        else:
            self.cursor[db].execute(cod)

        self.desconnect(db)