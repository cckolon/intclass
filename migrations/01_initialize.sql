CREATE TABLE IF NOT EXISTS training_data(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                integrand TEXT NOT NULL UNIQUE,
                                integral TEXT,
                                success BOOLEAN NOT NULL)