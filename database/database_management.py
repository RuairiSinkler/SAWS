import sqlite3
from pathlib import Path


class DatabaseManager:
    def __init__(self, directory, database_name):
        self.directory = directory
        self.database_name = "{}/{}".format(directory, database_name)

    def run_sql_file(self, file_path):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        with open("{}/{}".format(self.directory, file_path)) as f:
            cursor.executescript(f.read())
        connect.commit()
        connect.close()

    def clear(self):
        self.run_sql_file("delete_rations.sql")

    def build(self):
        self.run_sql_file("rations.sql")

    def insert_weigher(self, values):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        execution = "INSERT INTO weighers VALUES (?, ?, ?)"
        cursor.execute(execution, values)
        connect.commit()

        connect.close()

    def insert_ingredient(self, values):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute("SELECT MAX(id)+1 FROM ingredients")
        ingredient_id = cursor.fetchone()[0]
        if ingredient_id is None:
            ingredient_id = 0
        values.insert(0, ingredient_id)
        execution = "INSERT INTO ingredients VALUES (?, ?, ?, ?, ?)"
        cursor.execute(execution, values)
        connect.commit()

        connect.close()


    # Specifically inserts values into the rations table
    def insert_ration(self, values):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute("SELECT MAX(id)+1 FROM rations")
        ration_id = cursor.fetchone()[0]
        if ration_id is None:
            ration_id = 0
        values.insert(0, ration_id)

        execution = "INSERT INTO rations VALUES (?, ?)"
        cursor.execute(execution, values)
        connect.commit()

        connect.close()

    def insert_house(self, values):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute("SELECT MAX(id)+1 FROM houses")
        house_id = cursor.fetchone()[0]
        if house_id is None:
            house_id = 0
        values.insert(0, house_id)
        execution = "INSERT INTO houses VALUES (?, ?)"
        cursor.execute(execution, values)
        connect.commit()

        connect.close()

    def insert_ration_ingredients(self, values):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "INSERT INTO ration_ingredients VALUES (?, ?, ?)"
        cursor.execute(execution, values)
        connect.commit()

        connect.close()

    def get_id_by_name(self, table, name):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT id FROM {} WHERE name = ?".format(table)
        cursor.execute(execution, (name, ))

        result = cursor.fetchone()
        if result is not None:
            result = result[0]

        connect.close()

        return result

    def get_ration(self, ration_id):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT * FROM rations WHERE id = ?"
        cursor.execute(execution, (ration_id,))

        result = cursor.fetchone()

        connect.close()

        return result

    def get_weigher(self, weigher_id):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT * FROM weighers WHERE id = ?"
        cursor.execute(execution, (weigher_id,))

        result = cursor.fetchone()

        connect.close()

        return result

    def get_all_rations(self):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT * FROM rations"
        cursor.execute(execution)

        result = cursor.fetchall()

        connect.close()

        return result

    def get_ration_ingredients(self, ration_id):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT ingredients.name, amount, augar_pin, weigher_id, ordering FROM ration_ingredients " \
                    "JOIN ingredients ON ingredients.id = ration_ingredients.ingredient_id " \
                    "WHERE ration_id = ?"
        cursor.execute(execution, (str(ration_id),))

        result = cursor.fetchall()

        connect.close()

        return result

    def get_all_houses(self):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT * FROM houses"
        cursor.execute(execution)

        result = cursor.fetchall()

        connect.close()

        return result