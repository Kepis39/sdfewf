CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    mobile_phone VARCHAR(20),
    home_phone VARCHAR(20),
    birth_date DATE,
    gender VARCHAR(10),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS passports (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    passport_series_number VARCHAR(20) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    birth_date DATE,
    issue_date DATE,
    department_code VARCHAR(10),
    issued_by TEXT,
    birth_address TEXT,
    actual_address TEXT,
    has_foreign_passport BOOLEAN DEFAULT FALSE
);
