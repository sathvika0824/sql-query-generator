import sqlite3

def create_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            marks INTEGER,
            attendance INTEGER,
            grade TEXT
        )
    ''')

    cursor.executemany('''
        INSERT OR IGNORE INTO students (id, name, marks, attendance, grade)
        VALUES (?, ?, ?, ?, ?)
    ''', [
        (1, "Sathvika", 92, 95, "A"),
        (2, "Arjun", 78, 80, "B"),
        (3, "Priya", 85, 90, "A"),
        (4, "Rahul", 60, 70, "C"),
        (5, "Sneha", 45, 60, "D"),
        (6, "Kiran", 88, 85, "A"),
        (7, "Meena", 72, 75, "B"),
        (8, "Rohan", 55, 65, "C")
    ])

    conn.commit()
    conn.close()
    print("Database created successfully!")

create_database()