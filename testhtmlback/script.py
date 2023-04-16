import gspread
sa = gspread.service_account()
sh = sa.open("BOOK")
wks = sh.worksheet("database")
print(wks.acell('E9').value)