import sqlite3
from pathlib import Path


class DatabaseManager:
    def __init__(self, database_name):
        self.database_name = "./{}".format(database_name)

    def run_sql_file(self, file_path):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        with open("./{}".format(file_path)) as f:
            cursor.executescript(f.read())
        connect.commit()
        connect.close()

    def clear(self):
        self.run_sql_file("delete_rations.sql")

    def build(self):
        self.run_sql_file("rations.sql")

    def insert_ingredient(self, values):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute("SELECT MAX(id)+1 FROM ingredients")
        ingredient_id = cursor.fetchone()[0]
        if ingredient_id is None:
            ingredient_id = 0
        values.insert(0, ingredient_id)
        execution = "INSERT INTO ingredients VALUES (?, ?, ?, ?)"
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

        result = cursor.fetchall()[0][0]

        connect.close()

        return result

    def update_ration(self, values):
        # Perform Validation on the values inserted to go into the rations database
        all_ok = isinstance(values[1], str) and values[1]
        for i in range(2, 10):
            if (i == 8):
                all_ok = all_ok and isinstance(values[i], float)
            else:
                all_ok = all_ok and isinstance(values[i], int)

        # If all is ok then insert otherwise raise an exception
        if all_ok:
            ration_id = values.pop(0)
            values.append(ration_id)

            connect = sqlite3.connect(self.database_name)
            cursor = connect.cursor()

            execution = "UPDATE rations SET ration_name = ?, " \
                        "wheat = ?, barley = ?, soya = ?, " \
                        "limestone = ?, soya_oil = ?, arbocell = ?," \
                        "methionine = ?, premix = ? " \
                        "WHERE ration_id = ?"

            cursor.execute(execution, values)
            connect.commit()

            connect.close()
        else:
            raise (IOError)

    def get_ration(self, ration_id):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT * FROM rations WHERE id = ?"
        cursor.execute(execution, (ration_id,))

        result = cursor.fetchall()[0]

        connect.close()

        return result

    def get_all_rations(self):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT *  FROM rations"
        cursor.execute(execution)

        result = cursor.fetchall()

        connect.close()

        return result

    def get_ration_ingredients(self, ration_id):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT ingredients.name, amount, weigher, ordering FROM ration_ingredients " \
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