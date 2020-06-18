'''
import csv
import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import dj_database_url

# Set up database

engine = create_engine('postgresql://ltaouqwbmilrwx:d522f1799e0f2a830c397499232bca8c5ce524a19d936ee9eb87ad51d96d3169@ec2-54-235-92-244.compute-1.amazonaws.com/d5kndisgmg8b0b')

db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    
    for isbn,title,author,year in reader:
        db.execute("INSERT INTO BOOKS (ISBN,title,author,year) VALUES (:isbn,:title,:author,:year)",
        {"isbn":isbn,"title":title,"author":author,"year":year})
        print(f"added book {isbn}")
    
    db.commit()

if __name__=="__main__":
    main()
'''

#db.execute("INSERT INTO USERS(UNAME,PSW,EMAIL) VALUES('yuvraj','12345','yuvrajthakare@gmail.com')")
#db.commit()

import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "23l14tVXIrt8anlid1DzA", "isbns": "9781632168146"})
data = res.json()
x  = data.books

print(x)