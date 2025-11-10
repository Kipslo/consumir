from connect import connect
from table import table
from priceClass import priceClass
class product(connect):
    def __init__(self, name:str = "", tipe:str = "", category:str = "", price:str = "", printer:str = "", stock:str = "0"):
        self.name, self.tipe, self.category, self.price, self.printer, self.stock = name, tipe, category, price, printer, stock
        super().__init__()
        self.permissionCreate = True
    def get(self):
        product_table = table("produtos", "Products")
        where = []
        values = []
        if self.name != "":
            where.append("name"); values.append(self.name)
        if self.tipe != "":
            where.append("type"); values.append(self.tipe)
        if self.category != "":
            where.append("category"); values.append(self.category)
        data = product_table.getData(where= tuple(where), value=tuple(values))
        self.name, self.tipe, self.category, self.price, self.printer, self.stock = data[0]
        if self.name != "" and self.tipe != "" and self.category != "":
            self.permissionCreate = False
        self.priceBR = priceClass.getPrice(self.price)
    def create(self):
        if self.name != "" and self.tipe != "" and self.category != "" and self.permissionCreate:
            self.connect("produtos")
            if self.tipe == "SIZE":
                tableSize = table()
            
            self.desconnect("produtos")