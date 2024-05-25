import sys
import os
import unittest
from datetime import datetime, timedelta
from io import StringIO
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from habit import Habit  

class MockReward:
    def trigger(self):
        return "Mock reward triggered!"

class TestHabit(unittest.TestCase):

    def setUp(self):
        self.habit = Habit(habit_name='Exercise', frequency='daily')

    def test_initialization(self):
        self.assertEqual(self.habit.habit_name, 'Exercise')
        self.assertEqual(self.habit.frequency, 'daily')
        self.assertEqual(self.habit.streak, 0)
        self.assertIsInstance(self.habit.creation_date, datetime)
        self.assertEqual(self.habit.completion_dates, [])
        self.assertIsNone(self.habit.reward)

    def test_mark_complete(self):
        self.habit.mark_complete()
        self.assertEqual(self.habit.streak, 1)
        self.assertEqual(len(self.habit.completion_dates), 1)
        completion_date = datetime.fromisoformat(self.habit.completion_dates[0])
        self.assertAlmostEqual(completion_date, datetime.now(), delta=timedelta(seconds=1))

    def test_mark_incomplete(self):
        self.habit.mark_complete()
        self.habit.mark_incomplete()
        self.assertEqual(self.habit.streak, 0)
        self.assertEqual(len(self.habit.completion_dates), 0)

    def test_check_streak(self):
        self.assertEqual(self.habit.check_streak(), 0)
        self.habit.mark_complete()
        self.assertEqual(self.habit.check_streak(), 1)

    @patch('sys.stdout', new_callable=StringIO)
    def test_set_reward(self, mock_stdout):
        mock_reward = MockReward()
        self.habit.set_reward(mock_reward)
        self.assertEqual(self.habit.reward, mock_reward)

        self.habit.mark_complete()
        output = mock_stdout.getvalue().strip()
        self.assertIn('Mock reward triggered!', output)

if __name__ == '__main__':
    unittest.main()