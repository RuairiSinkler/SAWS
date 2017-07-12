
from DatabaseManagement import *

def main() :
    manager = DatabaseManager("test.db")
    manager.insert("test_table", ["test1", "test2", "test3"])

if __name__ == "__main__":
    main()
