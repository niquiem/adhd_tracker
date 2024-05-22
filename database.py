import sqlite3
from habit import Habit

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS habits
                 (id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, frequency TEXT, streak INTEGER, completion_dates TEXT)''')
    conn.commit()
    conn.close()

def add_user_to_db(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

def get_user_id(username):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = c.fetchone()
    conn.close()
    return user_id[0] if user_id else None

def add_habit_to_db(habit, user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO habits (user_id, name, frequency, streak, completion_dates) VALUES (?, ?, ?, ?, ?)", 
              (user_id, habit.habit_name, habit.frequency, habit.streak, ','.join(habit.completion_dates)))
    conn.commit()
    conn.close()

def load_habits_from_db(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT name, frequency, streak, completion_dates FROM habits WHERE user_id = ?", (user_id,))
    rows = c.fetchall()

conn.close()

return rows