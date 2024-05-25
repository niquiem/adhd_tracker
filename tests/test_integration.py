import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from user import User
from habit import Habit
from database import add_habit_to_db, load_habits_from_db, create_table, initialize_users_and_habits

class TestIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        create_table()
        initialize_users_and_habits()

    def setUp(self):
        self.user = User(username="IntegrationTestUser", user_id=99)

    @patch('user.add_habit_to_db', autospec=True)
    def test_add_and_remove_habit(self, mock_add_habit_to_db):
        habit1 = Habit("Test Habit 1", "daily")
        self.user.add_habit(habit1)
        
        self.assertIn(habit1, self.user.habits)
        mock_add_habit_to_db.assert_called_once_with(habit1, 99)

        habit2 = Habit("Test Habit 2", "weekly")
        self.user.add_habit(habit2)
        
        self.assertIn(habit1, self.user.habits)
        self.assertIn(habit2, self.user.habits)

        self.user.remove_habit("Test Habit 1")
        
        self.assertNotIn(habit1, self.user.habits)
        self.assertIn(habit2, self.user.habits)

    @patch('user.load_habits_from_db', autospec=True)
    def test_load_habits(self, mock_load_habits_from_db):
        
        mock_habits = [
            Habit("Mock Habit 1", "daily", streak=3, completion_dates=[datetime.now().isoformat()]),
            Habit("Mock Habit 2", "weekly", streak=1, completion_dates=[datetime.now().isoformat()])
        ]
        mock_load_habits_from_db.return_value = mock_habits
        
        user = User(username="IntegrationTestUser", user_id=99)
        
        self.assertEqual(user.habits, mock_habits)
        mock_load_habits_from_db.assert_called_once_with(99)

if __name__ == '__main__':
    unittest.main()