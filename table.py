import connect
class table(connect):
    def __init__(self, db : str, name : str, columns : tuple, values: tuple):
        self.db = db
        self.name = name
        self.columns= columns
        self.values = values
    def create(self):
        if len(self.columns) == len(self.values) and self.db != "" and self.name != "":
            rows = []
            for i, j in enumerate(self.columns):
                rows.append(f"{self.columns[i]} {self.values[i]}")
            rows = ", ".join(rows)
            self.connect(self.db)
            self.execute(self.db, f"CREATE TABLE IF NOT EXISTS {self.name}({rows})")
            self.desconnect(self.db)