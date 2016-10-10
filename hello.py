from flask import Flask, redirect, url_for, request, render_template
from werkzeug import secure_filename
import sqlite3 as sql
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "student.db")
con  = sql.connect(db_path)
print(con)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/upload'
@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' %name

@app.route('/blog/<int:postID>')
def show_blog(postID):
    return 'Blog Number %d '%postID

@app.route('/rev/<float:revNo>')
def revision(revNo):
    return 'Revision Number %f'%revNo

@app.route('/flask/')
def hello_flask():
    return 'Hello Flask'

@app.route('/admin')
def hello_admin():
    return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
    return 'Hello %s as Guest' %guest

@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest',guest='ayush'))

@app.route('/success/<name>')
def success(name):
    return render_template('success.html',name=name)

@app.route('/login', methods=['POST', 'GET'])
def login():
    print(request)
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success',name=user))
    else:
        user = request.args.get('nm')
        print(user)
        return redirect(url_for('success',name=user))

@app.route('/result', methods = ['POST','GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template('result.html',result=result)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/uploader', methods=['POST','GET'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'

@app.route('/enternew')
def new_student():
    return render_template('student.html')

@app.route('/addrec',methods=['POST','GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']
            print(con)
            print(nm,addr,city,pin)
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin))

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
    # con = sql.connect('database.db')
    print(con)
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute('select * from students')
    rows = cur.fetchall()
    return render_template('list.html',rows=rows)
if __name__ == '__main__':
    # app.debug = True
    app.run()
    # app.run(debug = True)
