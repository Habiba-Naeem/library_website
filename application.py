import os
import requests
import json
from flask import Flask, session, render_template, request, url_for, redirect, flash, jsonify, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

DATABASE_URL="postgres://ujmpxepmokdkjt:ab59d41af76430769acf21930d342f34fdeb027561b628c85ef2ba1d5c82b848@ec2-3-229-210-93.compute-1.amazonaws.com:5432/d3dn2fsroc788b"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():

    #get the username currently logged in
    username =  session.get('username')

    #if no user is logged in
    if username == None:
        return render_template("index.html", index = "index")
    
    #if a user is logged in then redirect to the books page
    else:
        return redirect(url_for('books'))

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user
    session.clear()

    #
    if request.method == "POST":
        email =  request.form.get("email")
        password = request.form.get("password")

        #check if all fields are filled
        if email == None or password == None :
            flash("Please fill all fields.", "danger")
        else:
            #select data
            data = db.execute("SELECT * FROM users WHERE email = :email AND password = :password", 
                                                                {"email":email, 
                                                                "password":password}).fetchone()
        #if nothing is selected from the database
        if data == None:
            flash("Email or password is not correct.", "danger")
        else:
            #remember the user
            session["id"] = data.id
            session["username"] = data.username
            return redirect(url_for('books'))
    #if request is get
    return render_template("login.html", login = "login")

@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("username")
    email =  request.form.get("email")
    password = request.form.get("password")
    confirm = request.form.get("confirm-password")
    data = db.execute("SELECT username, email FROM users WHERE username = :username AND email = :email",
                                                                              {"username":username,
                                                                                "email":email} ).fetchone()
    if request.method == "POST":

        if password != confirm:
            flash("Passwords do not match", "danger")

        if username == "" or email == "" or password == "" or confirm == "":
            flash("Please fill all fields", "danger")

        if data != None:
            flash("Username or email already exists", "danger")

        if data == None and password == confirm:
            db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)", 
                                                                                        {"username": username,
                                                                                        "email": email,
                                                                                        "password": password})
            db.commit()
            session["username"] = username
            print(f"{username}")
            id = db.execute("SELECT id FROM users WHERE username = :username", {"username":username})
            session["id"] = id
            #take to books.html and render the list of books
            return redirect(url_for('books'))

        return redirect(url_for('register'))

    return render_template("register.html", register = "register")


@app.route("/logout")
def logout():
    #forget user
    session.clear()
    return redirect(url_for('index'))



 @app.route("/register", methods=["GET", "POST"])
 def register():
    username = request.form.get("username")
    email =  request.form.get("email")
    password = request.form.get("password")
    confirm = request.form.get("confirm-password")
    data = db.execute("SELECT username, email FROM users WHERE username = :username AND email = :email",
                                                               {"username":username,
                                                                "email":email} ).fetchone()
    if request.method == "POST":
         
        if password != confirm:
            flash("Passwords do not match", "danger")
         
        if username == "" or email == "" or password == "" or confirm == "":
            flash("Please fill all fields", "danger")

        if data != None:
            flash("Username or email already exists", "danger")

        if data == None and password == confirm:
            db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)", 
                                                          {"username": username,
                                                                                                        "email": email,
                                                                                                        "password": password})
            db.commit()
            session["username"] = username
            print(f"{username}")
            id = db.execute("SELECT id FROM users WHERE username = :username", {"username":username})
            session["id"] = id
            #take to books.html and render the list of books
            return redirect(url_for('books'))

        return redirect(url_for('register'))

    return render_template("register.html", register = "register")
    """print(f"{data}, {data}")
    #Post request
    if request.method == "POST":
        
        #if any field is null
        if username == "" or email == "" or password == "" or confirm == "":
            flash("Please fill all fields.", "danger")
            return redirect(url_for('register'))

        if data == None:
            print("heloo")
            if password == confirm:
                    db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)", 
                                                                                        {"username": username,
                                                                                        "email": email,
                                                                                        "password": password})
                    db.commit()
                    session["username"] = username
                    print(f"{username}")
                    id = db.execute("SELECT id FROM users WHERE username = :username", {"username":username})
                    session["id"] = id
                    #take to books.html and render the list of books
                    return redirect(url_for('books'))
            else:
                flash("Passwords do not match", "danger")
        else:
            flash("Username or E-mail alreay exists. Please enter a different username or E-mail.", "danger")
            return redirect(url_for('register'))
    elif request.method == "GET":
        return render_template("register.html", register = "register")"""




