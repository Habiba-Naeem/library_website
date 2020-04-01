import os, csv
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#DATABASE_URL="postgres://ujmpxepmokdkjt:ab59d41af76430769acf21930d342f34fdeb027561b628c85ef2ba1d5c82b848@ec2-3-229-210-93.compute-1.amazonaws.com:5432/d3dn2fsroc788b"

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
#    raise RuntimeError("DATABASE_URL is not set")
# database engine object from SQLAlchemy that manages connections to the database
# DATABASE_URL is an environment variable that indicates where the database lives
#engine = create_engine(os.getenv("DATABASE_URL")) 

# create a 'scoped session' that ensures different users' interactions with the
# database are kept separate
#db = scoped_session(sessionmaker(bind=engine))

def main():
    #db.execute("INSERT INTO users (username, email, password) VALUES ('habiba', 'h@g', '12')")
    #db.commit()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "R4AMQUSRImOSejZpMduGVQ", "isbns": "9781632168146"})
    print(res.json())
if __name__ == "__main__":
    main()