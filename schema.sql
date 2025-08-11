DROP TABLE IF EXISTS donors;
DROP TABLE IF EXISTS receivers;

CREATE TABLE donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    sex TEXT,
    age INTEGER,
    height REAL,
    weight REAL,
    blood_type TEXT,
    illness TEXT,
    allergy TEXT,
    phone TEXT,
    city TEXT
);

CREATE TABLE receivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    sex TEXT,
    age INTEGER,
    height REAL,
    weight REAL,
    blood_type TEXT,
    illness TEXT,
    allergy TEXT,
    phone TEXT,
    city TEXT
);
