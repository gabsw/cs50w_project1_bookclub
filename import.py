import csv
import os
from tqdm import tqdm

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def main():
    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))

    f = open("books.csv")
    reader = csv.reader(f)
    # skips the header
    next(reader)
    for isbn, title, author, year in tqdm(reader, unit=" inserts"):
        db.execute("INSERT INTO books (title, author, publication_year, isbn) "
                   "VALUES (:title, :author, :publication_year, :isbn)",
                   {"title": title, "author": author, "publication_year": year, "isbn": isbn})
    db.commit()


if __name__ == "__main__":
    main()
