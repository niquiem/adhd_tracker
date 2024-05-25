import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from user import User
from habit import Habit

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(username="HarryPotterFan", user_id=1)

    @patch('user.add_habit_to_db')
    def test_add_habit(self, mock_add_habit_to_db):
        new_habit = Habit("Read a Chapter of 'Magical Theory'", "daily")
        
        self.user.add_habit(new_habit)
        
        self.assertIn(new_habit, self.user.habits)
        
        mock_add_habit_to_db.assert_called_once_with(new_habit, 1)

    def test_remove_habit(self):
        habit1 = Habit("Practice Quidditch", "daily")
        habit2 = Habit("Read a Chapter of 'Magical Theory'", "daily")
        self.user.habits = [habit1, habit2]
        
        self.user.remove_habit("Practice Quidditch")
        
        self.assertNotIn(habit1, self.user.habits)
        
        self.assertIn(habit2, self.user.habits)

    def test_get_habits(self):
        habit = Habit("Practice Quidditch", "daily")
        self.user.habits = [habit]
        
        habits = self.user.get_habits()
        
        self.assertEqual(habits, [habit])

    @patch('user.load_habits_from_db')
    def test_load_habits(self, mock_load_habits_from_db):
        mock_habits = [
            Habit("Practice Quidditch", "daily"),
            Habit("Brew a Potion", "weekly")
        ]
        mock_load_habits_from_db.return_value = mock_habits
        
        user = User(username="TestUser", user_id=2)
        
        self.assertEqual(user.habits, mock_habits)
        
        mock_load_habits_from_db.assert_called_once_with(2)

if __name__ == '__main__':
    unittest.main()