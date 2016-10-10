from flask import Flask, redirect, url_for, request, render_template
from werkzeug import secure_filename
import sqlite3 as sql
import os.path
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = BASE_DIR + '/upload'
db_path = os.path.join(BASE_DIR, "myshopup.db")
con  = sql.connect(db_path)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addrec',methods=['GET','POST'])
def addrec():
    if request.method == 'POST':
        try:
            name = request.form['name']
            price = int(request.form['price'])
            inventory = int(request.form['inventory'])
            f = request.files['file']
            filename = secure_filename(f.filename)
            print(type(price))
            print(name,price,inventory,filename)
            f.save(filename)
            cur = con.cursor()
            cur.execute("INSERT INTO sellerPanel (name,price,inventory,image) VALUES (?,?,?,?)",(name,price,inventory,filename))

            con.commit()
            msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
        finally:
            return render_template('result.html',msg=msg)
            con.close()

@app.route('/list')
def list():
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('select * from sellerPanel')
    rows = cur.fetchall()
    return render_template('list.html',rows=rows)

@app.route('/product')
def product():
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('select * from sellerPanel')
    rows = cur.fetchall()
    # print(rows)
    return render_template('product.html',products=rows)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout', methods=['GET','POST'])
def checkout():
    if request.method == 'POST':
        print(request.form.to_dict())
        d = request.form.to_dict()
        print(len(d))
        count = len(d)/4
        for i in range(count):
            for key in sorted(d.iterkeys()):
                print "%s: %s" % (key, d[key])
                if key == 'item['+str(i)+'][name]':
                    name = d[key]
                elif key == 'item['+str(i)+'][price]':
                    price = int(d[key])
                elif key == 'item['+str(i)+'][quantity]':
                    quantity = int(d[key])
                elif key == 'item['+str(i)+'][product_id]':
                    product_id = int(d[key])
            cur = con.cursor()
            cur.execute('select * from sellerPanel where ID =?',[product_id])
            stock = cur.fetchone()
            print(stock)
            remaining_stock = stock[3] - quantity
            cur.execute("INSERT INTO orders (name,price,quantity,product_id) VALUES (?,?,?,?)",(name,price,quantity,product_id))
            cur.execute("UPDATE sellerPanel SET inventory =(?) WHERE ID=(?)",[remaining_stock,product_id])
            con.commit()
            return redirect(url_for('order'))

@app.route('/order')
def order():
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute('select * from orders')
    rows = cur.fetchall()
    # print(rows)
    return render_template('order.html',orders=rows)
if __name__ == '__main__':
    # app.debug = True
    app.run()
    # app.run(debug = True)
