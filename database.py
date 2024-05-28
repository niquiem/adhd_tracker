import sqlite3
import time
from datetime import datetime, timedelta
from habit import Habit

def create_connection(): # Create a connection to the database
    conn = sqlite3.connect('habits.db', timeout=30)
    return conn

def create_table(): # Create the tables in the database and ussers if they don't exist
    with create_connection() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS habits
                     (id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, frequency TEXT, streak INTEGER, completion_dates TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, username TEXT)''')

def alter_table_add_column(): # Add the user_id column to the habits table if it doesn't exist
    with create_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("ALTER TABLE habits ADD COLUMN user_id INTEGER")
        except sqlite3.OperationalError:
            pass

def execute_with_retry(cursor, query, params=()): # Execute a query with retries in case of an OperationalError
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

def add_habit_to_db(habit, user_id): # Add a habit to the database for a specific user
    with create_connection() as conn:
        c = conn.cursor()
        execute_with_retry(c, "INSERT INTO habits (user_id, name, frequency, streak, completion_dates) VALUES (?, ?, ?, ?, ?)", 
                           (user_id, habit.habit_name, habit.frequency, habit.streak, ','.join(habit.completion_dates)))
        conn.commit()

def remove_habit_from_db(habit_name, user_id): # Remove a habit from the database for a specific user
    with create_connection() as conn:
        c = conn.cursor()
        execute_with_retry(c, "DELETE FROM habits WHERE user_id = ? AND name = ?", (user_id, habit_name))
        conn.commit()

def update_habit_in_db(habit, user_id): # Update a habit in the database for a specific user
    with create_connection() as conn:
        c = conn.cursor()
        execute_with_retry(c, "UPDATE habits SET streak = ?, completion_dates = ? WHERE user_id = ? AND name = ?", 
                           (habit.streak, ','.join(habit.completion_dates), user_id, habit.habit_name))
        conn.commit()

def load_habits_from_db(user_id): # Load the habits from the database for a specific user
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

def load_users_from_db(): # Load the users from the database
    with create_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id, username FROM users")
        return c.fetchall()

def add_user_to_db(username): # Add a new user to the database
    with create_connection() as conn:
        c = conn.cursor()
        execute_with_retry(c, "INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()

def get_user_id(username): # Get the user ID for a specific username
    with create_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_id = c.fetchone()
        return user_id[0] if user_id else None
    
def delete_user_from_db(user_id): # Delete a user from the database
    with create_connection() as conn:
        c = conn.cursor()
        execute_with_retry(c, "DELETE FROM habits WHERE user_id = ?", (user_id,))
        execute_with_retry(c, "DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

def initialize_users_and_habits(): # Initialize the database with some predefined users and habits
    create_table()
    alter_table_add_column()  
    users = ["HarryPotterFan", "Neville Longbottom", "Luna Lovegood"]
    predefined_habits = {
        "HarryPotterFan": [
            {"name": "Practice Quidditch", "frequency": "daily"},
            {"name": "Read a Chapter of 'Magical Theory'", "frequency": "daily"},
            {"name": "Brew a Potion", "frequency": "weekly"},
            {"name": "Visit Hagrid", "frequency": "weekly"},
            {"name": "Attend Dueling Club", "frequency": "weekly"}
        ],
        "Neville Longbottom": [
            {"name": "Water Herbology Plants", "frequency": "daily"},
            {"name": "Study Herbology", "frequency": "daily"},
            {"name": "Practice Defensive Spells", "frequency": "weekly"},
            {"name": "Collect Magical Herbs", "frequency": "weekly"},
            {"name": "Visit the Greenhouses", "frequency": "weekly"}
        ],
        "Luna Lovegood": [
            {"name": "Search for Nargles", "frequency": "daily"},
            {"name": "Read The Quibbler", "frequency": "daily"},
            {"name": "Practice Charm Spells", "frequency": "weekly"},
            {"name": "Explore Forbidden Forest", "frequency": "weekly"},
            {"name": "Help Magical Creatures", "frequency": "weekly"}
        ]
    }

    with create_connection() as conn:
        c = conn.cursor()
        
        for username in users:
            execute_with_retry(c, "INSERT INTO users (username) VALUES (?)", (username,))
            c.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_id = c.fetchone()[0]

            for habit_data in predefined_habits[username]:
                habit = Habit(habit_data["name"], habit_data["frequency"])
                completion_dates = [datetime.now() - timedelta(days=x) for x in range(0, 35, 7 if habit_data["frequency"] == "weekly" else 1)]
                habit.completion_dates = [date.isoformat() for date in completion_dates]
                habit.streak = len(habit.completion_dates)
                execute_with_retry(c, "INSERT INTO habits (user_id, name, frequency, streak, completion_dates) VALUES (?, ?, ?, ?, ?)", 
                                   (user_id, habit.habit_name, habit.frequency, habit.streak, ','.join(habit.completion_dates)))

        conn.commit()

# Initialize the users and habits
initialize_users_and_habits()