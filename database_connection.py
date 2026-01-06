import sqlite3


class DatabaseConnection:

    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    @staticmethod
    def dict_factory(cursor, row):
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = self.dict_factory
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.close()
