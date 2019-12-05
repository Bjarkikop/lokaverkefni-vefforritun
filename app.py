from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
#import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = "epli"

# https://pythonspot.com/login-authentication-with-flask/


@app.route('/', methods=["GET", "POST"])
def login():
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='2106002560', password='mypassword', database='2106002560_nam')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users")    
    users = cur.fetchall()
    data = cur.execute("Select * from news")
    data = cur.fetchall()  
    msg=""
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        session["loggedin"] = False
        username = request.form['username']
        password = request.form['password']
        cur.execute("SELECT * FROM users WHERE user = %s AND pass = %s", (username, password))
        account = cur.fetchone()
        if account:
            if account[2] == "a":
                session["loggedin"] = True
                session["username"] = request.form["username"]
                return render_template('admin.html', data=data)
            else:
                session["loggedin"] = True
                session["username"] = request.form["username"]
                
                return render_template('news.html')
        else:
            msg = "Rangt pass eða user"
    
    return render_template('index.html', msg="", data=data)

@app.route('/logout')
def logout():
    if session['loggedin'] != False:
        session["loggedin"] = False
        return '<h1>Þú hefur loggað þig út</h1> <a href="/">Heim</a>'
    else:
        return '<h1>Þú ert ekki loggaður inn</h1> <a href="/">Heim</a>'


@app.route("/newpost", methods=["GET", "POST"])
def new_post():
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='2106002560', password='mypassword', database='2106002560_nam')
    session["loggedin"] = True
    if request.method == "POST":
        titill = request.form["title"]
        texti = request.form["article"]
        user = session["username"]
        cur = conn.cursor()
        cur.execute("insert into news(title, news, user_id) values(%s, %s, %s)", (titill, texti, user))
        conn.commit()
    return login()
    

@app.route('/SignUp', methods=["GET", "POST"])
def signup():
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='2106002560', password='mypassword', database='2106002560_nam')

    cur = conn.cursor()
    cur.execute("SELECT * FROM Users")    
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur.execute("INSERT INTO Users(user, pass) values(%s, %s)", (username, password)) 
        conn.commit()
        return login()
    return render_template("signUp.html")

@app.route('/delete_article', methods=["GET", "POST"])
def delete():
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='2106002560', password='mypassword', database='2106002560_nam')
    session["loggedin"] = True
    if request.method == "POST":
        titill = request.form["title"]
        cur = conn.cursor()
        cur.execute('DELETE FROM news WHERE title = %s', titill)
        conn.commit()
        return '<h1>Frétt hefur verið deletuð</h1> <a href="/">Heim</a>'

@app.route('/update_article', methods=["GET", "POST"])
def update():
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='2106002560', password='mypassword', database='2106002560_nam')
    session["loggedin"] = True
    if request.method == "POST":
        titill = request.form["title"]
        texti = request.form["article"]
        cur = conn.cursor()
        cur.execute('UPDATE news SET news=%s WHERE title=%s', (texti, titill))
        conn.commit()
        return '<h1>Frétt hefur verið updateuð</h1> <a href="/">Heim</a>'

@app.errorhandler(404)
def error404(error):
	return '<h1>Þessi síða er ekki til</h1> <a href="/">Heim</a>', 404


if __name__ == "__main__":
	app.run(debug=True)
	