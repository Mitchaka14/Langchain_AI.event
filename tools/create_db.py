# create_db.py

import sqlite3
from sqlite3 import Error


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(
            "appointments.db"
        )  # Creates a SQLite database file named 'appointments.db'
        print(f"successful connection with sqlite version {sqlite3.version}")
    except Error as e:
        print(e)

    if conn:
        return conn


def create_table(conn):
    try:
        query = """CREATE TABLE appointments (
                        id integer PRIMARY KEY,
                        date text NOT NULL,
                        time text NOT NULL,
                        details text NOT NULL,
                        client_name text NOT NULL,
                        client_contact text NOT NULL
                    ); """
        conn.execute(query)
        print("Table created successfully....")
    except Error as e:
        print(e)


def insert_appointments(conn):
    appointments = [
        ("2023-08-10", "10:00", "Check-up", "John Doe", "1234567890"),
        ("2023-08-15", "14:00", "Consultation", "Jane Doe", "0987654321"),
        ("2023-08-20", "11:00", "Follow-up", "Tom Smith", "1122334455"),
        ("2023-08-25", "15:30", "Check-up", "Alice Johnson", "3344556677"),
    ]

    conn.executemany(
        """
        INSERT INTO appointments(date, time, details, client_name, client_contact)
        VALUES(?,?,?,?,?)""",
        appointments,
    )

    conn.commit()

    print(f"{conn.total_changes} records inserted successfully into appointments table")


def main():
    conn = create_connection()
    if conn is not None:
        create_table(conn)
        insert_appointments(conn)
    else:
        print("Error! Cannot create a database connection.")


if __name__ == "__main__":
    main()
