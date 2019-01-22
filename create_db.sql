CREATE TABLE users(
   ID 			        SERIAL  PRIMARY KEY,
   USERNAME             TEXT    UNIQUE        NOT NULL,
   PASSWORD_HASH        TEXT    UNIQUE        NOT NULL
);

CREATE TABLE books(
   ID 			           SERIAL  PRIMARY KEY,
   TITLE                   TEXT    NOT NULL,
   AUTHOR                  TEXT    NOT NULL,
   PUBLICATION_YEAR        TEXT    NOT NULL,
   ISBN                    TEXT    UNIQUE        NOT NULL
);

CREATE TABLE reviews(
   ID 			           SERIAL     PRIMARY KEY ,
   BODY                    TEXT       NOT NULL,
   SCORE                   INTEGER    NOT NULL      CHECK (SCORE > 0)       CHECK (SCORE < 6),
   BOOK_ID                 INTEGER    NOT NULL      REFERENCES books(ID),
   USER_ID                 INTEGER    NOT NULL      REFERENCES users(ID)
);

CREATE INDEX index_isbn ON books (isbn);