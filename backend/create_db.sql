CREATE TABLE members (
    id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    account TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);