@app.route("/books", methods=["GET", "POST"])
def books():
    #display all the books
    books = db.execute("SELECT * FROM books").fetchall()
    username =  session.get('username')
    print(f"{username}")
    
    if username == None:
        return redirect(url_for('index'))

    if request.method == "POST":
        #search for text in the searchbar
        search = request.form.get("searchbar")
        print(f"{search}")

        #redirect to books if searchbar is empty
        if search == "":
            return redirect(url_for("books"))
        
        #select and display data 
        else:
            books = db.execute("SELECT * FROM books WHERE isbn LIKE '%"+search+"%' OR title LIKE '%"+search+"%' OR author LIKE '%"+search+"%'")
            if books ==  None:
                flash("Sorry. The book you searched for does not exist.", "info")
            return render_template("books.html", books = books, username = username )
    
    #if request is get
    return render_template("books.html", books = books, username = username)


@app.route("/bookpage/<string:isbn>", methods=["GET", "POST"])
def bookpage(isbn):

    username =  session.get('username')
    id = session.get('id')
    print(f"{username}, {id}")
    if username == None:
        return redirect(url_for('index'))

    print(f"{isbn}")
    
    #select data on the basis of isbn from books.html
    data = db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
    if data == None:
        redirect(url_for('books'))
    
    #make api request
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "Ydcqyr9QO7Uj623vRgYS5A", "isbns": isbn})
    api=res.json()

    #average and total ratings given to a book
    average_rating = res.json()['books'][0]['average_rating']
    work_ratings_count = res.json()['books'][0]['work_ratings_count'] 

    #display reviews and ratings.
    display = db.execute("SELECT * FROM reviews WHERE isbn = :isbn ", {"isbn":isbn}).fetchall()

    
    review = request.form.get("review")
    rating = request.form.get("rating")
    print(f"{review},{rating}")

    #if user tries to submit review and rating
    if request.method == "POST":
       
        reviews = db.execute("SELECT id, username FROM reviews WHERE isbn = :isbn AND id = :id AND username = :username", 
                                                {"isbn":isbn, 
                                                "id":id,
                                                "username":username}).fetchone()
        if reviews == None:
            db.execute("INSERT INTO reviews ( review, rating, id, isbn, username ) VALUES ( :review, :rating, :id, :isbn, :username)", {
                                                                                "review":review,    
                                                                                "rating":rating,                                                                            "rating":rating,
                                                                                "id":id,
                                                                                "isbn":isbn,
                                                                                "username":username})
            print("worked")
            db.commit()
            return redirect(url_for('bookpage', isbn = isbn))
            
        elif reviews.id != id:
            db.execute("INSERT INTO reviews ( review, rating, id, isbn, username ) VALUES ( :review, :rating, :id, :isbn, :username)", {
                                                                                "review":review,    
                                                                                "rating":rating,                                                                            "rating":rating,
                                                                                "id":id,
                                                                                "isbn":isbn,
                                                                                "username":username
                                                                                })
            print("worked")
            db.commit()
            return redirect(url_for('bookpage', isbn = isbn))
                           
        else:
            flash("You have already given the review for this book", "danger")

    #if get request
    return render_template("bookpage.html",books = "c", data = data, average_rating = average_rating , 
                            work_ratings_count = work_ratings_count,display = display,  username = username)




@app.route("/api/<isbn>")
def api(isbn):

    data = db.execute("SELECT * FROM books WHERE isbn = :isbn",{"isbn":isbn}).fetchone()
    if data == None:
        abort(404)
    
    #make api request
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "Ydcqyr9QO7Uj623vRgYS5A", "isbns": isbn})
    api=res.json()

    #average and total ratings given to a book
    average_rating = res.json()['books'][0]['average_rating']
    work_ratings_count = res.json()['books'][0]['work_ratings_count'] 

    return jsonify({
        "title": data.title,
        "author": data.author,
        "year": data.year,
        "isbn": data.isbn,
        "review_count": work_ratings_count,
        "average_score": average_rating
    })

if __name__ == '__main__':
    app.run(debug=True)
