import os, csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL="postgres://ujmpxepmokdkjt:ab59d41af76430769acf21930d342f34fdeb027561b628c85ef2ba1d5c82b848@ec2-3-229-210-93.compute-1.amazonaws.com:5432/d3dn2fsroc788b"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
# database engine object from SQLAlchemy that manages connections to the database
# DATABASE_URL is an environment variable that indicates where the database lives
engine = create_engine(os.getenv("DATABASE_URL")) 

# create a 'scoped session' that ensures different users' interactions with the
# database are kept separate
db = scoped_session(sessionmaker(bind=engine))

def main():
    db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR NOT NULL UNIQUE, email VARCHAR NOT NULL UNIQUE, password VARCHAR NOT NULL)")
    print("user table")
    db.execute("CREATE TABLE reviews (review VARCHAR NOT NULL, rating INTEGER NOT NULL, isbn VARCHAR NOT NULL, user_id INTEGER NOT NULL)")
    print("review table")
    db.execute("CREATE TABLE books (isbn VARCHAR PRIMARY KEY, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year VARCHAR NOT NULL)")
    f=open("books.csv")
    reader =csv.reader(f)
    for isbn, title, author, year in reader:
        if year == "year":
            print('skipped first line')
        else:    
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn,:title,:author,:year)",
                                                                                {"isbn":isbn,
                                                                                "title":title,
                                                                                "author":author,
                                                                                "year":year})
        print(f"Added: {title}")
        
    print("done")            
    db.commit()    
if __name__ == "__main__":
    main()





