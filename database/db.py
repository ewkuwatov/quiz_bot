import sqlite3

class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        self.create_table()
        self.question_table()


    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                rating INTEGER DEFAULT 0
            )
        """)
        self.connection.commit()

    def add_user(self, user_id, username, first_name, last_name):
        existing_user = self.get_user_by_id(user_id)

        if existing_user:
            print(f"Пользователь с ID {user_id} уже существует.")
        else:
            self.cursor.execute("""
                INSERT INTO users (user_id, username, first_name, last_name, rating)
                VALUES (?, ?, ?, ?, 0)
            """, (user_id, username, first_name, last_name))
            self.connection.commit()

    def get_user_by_id(self, user_id):
        self.cursor.execute("""
            SELECT * FROM users WHERE user_id = ?
        """, (user_id,))
        return self.cursor.fetchone()

    def delete_user(self, user_id):
        self.cursor.execute("""
            DELETE FROM users WHERE user_id = ?
        """, (user_id,))
        self.connection.commit()

    def increment_user_rating(self, user_id):
        self.cursor.execute("""
            UPDATE users SET rating = rating + 1 WHERE user_id = ?
        """, (user_id,))
        self.connection.commit()

    # Добавим метод для корректного закрытия базы данных
    def close(self):
        if self.connection:
            self.connection.close()

    def question_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT,
                option1 TEXT,
                option2 TEXT,
                option3 TEXT,
                option4 TEXT,
                correct_option INTEGER
            )
        """)
        self.connection.commit()


