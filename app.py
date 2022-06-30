from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
db=sqlite3.connect("app.db",check_same_thread=False)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/",methods=["GET", "POST"])

def login():
    if  session:
        return redirect("/main")    
    if request.method == "POST":

        username = request.form.get("name")
        password = request.form.get("password")

        if not request.form.get("name"):
            return render_template("erorr.html",re="must provide username")


        elif not request.form.get("password"):
            return render_template("erorr.html",re="must provide password")

        rows = db.execute("SELECT * FROM users WHERE username = (?)", (username,))
        db.commit()
        for row in rows:

             if  not check_password_hash(row[2], request.form.get("password")) :
                return render_template("erorr.html",re="invalid username and/or password")


        
        rows=db.execute("SELECT id FROM users WHERE username = (?)" , (username,))
        for row in rows.fetchall():

            session["id"]=row[0]
        return redirect("/main")
        
    else:

        return render_template("login.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")            

@app.route("/register",methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")

        password=request.form.get("password")
        compass=request.form.get("confirmation")
        reuse= db.execute("SELECT username FROM  users")
        db.commit()

        for row in reuse.fetchall():
            if row[0] == username:
                return render_template("erorr.html",re="username is taken")
        if not username or not password or not compass:

            return render_template("erorr.html",re="empty input")
        elif password != compass:

            return render_template("erorr.html",re="NOT MATCH PASSWORD")        

        db.execute("INSERT INTO users(username,hash) VALUES(?,?)" ,(username,generate_password_hash(password)))
        db.commit()
        return redirect("/")
    else:

        return render_template("register.html")

@app.route("/main" , methods=["GET", "POST"])
def main():
    if request.method == "POST":
        name = request.form.get("name")
        image = request.form.get("imag")
        rating = request.form.get("rating")
        db.execute("INSERT INTO watchlist(title,rating,image,user_id) VALUES(?,?,?,?)" ,(name,rating,image,session["id"]))
        db.commit()
        return redirect("/Watchlist")

        



        
    else:
        rows=db.execute("SELECT title FROM watchlist WHERE user_id = (?)",(session["id"],)).fetchall()
        db.commit()


        return render_template("main.html",n=rows)
@app.route("/movie" ,methods=["GET", "POST"])
def f():
    if request.method == "POST":
        name = request.form.get("name")
        image = request.form.get("imag")
        rating = request.form.get("rating")
        db.execute("INSERT INTO watchlist(title,rating,image,user_id) VALUES(?,?,?,?)" ,(name,rating,image,session["id"]))
        db.commit()
        return redirect("/Watchlist")

    else:
        rows=db.execute("SELECT title FROM watchlist WHERE user_id = (?)",(session["id"],)).fetchall()
        db.commit()
       
       
        return render_template("movie.html",n=rows)

@app.route("/series",methods=["GET", "POST"])
def g():
    if request.method == "POST":
        name = request.form.get("name")
        image = request.form.get("imag")
        rating = request.form.get("rating")
        db.execute("INSERT INTO watchlist(title,rating,image,user_id) VALUES(?,?,?,?)" ,(name,rating,image,session["id"]))
        db.commit()
        return redirect("/Watchlist")
    else:
        rows=db.execute("SELECT title FROM watchlist WHERE user_id = (?)",(session["id"],)).fetchall()
        db.commit()


        return render_template("series.html",n=rows)

@app.route("/Watchlist" , methods=["GET", "POST"])
def h():
    if request.method == "POST":
        id = request.form.get("name")
        rows=db.execute("DELETE FROM watchlist WHERE id = (?)",(id,))
        db.commit()
        rows=db.execute("SELECT * FROM watchlist WHERE user_id = (?)",(session["id"],))
        db.commit()
        return render_template("Watchlist.html",row=rows.fetchall())
    else:
        rows=db.execute("SELECT * FROM watchlist WHERE user_id = (?)",(session["id"],))
        db.commit()
        return render_template("Watchlist.html",row=rows.fetchall())







