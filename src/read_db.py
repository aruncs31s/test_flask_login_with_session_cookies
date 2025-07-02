import sqlite3


def read_users_db(db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if not tables:
            print(f"No tables found in {db_path}")
            return

        print(f"Tables in {db_path}: {tables}")

        # Assuming the table is named 'user' based on the SQLAlchemy model
        cursor.execute("SELECT id, name, email, role FROM user")
        rows = cursor.fetchall()

        if not rows:
            print("No users found in the 'user' table.")
            return

        print("\nUsers in the database:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Role: {row[3]}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    db_file = "instance/users.db"
    read_users_db(db_file)
