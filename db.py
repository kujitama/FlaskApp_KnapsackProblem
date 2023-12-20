import sqlite3

DATABASE = "database.db"

'''
items : 登録した商品
budget_data : 予算
best_items : 最適化された商品の組み合わせ
total_data : 選ばれた商品の合計金額
satisfy_data : 選ばれた商品の重要度総和
'''

def create_table():
    con = sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS items (name, price, importance)")
    con.close

def delete_table():
    con = sqlite3.connect(DATABASE)
    con.execute('DROP TABLE IF EXISTS items')
    con.close

def create_budget():
    con = sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS budget_data (budget)")
    con.close

def delete_budget():
    con = sqlite3.connect(DATABASE)
    con.execute('DROP TABLE IF EXISTS budget_data')
    con.close

def create_besttable():
    con = sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS best_items (name, price, importance)")
    con.close

def delete_besttable():
    con = sqlite3.connect(DATABASE)
    con.execute('DROP TABLE IF EXISTS best_items')
    con.close

def create_total():
    con = sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS total_data (total)")
    con.close

def delete_total():
    con = sqlite3.connect(DATABASE)
    con.execute('DROP TABLE IF EXISTS total_data')
    con.close

def create_satisfy():
    con = sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS satisfy_data (satisfy)")
    con.close

def delete_satisfy():
    con = sqlite3.connect(DATABASE)
    con.execute('DROP TABLE IF EXISTS satisfy_data')
    con.close