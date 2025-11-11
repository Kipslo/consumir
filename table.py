from connect import connect
class table(connect):
    def __init__(self, db : str, name : str, columns : tuple = (), values: tuple = ()):
        super().__init__()
        self.db = db
        self.name = name
        self.columns= columns
        self.values = values
        self.createPermission = False
        if columns != () and values != ():
            self.createPermission = True
    def fortext(self, joinstr:str, middle:str = "", columns, values = []):
        if values == ():
            for i in columns:
                values.append("")
        rows = []
        for i in range(len(columns)):
            rows.append(f"{columns[i]}{middle}{values[i]}")
        result = joinstr.join(rows)
        return
    def create(self, columns : tuple = (), values: tuple = ()):
        if columns != ():
            self.columns, self.values = columns, values
        if len(self.columns) == len(self.values) and self.db != "" and self.name != "" and self.createPermission:
            rows = self.fortext(", ", " ", self.columns, self.values)
            self.execute(self.db, f"CREATE TABLE IF NOT EXISTS {self.name}({rows})")
    def deleteData(self, where:tuple = (), value:tuple = ()):
        rows = ""
        if where != ():
            rows = " WHERE " + self.fortext(" AND ", " = ", where, value)
        self.execute(self.db, f"DELETE FROM {self.name}{rows}")
    def updateData(self, newcolumns:tuple = (), newvalues:tuple = (), where:tuple = (), valuewhere:tuple = ()):
        if where == ():
            where, valuewhere = self.columns, self.values
        if where != ():
            whererows = self.fortext(" AND ", " = ", where, valuewhere)
        newrows = self.fortext(", ", " = ", newcolumns, newvalues)
        self.execute(self.db, f"UPDATE {self.name} SET {newrows} WHERE {whererows}")
    def getData(self, column: tuple = ("*", ), where:tuple = (), value: tuple = ()):
        where, value = list(where), list(value)
        self.connect(self.db)
        cod = self.name
        if len(where) > 0 and len(where) == len(value):
            cod = cod + f" WHERE {self.fortext(" AND ", " = ", where, value)}"
        listen = self.execute(self.db, F"SELECT {column} FROM {cod}", True)
        if listen == None:
            return "NULL"
        return listen
    def insertData(self, columns: tuple=(), values:tuple=()):
        if columns != ():
            self.columns, self.values = columns, values
        if len(self.columns) == len(self.values): 
            self.execute(self.db, F"INSERT INTO {self.name} {str(self.columns)} VALUES {str(self.values)}")
if __name__ == "__main__":
    oi = table("produtos", "Products")
    print(oi.getData())