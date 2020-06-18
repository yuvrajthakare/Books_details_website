import os
from flask import Flask, session,render_template,request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import dj_database_url
import requests

# Parse database configuration from $DATABASE_URL
app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine('postgresql://ltaouqwbmilrwx:d522f1799e0f2a830c397499232bca8c5ce524a19d936ee9eb87ad51d96d3169@ec2-54-235-92-244.compute-1.amazonaws.com/d5kndisgmg8b0b')
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def start():
    return render_template("login.html")

@app.route("/login",methods=["POST"])
def login():
    user = None
    uname=request.form.get("uname")
    psw=request.form.get("psw")
    user = db.execute("select * from users where uname=:uname and psw=:psw",{"uname":uname,"psw":psw}).fetchone()
    if user==None:
        return("Invalid Username or Password ")
    else:
        return render_template("index.html",user=user)

@app.route("/create")
def create():
    return render_template("signup.html")

@app.route("/signup",methods=["POST"])
def signup():
    user = None
    name = request.form.get("uname")
    mail = request.form.get("email")
    pasw = request.form.get("psw")
    psw_repeat = request.form.get("psw-repeat")
    uname =  db.execute("select * from users where uname=:name",{"name":name}).fetchone()
    email =  db.execute("select * from users where email=:mail",{"mail":mail}).fetchone()
    
    if uname!=None:
        return("username not available...Already exists")
    elif len(pasw)<8:
        return("Password length too small\n minimum 8 characters")
    elif email!=None:
        return("Cannot use this Email....!!\n Email_Id already exists")
    elif pasw!=psw_repeat:
        return("Password deosn't match")
    else:
        db.execute("insert into users(uname,psw,email) values(:name,:pasw,:mail)",{"name":name,"pasw":pasw,"mail":mail})
        db.commit()
        return render_template("login.html")


@app.route("/index",methods=["POST"])
def index():
    books = db.execute("select * from books order by title").fetchall()
    return render_template("index.html",books=books)

@app.route("/search/<int:user_id>" , methods=["POST"])
def search(user_id):
    book=None
    name=request.form.get("name")
    book =db.execute("select * from books where title=:name",{"name":name}).fetchone()
    if book is None:
        book_id =request.form.get("book_id")
        book =db.execute("select * from books where id=:book_id",{"book_id":book_id}).fetchone()
    '''
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "23l14tVXIrt8anlid1DzA", "isbns": book.isbn})
    if res.status_code != 200:
        raise Exception("ERROR! API request unsuccessful.")
    data = res.json()
    total_ratings = data[books][work_ratings_count]
    avg_rating= data[books][average_rating]  
    '''
    reviews=db.execute("select * from reviews where book_id=:book_id",{"book_id":book.id}).fetchall()
    user=db.execute("select * from users where id=:user_id",{"user_id":user_id}).fetchone()
    return render_template("search.html",book=book,reviews=reviews,user=user)


@app.route("/comment/<int:user_id>/<int:book_id>",methods=["POST"])
def comment(user_id,book_id):
    comment=request.form.get("comment")
    db.execute("insert into reviews values(:user_id,:book_id,:comment)",{"user_id":user_id,"book_id":book_id,"comment":comment})
   
    user=db.execute("select * from users where id=:user_id",{"user_id":user_id}).fetchone()
    book =db.execute("select * from books where id=:book_id",{"book_id":book_id}).fetchone()
    reviews = db.execute("select * from reviews where book_id=:book_id ",{"book_id":book.id}).fetchall()
    db.commit()
    '''
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "23l14tVXIrt8anlid1DzA", "isbns": book.isbn})
    if res.status_code != 200:
        raise Exception("ERROR! API request unsuccessful.")
    data = res.json()
    total_ratings = data[books][work_ratings_count]
    avg_rating= data[books][average_rating]  
    '''
    return render_template("search.html",book=book,reviews=reviews,user=user)

