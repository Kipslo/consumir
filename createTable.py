from table import table
def createTable():
    tableConfig = table("configuracoes", "Config", ("cod", "stylemode", "maxcommands", "cnpj", "housename", "adress", "fone", "printer"), 
                        ("INTEGER PRIMARY KEY", "VARCHAR(15)", "INTEGER(4)", "VARCHAR(20)", "VARCHAR(30)", "VARCHAR(30)", "VARCHAR(10)", "VARCHAR(30)")).create()
    tableEntries = table("configuracoes", "Entries", ("cod", "name", "entry"), ("INTEGER PRIMARY KEY", "VARCHAR(30)", "VARCHAR(30)")).create()
        
    tableConts = table("contas", "Conts", ("username", "name", "password", "valuepayment", "periodpayment", "permissionmaster", "permissionrelease", "permissionentry", "permissionclose", "lastlogin", "lastmodification"),
                ("VARCHAR(30) NOT NULL", "VARCHAR(20) NOT NULL", "VARCHAR(30) NOT NULL", "VARCHAR(10)", "VARCHAR(10)", "CHAR(1)", "CHAR(1)", "CHAR(1)", "CHAR(1)", "CHAR(19)", "CHAR(19)")).create()
    tableCommandsActive = table("comandas", "CommandsActive", ("number", "initdate", "hour", "nameclient", "idclient"), 
                                ("INTEGER PRIMARY KEY", "CHAR(10)", "CHAR(5)", "VARCHAR(30)", "INTEGER(5)")).create()
    tableConsumption = table("comandas", "Consumption", ("cod", "number", "date", "hour", "waiter", "price", "unitprice", "quantity", "product", "type", "size", "text", "category", "printer"), 
                         ("INTEGER PRIMARY KEY", "VARCHAR(4)", "CHAR(10)", "CHAR(5)", "VARCHAR(30)", "VARCHAR(8)", "VARCHAR(8)", "INTEGER(3)", "VARCHAR(30)", "VARCHAR(30)", "VARCHAR(30)", "VARCHAR(100)", "VARCHAR(30)", "VARCHAR(30)")).create()
    tablePayments = table("comandas", "Payments", ("cod", "number", "type", "quantity"), ("INTEGER PRIMARY KEY", "INTEGER(4)", "VARCHAR(10)", "VARCHAR(8)")).create()
    tableProducts = table("produtos", "Products", ("name", "type", "category", "price", "printer", "stock"), ("VARCHAR(30)", "VARCHAR(10)", "VARCHAR(10)", "VARCHAR(8)", "VARCHAR(30)", "INTEGER(10)")).create()
    tableNotes = table("produtos", "Notes", ("id", "text", "category"), ("INTEGER PRIMARY KEY", "VARCHAR(30)", "VARCHAR(30)")).create()
    taleCombo = table("produtos", "Combo", ("name", "price", "products"), ("VARCHAR(30)", "VARCHAR(8)", "VARCHAR(50)")).create()
    tableCurrentProducts = table("produtos", "CurrentProducts", ("name", "type", "command", "releasedate", "releasehour", "releasefunctionary", "currentprice"), 
                                 ("VARCHAR(30)", "VARCHAR(10)", "VARCHAR(10)", "CHAR(10)", "CHAR(5)", "VARCHAR(30)", "VARCHAR(8)")).create()
    tableCategory = table("produtos", "Category", ("cod", "name"), ("INTEGER PRIMARY KEY", "VARCHAR(30)")).create()
    tableSizeofProducts = table("produtos", "SizeofProducts", ("product", "price", "name", "category"), ("VARCHAR(30)", "VARCHAR(8)", "VARCHAR(30)", "VARCHAR(30)")).create()
    tableClosedCommand = table("historico", "ClosedCommand", ("cod", "number", "date", "hour", "nameclient", "idclient", "totalprice", "datefinish", "cashier", "pay", "cashdesk"), ("INTEGER PRIMARY KEY", "VARCHAR(4)", "CHAR(10)", "CHAR(5)", "VARCHAR(30)", "INTEGER(5)", "VARCHAR(8)", "VARCHAR(19)", "VARCHAR(30)", "VARCHAR(8)", "VARCHAR(6)")).create()
    tableCashdesk = table("historico", "Cashdesk", ("id", "initdate", "finishdate", "status", "totalcash"), ("INTEGER PRIMARY KEY", "VARCHAR(20)", "VARCHAR(20)", "VARCHAR(5)", "VARCHAR(10)")).create()
    tablePayments = table("historico", "Payments", ("commandid", "type", "quantity"), ("INTEGER(4)", "VARCHAR(10)", "VARCHAR(8)"))
    tableProducts = table("historico", "Products", ("commandid", "name", "type", "quantity", "unitprice", "releasedate", "releasehour", "waiter", "price"), ("INTEGER(6)", "VARCHAR(30)", "VARCHAR(10)", "VARCHAR(4)", "VARCHAR(8)", "CHAR(10)", "CHAR(5)", "VARCHAR(30)", "VARCHAR(8)")).create()
    tableSupplierHistory = table("historico", "SupplierHistory", ("cod", "product", "supplier", "cost", "quantity", "cashid"), ("INTEGER PRIMARY KEY", "VARCHAR(30)", "VARCHAR(20)", "VARCHAR(30)", "INTEGER(5)", "INTEGER(8)")).create()
    tableTempProducts = table("temporario", "TempProducts", ("cod", "number", "product", "category", "unitprice", "quatity", "text", "waiter", "type", "printer"), ("INTEGER PRIMARY KEY", "INTEGER(4)", "VARCHAR(30)", "VARCHAR(30)", "VARCHAR(8)", "INTEGER(3)", "VARCHAR(100)", "VARCHAR(30)", "VARCHAR(10)", "VARCHAR(30)")).create()
    tableTempLogin = table("temporario", "TempLogin", ("name", "lastlogin"), ("VARCHAR(30)", "VARCHAR(19)")).create()
    tableClients = table("clientes", "Clients", ("id", "name", "fone", "email", "idade", "genero"), ("INTEGER PRIMARY KEY", "VARCHAR(30)", "INTEGER(13)", "VARCHAR(30)", "INTEGER(3)", "VARHCAR(10)")).create()
    tableProductPrint = table("impressoras", "ProductPrint", ("product", "printer", "type", "command", "waiter", "date", "qtd", "text"), ("VARCHAR(500)", "VARCHAR(30)", "VARCHAR(10)", "INTEGER(4)", "VARCHAR(30)", "VARCHAR(20)", "INTEGER(3)", "VARCHAR(100)")).create()
    tableClosedPrinter = table("impressoras", "ClosedPrinter", ("id", "command", "date", "permission", "client"), ("INTEGER PRIMARY KEY", "INTEGER(4)", "VARCHAR(20)", "VARCHAR(5)", "VARCHAR(30)")).create()
    tableProductsClosed = table("impressoras", "ProductsClosed", ("id", "product", "type", "qtd", "unitprice"), ("INTEGER(10)", "VARCHAR(500)", "VARCHAR(10)", "INTEGER(3)", "VARCHAR(8)")).create()
    tablePrinters = table("impressoras", "Printers", ("name", "ip"), ("VARCHAR(30)", "VARCHAR(19)")).create()