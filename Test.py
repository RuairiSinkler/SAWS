
from DatabaseManagement import *

def main() :
    ration_manager = DatabaseManager("rations.db")
    ration_manager.insert_ration(["Minnie", 200, 360, 20, 300, 110, 30, 8, 700])

if __name__ == "__main__":
    main()
