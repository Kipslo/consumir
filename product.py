import connect, table
from priceClass import priceClass
class product(connect):
    def __init__(self, name:str = "", tipe:str = "", category:str = "", price:str = "", printer:str = "", stock:str = "0"):
        self.name, self.tipe, self.category, self.price, self.printer, self.stock = name, tipe, category, price, printer, stock

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
        data = product_table.data(where= tuple(where), value=tuple(values))
        self.name, self.tipe, self.category, self.price, self.printer, self.stock = data[0]
        self.priceBR = priceClass.getPrice(self.price)
    def create(self):
        pass