import mysql.connector
def connect_to_login_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="database name"  # Connect to the existing Users database
    )

def add_user(username, password):
    try:
        conn = connect_to_login_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        print("User added successfully!")
        return "User added successfully!"
    except mysql.connector.IntegrityError as e:
        # This exception is raised if the username already exists in the database
        print("User already exists!")
        return "User already exists!"
    except Exception as e:
        print(f"Error adding user: {e}")
        return "Failed to register. Please try again."
    finally:
        conn.close()

def validate_login(username, password):
    try:
        conn = connect_to_login_database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            print("Login Successful!")
            return True
        else:
            print("Invalid username or password")
            return False
    except Exception as e:
        print(f"Error validating login: {e}")
        return False
    finally:
        conn.close()

