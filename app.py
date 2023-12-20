from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from knapsack import main

DATABASE = 'database.db'

app = Flask(__name__)

# トップ画面
@app.route('/')
def index():
    con = sqlite3.connect(DATABASE)
    # db_items = [(1列目, 2列目, 3列目), (1列目, 2列目, 3列目), ...]
    db_items = con.execute('SELECT * FROM items').fetchall()
    items = []
    for row in db_items:
        items.append({'name': row[0], 'price': row[1], 'importance': row[2]})

    budget = con.execute('SELECT * FROM budget_data').fetchall()
    if budget!=[]: budget = budget[0][0]
    total = con.execute('SELECT * FROM total_data').fetchall()
    if total!=[]: total = total[0][0]
    satisfy = con.execute('SELECT * FROM satisfy_data').fetchall()
    if satisfy!=[]: satisfy = satisfy[0][0]

    db_best_items = con.execute('SELECT * FROM best_items').fetchall()
    best_items = []
    for row in db_best_items:
        best_items.append({'name': row[0], 'price': row[1], 'importance': row[2]})

    return render_template(
        'index.html',
        items=items, budget=budget, best_items=best_items, total=total, satisfy=satisfy
        )

# 商品登録画面
@app.route('/form')
def form():
    return render_template('form.html')
# 登録した商品をデータベースに保存し、トップ画面に表示
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    price = request.form['price']
    importance = request.form['importance']

    con = sqlite3.connect(DATABASE)
    con.execute('INSERT INTO items VALUES(?, ?, ?)',
              [name, price, importance]  )
    con.commit()
    con.close()
    return redirect(url_for('index'))

# 商品削除画面
@app.route('/delete_form')
def delete_form():
    return render_template('delete_form.html')
# 入力された商品をデータベースから削除
@app.route('/delete_item', methods=['POST'])
def delete_item():
    name = request.form['name']
    con = sqlite3.connect(DATABASE)
    con.execute('DELETE FROM items WHERE name==?', [name])
    con.commit()
    con.close()
    return redirect(url_for('index'))

# 予算登録画面
@app.route('/budget_form')
def budget_form():
    return render_template('budget_form.html')
# 登録した予算をデータベースに保存し、トップ画面に表示
@app.route('/set_budget', methods=['POST'])
def set_budget():
    budget = request.form['budget']
    db.delete_budget()
    db.create_budget()
    con = sqlite3.connect(DATABASE)
    con.execute('INSERT INTO budget_data VALUES(?)', [budget])
    con.commit()
    con.close()
    return redirect(url_for('index'))

# 最適化を行い、トップ画面に表示
@app.route('/calculate')
def calculate():
    db.delete_besttable()
    db.create_besttable()
    db.delete_total()
    db.create_total()
    db.delete_satisfy()
    db.create_satisfy()
    con = sqlite3.connect(DATABASE)
    db_items = con.execute('SELECT * FROM items').fetchall() 
    budget = con.execute('SELECT * FROM budget_data').fetchone()[0]
    names = []
    costs = []
    importances = []
    for item in db_items:
        names.append(item[0])
        costs.append(item[1])
        importances.append(item[2])
    best_solution, total, satisfy = main(names, costs, importances, budget)
    best_items = [con.execute('SELECT * FROM items WHERE name==?', [solution]).fetchone() for solution in best_solution]
    for row in best_items:
        name, price, importance = row[0], row[1], row[2]
        con.execute('INSERT INTO best_items VALUES(?, ?, ?)', [name, price, importance])

    con.execute('INSERT INTO total_data VALUES(?)', [int(total)])
    con.execute('INSERT INTO satisfy_data VALUES(?)', [int(satisfy)])
    con.commit()
    con.close()

    return redirect(url_for('index'))

# データベースを初期化して、トップ画面に戻る
@app.route('/reset')
def reset():
    db.delete_table()
    db.create_table()
    db.delete_budget()
    db.create_budget()
    db.delete_besttable()
    db.create_besttable()
    db.delete_total()
    db.create_total()
    db.delete_satisfy()
    db.create_satisfy()
    return redirect(url_for('index'))


if __name__ == "__main__":

    import db

    db.delete_table()
    db.create_table()
    db.delete_budget()
    db.create_budget()
    db.delete_besttable()
    db.create_besttable()
    db.delete_total()
    db.create_total()
    db.delete_satisfy()
    db.create_satisfy()

    app.run(host="0.0.0.0", port=1202, debug=True)
