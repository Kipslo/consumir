import sqlite3 as sql

class connect():
    def __init__(self):
        
        self.connected = {}
        self.cursor = {}
        self.dbs = {"contas":"sql", "comandas":"commands", "produtos":"products", "historico":"his", "clientes":"clients", "configuracoes":"config", "temporario":"temp", "impressora":"printer"}
    def createtables(self):
        self.connect("configuracoes")
        self.configcursor.execute("""CREATE TABLE IF NOT EXISTS Config(
                                  cod INTEGER PRIMARY KEY,
                                  stylemode VARCHAR,
                                  maxcommands INTEGER(4), 
                                  cnpj VARCHAR(20),
                                  housename VARCHAR(30),
                                  adress VARCHAR(30),
                                  fone VARCHAR(10),
                                  printer VARCHAR(30)
                                  )""")
        self.configcursor.execute("""CREATE TABLE IF NOT EXISTS Entries(
                                  cod INTEGER PRIMARY KEY, 
                                  name VARCHAR(30),
                                  entry VARCHAR(30))""")
        self.desconnect("configuracoes")
        self.connect("contas")
        self.contscursor.execute("""CREATE TABLE IF NOT EXISTS Conts(
                                 username VARCHAR(30) NOT NULL,
                                 name VARCHAR(20) NOT NULL,
                                 password VARCHAR(30) NOT NULL,
                                 valupayment VARCHAR(10),
                                 periodpayment VARCHAR(10),
                                 permissionmaster CHAR(1) NOT NULL, 
                                 permissionrelease CHAR(1),
                                 permissionentry CHAR(1),
                                 permissionclose CHAR(1),
                                 lastlogin CHAR(19),
                                 lastmodification CHAR(19)
                                 )""")
        self.desconnect("contas")
        self.connect("comandas")
        self.commandscursor.execute("""CREATE TABLE IF NOT EXISTS CommandsActive(
                                    number INTEGER PRIMARY KEY,
                                    initdate CHAR(10),
                                    hour CHAR(5),
                                    nameclient VARCHAR(30),
                                    idclient INTEGER(5)
                                    )""")
        self.commandscursor.execute("""CREATE TABLE IF NOT EXISTS Consumption(
                                    cod INTEGER PRIMARY KEY,
                                    number VARCHAR(4),
                                    date CHAR(10),
                                    hour CHAR(5),
                                    waiter VARCHAR(30),
                                    price VARCHAR(8),
                                    unitprice VARCHAR(8),
                                    quantity INTERGER(3),
                                    product VARCHAR(30),
                                    type VARCHAR(30),
                                    size VARCHAR(30),
                                    text VARCHAR(100),
                                    category VARCHAR(30),
                                    printer VARCHAR(30)
                                    )""")
        self.commandscursor.execute("""CREATE TABLE IF NOT EXISTS Payments(
                                    cod INTEGER PRIMARY KEY,
                                    number INTEGER(4),
                                    type VARCHAR(10),
                                    quantity VARCHAR(8)
                                    )""")
        self.desconnect("comandas")
        self.connect("produtos")
        self.productcursor.execute("""CREATE TABLE IF NOT EXISTS Products(
                                   name VARCHAR(30),
                                   type VARCHAR(10),
                                   category VARCHAR(10),
                                   price VARCHAR(8),
                                   printer VARCHAR(30),
                                   stock INTEGER(10)
                                   )""")
        self.productcursor.execute("""CREATE TABLE IF NOT EXISTS Notes(
                                    id INTEGER PRIMARY KEY,
                                    text VARCHAR(30),
                                    category VARCHAR(30)
                                    )""")
        self.productcursor.execute("""CREATE TABLE IF NOT EXISTS Combo(
                                   name VARCHAR(30),
                                   price VARCHAR(8),
                                   products VARCHAR(50)
                                   )""")
        self.productcursor.execute("""CREATE TABLE IF NOT EXISTS CurrentProducts(
                                   name VARCHAR(30),
                                   type VARCHAR(10),
                                   command VARCHAR(10),
                                   releasedate CHAR(10),
                                   releasehour CHAR(5),
                                   releasefunctionary VARCHAR(30),
                                   currentprice VARCHAR(8)
                                   )""")
        self.productcursor.execute("""CREATE TABLE IF NOT EXISTS Category(
                                   cod INTEGER PRIMARY KEY,
                                   name VARCHAR(30)
                                   
                                   )""")
        self.productcursor.execute("""CREATE TABLE IF NOT EXISTS SizeofProducts(
                                   product VARCHAR(30),
                                   price VARCHAR(8),
                                   name VARCHAR(30),
                                   category VARCHAR(30)
                                   )""")
        self.desconnect("produtos") 
        self.connect("historico")
        self.historycursor.execute("""CREATE TABLE IF NOT EXISTS ClosedCommand(
                                    cod INTEGER PRIMARY KEY,
                                    number VARCHAR(4),
                                    date CHAR(10),
                                    hour CHAR(5),
                                    nameclient VARCHAR(30),
                                    idclient INTEGER(5),
                                    totalprice VARCHAR(8),
                                    datefinish VARCHAR(19),
                                    cashier VARCHAR(30),
                                    pay VARCHAR(8),
                                    cashdesk INTEGER(6)
                                    )""")
        self.historycursor.execute("""CREATE TABLE IF NOT EXISTS Cashdesk(
                                    id INTEGER PRIMARY KEY,
                                    initdate VARCHAR(20),
                                    finishdate VARCHAR(20),
                                    status VARCHAR(5),
                                    totalcash VARCHAR(10)
                                    )""")
        self.historycursor.execute("""CREATE TABLE IF NOT EXISTS Payments(
                                    commandid INTEGER(4),
                                    type VARCHAR(10),
                                    quantity VARCHAR(8)
                                    )""")
        self.historycursor.execute("""CREATE TABLE IF NOT EXISTS Products(
                                    commandid INTEGER(6),
                                    name VARCHAR(30),
                                    type VARCHAR(10),
                                    quantity VARCHAR(4),
                                    unitprice VARCHAR(8),
                                    releasedate CHAR(10),
                                    releasehour CHAR(5),
                                    waiter VARCHAR(30),
                                    price VARCHAR(8)
                                    )""")
        self.historycursor.execute("""CREATE TABLE IF NOT EXISTS SupplierHistory(
                                   cod INTEGER PRIMARY KEY,
                                   product VARCHAR(30),
                                   supplier VARCHAR(20),
                                   cost VARCHAR(30),
                                   quantity INTEGER(5),
                                   cashid INTEGER(8)
                                   )""")
        self.desconnect("historico")
        self.connect("temporario")
        self.tempdbcursor.execute("""CREATE TABLE IF NOT EXISTS TempProducts(
                                cod INTEGER PRIMARY KEY,
                                number INTEGER(4),
                                product VARCHAR(30),
                                category VARCHAR(30),
                                unitprice VARCHAR(8),
                                quatity INTEGER(3),
                                text VARCHAR(100),
                                waiter VARCHAR(30),
                                type VARCHAR(10),
                                printer VARCHAR(30)
                                    )""")
        self.tempdbcursor.execute("""CREATE TABLE IF NOT EXISTS TempLogin(
                                  name VARCHAR(30),
                                  lastlogin varchar(19)
                                  )""")
        self.desconnect("temporario")
        self.connect("clientes")
        self.clientscursor.execute("""CREATE TABLE IF NOT EXISTS Clients(
                                id INTEGER PRIMARY KEY,
                                name VARCHAR(30),
                                fone INTEGER(13),
                                email VARCHAR(30),
                                idade INTEGER(3),
                                genero VARCHAR(10)
        )""")
        self.desconnect("clientes")
        self.connect(self.bds["impressora"])
        self.printercursor.execute("""CREATE TABLE IF NOT EXISTS ProductPrint(
                                   product VARCHAR(500),
                                   printer VARCHAR(30),
                                   type VARCHAR(10),
                                   command INTEGER(4),
                                   waiter VARCHAR(30),
                                   date VARCHAR(20),
                                   qtd INTEGER(3), 
                                   text VARCHAR(100)
                                   )""")
        self.printercursor.execute("""CREATE TABLE IF NOT EXISTS ClosedPrinter(
                                    id INTEGER PRIMARY KEY,
                                    command INTEGER(4),
                                    date VARCHAR(20),
                                    permission VARCHAR(5),
                                    client VARCHAR(30)
        )""")
        self.printercursor.execute("""CREATE TABLE IF NOT EXISTS ProductsClosed(
                                    id INTEGER(10),
                                    product VARCHAR(500),
                                    type VARCHAR(10),
                                    qtd INTEGER(3), 
                                    unitprice VARCHAR(8)
                                    )""")
        self.printercursor.execute("""CREATE TABLE IF NOT EXISTS Printers(
                                   name VARCHAR(30),
                                   ip VARCHAR(19)
                                   )""")
        self.desconnect("impressora")
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