import os

from flask import Flask, session, render_template, request, url_for, redirect, flash
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
        return redirect(url_for('books', books = "books"))

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user
    session.clear()

    #
    if request.method == "POST":
        email =  request.form.get("email")
        password = request.form.get("password")

        #check if all fields are filled
        if email == "" or password == "" :
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
            return render_template("books.html", books = "books", username = session["username"])
    #if request is get
    return render_template("login.html", login = "login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/register", methods=["GET", "POST"])
def register():
    #Post request
    if request.method == "POST":
        username = request.form.get("username")
        email =  request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm-password")
        data = db.execute("SELECT username, email FROM users").fetchall()
        
        #if any field is null
        if username == "" or email == "" or password == "" or confirm == "":
             return redirect(url_for('register', register = "register", message = "Please fill all fields."))
        
        #loop through the fetched data
        for select in data:

            #match username and email
            if select.username == username or select.email == email:
                return redirect(url_for('register', register = "register", message = "Username or E-mail alreay exists. Please enter a different username or E-mail "))
            
            
            else:

                #match the passwords
                if password == confirm:
                    db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)", 
                                                                                        {"username": username,
                                                                                        "email": email,
                                                                                        "password": password})
                    db.commit()
                    
                    #take to books.html and render the list of books
                    return redirect(url_for('books', username = username))
                
                else:
                    return redirect(url_for('register', register = "register", message = "Passwords do not match"))
    
    #if get request; do following
    else:    
        return render_template("register.html", register = "register")



@app.route("/books", methods=["GET", "POST"])
def books():
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("books.html", books = books )
    #if request.method == "POST":
        #search = request.form.get("searchbar")
        #print(f"{search}")
        #if search == "":
        #    return render_template("books.html", books = books )
        #books = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn OR title LIKE :title OR author LIKE :author ", 
        #                                                                               {"isbn":search},
        #                                                                               {"title":search},
        #                                                                                {"author":search}).fetchall()
        #return render_template("books.html", books = books )
        #isbn = db.execute("SELECT isbn FROM books WHERE isbn = :isbn ", {"isbn":search}).fetchall()
        #title = db.execute("SELECT title FROM books WHERE title = :title ", {"title":search}).fetchall()
        #author = db.execute("SELECT author FROM books WHERE author = :author ", {"author":search}).fetchall()

    


if __name__ == '__main__':
    app.run(debug=True)
