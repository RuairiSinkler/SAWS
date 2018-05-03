import ExcelManagement as ex

book = ex.WorksheetManager("./", "test")
print(book.find("Time Run"))