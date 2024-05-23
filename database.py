import sqlite3
import time
from datetime import datetime, timedelta
from habit import Habit

def create_connection():
    conn = sqlite3.connect('habits.db', timeout=30)
    return conn

def create_table():
    with create_connection() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS habits
                     (id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, frequency TEXT, streak INTEGER, completion_dates TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, username TEXT)''')

def alter_table_add_column():
    with create_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("ALTER TABLE habits ADD COLUMN user_id INTEGER")
        except sqlite3.OperationalError:
            pass

def execute_with_retry(cursor, query, params=()):
    retries = 5
    while retries > 0:
        try:
            cursor.execute(query, params)
            return
        except sqlite3.OperationalError:
            retries -= 1
            if retries == 0:
                raise
            time.sleep(2)

def add_habit_to_db(habit, user_id):
    with create_connection() as conn:
        c = conn.cursor()
        execute_with_retry(c, "INSERT INTO habits (user_id, name, frequency, streak, completion_dates) VALUES (?, ?, ?, ?, ?)", 
                           (user_id, habit.habit_name, habit.frequency, habit.streak, ','.join(habit.completion_dates)))
        conn.commit()

def update_habit_in_db(habit, user_id):
    with create_connection() as conn:
        c = conn.cursor()
        execute_with_retry(c, "UPDATE habits SET streak = ?, completion_dates = ? WHERE user_id = ? AND name = ?", 
                           (habit.streak, ','.join(habit.completion_dates), user_id, habit.habit_name))
        conn.commit()

def load_habits_from_db(user_id):
    with create_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT name, frequency, streak, completion_dates FROM habits WHERE user_id = ?", (user_id,))
        rows = c.fetchall()
        
        habits = []
        for row in rows:
            name, frequency, streak, completion_dates = row
            habit = Habit(name, frequency)
            habit.streak = streak
            habit.creation_date = datetime.now()
            habit.completion_dates = completion_dates.split(',') if completion_dates else []
            habits.append(habit)
        return habits

def load_users_from_db():
    with create_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id, username FROM users")
        return c.fetchall()

def add_user_to_db(username):
    with create_connection() as conn:
        c = conn.cursor()
        execute_with_retry(c, "INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()

def get_user_id(username):
    with create_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_id = c.fetchone()
        return user_id[0] if user_id else None

def initialize_users_and_habits():
    create_table()
    alter_table_add_column()  
    users = ["HarryPotterFan"]
    predefined_habits = [
        {"name": "Practice Quidditch", "frequency": "daily"},
        {"name": "Read a Chapter of 'Magical Theory'", "frequency": "daily"},
        {"name": "Brew a Potion", "frequency": "weekly"},
        {"name": "Visit Hagrid", "frequency": "weekly"},
        {"name": "Attend Dueling Club", "frequency": "weekly"}
    ]

    with create_connection() as conn:
        c = conn.cursor()
        
        for username in users:
            execute_with_retry(c, "INSERT INTO users (username) VALUES (?)", (username,))
            c.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_id = c.fetchone()[0]

            for habit_data in predefined_habits:
                habit = Habit(habit_data["name"], habit_data["frequency"])
                completion_dates = [datetime.now() - timedelta(days=x) for x in range(0, 28, 7 if habit_data["frequency"] == "weekly" else 1)]
                habit.completion_dates = [date.isoformat() for date in completion_dates]
                habit.streak = len(habit.completion_dates)
                execute_with_retry(c, "INSERT INTO habits (user_id, name, frequency, streak, completion_dates) VALUES (?, ?, ?, ?, ?)", 
                                   (user_id, habit.habit_name, habit.frequency, habit.streak, ','.join(habit.completion_dates)))

        conn.commit()