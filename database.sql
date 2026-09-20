CREATE TABLE IF NOT EXISTS credentials (
    credential_id INTEGER PRIMARY KEY,
    user_account TEXT NOT NULL UNIQUE,
    user_password BLOB NOT NULL
);

