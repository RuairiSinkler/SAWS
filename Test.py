
from DatabaseManagement import *

def main() :
    ration_manager = DatabaseManager("rations.db")
    ration_manager.insert_rations("rations", ["Peak lay", 560, 400, 220, 100, 10, 20, 30, 40])

if __name__ == "__main__":
    main()
