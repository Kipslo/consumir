class priceClass():
    def __init__(self, price):
        self.getprice(price)
    @staticmethod
    def getPrice(price:str =""):
        price = price.replace(",", ".").split(".")
        
        decimal = str(int(price[1])) + ("0" * ((len(str(int(price[1]))) - 2) * -1)) 
       
        return "R$ " + price[0] + "," + decimal