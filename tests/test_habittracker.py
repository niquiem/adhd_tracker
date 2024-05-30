import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from habittracker import HabitTracker
from habit import Habit
import database as db

class TestHabitTracker(unittest.TestCase):

    def setUp(self):
        db.create_table()
        db.alter_table_add_column()
        db.add_user_to_db('TestUser')
        self.user_id = db.load_users_from_db()[0][0]
        self.tracker = HabitTracker(self.user_id)
        self.clear_habits()
        self.initialize_predefined_habits()

    def tearDown(self):
        self.clear_habits()

    def clear_habits(self):
        conn = db.create_connection()
        c = conn.cursor()
        c.execute("DELETE FROM habits WHERE user_id = ?", (self.user_id,))
        conn.commit()
        conn.close()

    def initialize_predefined_habits(self):
        predefined_habits = [
            {"name": "Practice Quidditch", "frequency": "daily"},
            {"name": "Read a Chapter of 'Magical Theory'", "frequency": "daily"},
            {"name": "Brew a Potion", "frequency": "weekly"},
            {"name": "Visit Hagrid", "frequency": "weekly"},
            {"name": "Attend Dueling Club", "frequency": "weekly"}
        ]
        for habit_data in predefined_habits:
            habit = Habit(habit_data["name"], habit_data["frequency"])
            completion_dates = [datetime.now() - timedelta(days=x) for x in range(0, 35, 7 if habit_data["frequency"] == "weekly" else 1)]
            habit.completion_dates = [date.isoformat() for date in completion_dates]
            habit.streak = len(habit.completion_dates)
            self.tracker.add_habit(habit)

    def test_add_habit(self):
        new_habit = Habit('Exercise', 'daily')
        self.tracker.add_habit(new_habit)
        self.assertIn(new_habit, self.tracker.habits)

    def test_mark_habit_complete(self):
        self.tracker.mark_habit_complete('Practice Quidditch')
        habit = next((h for h in self.tracker.habits if h.habit_name == 'Practice Quidditch'), None)
        self.assertIsNotNone(habit)
        self.assertEqual(habit.streak, 36)  # Correct streak count after marking complete

    def test_view_all_habits(self):
        habits = self.tracker.view_all_habits()
        habit_names = [habit.habit_name for habit in habits]
        expected_habits = [
            'Practice Quidditch', 
            'Read a Chapter of \'Magical Theory\'', 
            'Brew a Potion', 
            'Visit Hagrid', 
            'Attend Dueling Club'
        ]
        self.assertCountEqual(habit_names, expected_habits)

    def test_remove_habit(self):
        self.tracker.add_habit(Habit('Exercise', 'daily'))
        self.tracker.remove_habit('Exercise')
        habit_names = [habit.habit_name for habit in self.tracker.view_all_habits()]
        self.assertNotIn('Exercise', habit_names)

if __name__ == '__main__':
    unittest.main()