sqlite3 users.db "CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, token TEXT, verified INTEGER);"


sqlite3 users.db
.tables
.schema users
