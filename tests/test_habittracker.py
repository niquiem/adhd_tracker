import unittest
from unittest.mock import patch, MagicMock
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../habittracker')))

from habittracker import HabitTracker
from habit import Habit
import database as db

class TestHabitTracker(unittest.TestCase):

    def setUp(self):
        db.create_table()
        db.add_user_to_db('TestUser')
        self.user_id = db.load_users_from_db()[0][0]
        self.tracker = HabitTracker(self.user_id)
        self.clear_habits()
        self.habit = Habit('Exercise', 'daily')

    def tearDown(self):
        self.clear_habits()

    def clear_habits(self):
        conn = db.create_connection()
        c = conn.cursor()
        c.execute("DELETE FROM habits WHERE user_id = ?", (self.user_id,))
        conn.commit()
        conn.close()

    def test_add_habit(self):
        self.tracker.add_habit(self.habit)
        self.assertIn(self.habit, self.tracker.habits)

    def test_mark_habit_complete(self):
        self.tracker.add_habit(self.habit)
        self.tracker.mark_habit_complete('Exercise')
        habit = next((h for h in self.tracker.habits if h.habit_name == 'Exercise'), None)
        print(f"Debug: Streak after marking complete is {habit.streak}")  # Debugging
        self.assertIsNotNone(habit)
        self.assertEqual(habit.streak, 1)

    def test_view_all_habits(self):
        self.tracker.add_habit(self.habit)
        habits = self.tracker.view_all_habits()
        self.assertIn(self.habit, habits)

if __name__ == '__main__':
    unittest.main()