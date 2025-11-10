from connect import connect
class table(connect):
    def __init__(self, db : str, name : str, columns : tuple = ("", ), values: tuple = ("", )):
        super().__init__()
        self.db = db
        self.name = name
        self.columns= columns
        self.values = values
        self.createPermission = False
        if columns[0] != "" and values[0] != "":
            self.createPermission = True
    def create(self):
        if len(self.columns) == len(self.values) and self.db != "" and self.name != "" and self.createPermission:
            rows = []
            for i, j in enumerate(self.columns):
                rows.append(f"{self.columns[i]} {self.values[i]}")
            rows = ", ".join(rows)
            self.connect(self.db)
            self.execute(self.db, f"CREATE TABLE IF NOT EXISTS {self.name}({rows})")
            self.desconnect(self.db)
    def listcolumns(self):
        return self.columns
    def getData(self, column: tuple= ("*", ), where:tuple = (), value: tuple= ()):
        column, where, value = list(column), list(where), list(value)
        self.connect(self.db)
        cod = self.name
        if len(where) > 0 and len(where) == len(value):
            cod = cod + f" WHERE {where[0]} = {value[0]}"; del where[0], value[0]
            for whe, val in zip(where, value):
                    cod = cod + f" AND {whe} = {val}"
        columns = column[0]
        del column[0]
        for i in column:
            columns = columns + f", {i}"
        listen = self.execute(self.db, F"SELECT {columns} FROM {cod}", True)
        if listen == None:
            return "NULL"
        return listen
    def insertData(self, columns: tuple=(), values:tuple=()):
        if columns != ():
            self.columns, self.values = columns, values
        if len(self.columns) == len(self.values): 
            self.execute(self.db, F"INSERT INTO {self.name} {str(self.columns)} VALUES {str(self.values)}")
if __name__ == "__main__":
    oi = table("", "Conts")
    print(oi.getData())