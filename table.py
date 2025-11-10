from connect import connect
class table(connect):
    def __init__(self, db : str, name : str, columns : tuple = ("", ), values: tuple = ("", )):
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
    def data(self, column: tuple= ("*", ), where:tuple = (), value: tuple= ()):
        self.connect(self.db)
        cod = self.name
        if len(where) > 0 and len(where) == len(value):
            for i, j in enumerate(where):
                if i == 0:
                    cod =  cod + f" WHERE {where[i]} = {value[i]}"
                else:
                    cod = cod + f" AND {where[i]} = {value[i]}"
        columns = ""
        for i, j in enumerate(column):
            if i == 0:
                columns = j
            else:
                columns = columns + f", {j}"
        temp = self.execute(self.db, F"SELECT {columns} FROM {cod}")
        listen = []
        for i in temp:
            listen.append(i)
        self.desconnect(self.db)
        return listen