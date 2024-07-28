CREATE TABLE IF NOT EXISTS training_data(
    id SERIAL PRIMARY KEY,
    integrand TEXT NOT NULL UNIQUE,
    integral TEXT,
    success BOOLEAN NOT NULL
);