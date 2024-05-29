import sys
import os
import unittest
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from habit import Habit
from analytics import Analytics

class TestAnalytics(unittest.TestCase):

    def setUp(self):
        # Predefined habits from initialize_users_and_habits
        self.habits = [
            Habit(habit_name='Practice Quidditch', frequency='daily'),
            Habit(habit_name='Read a Chapter of \'Magical Theory\'', frequency='daily'),
            Habit(habit_name='Brew a Potion', frequency='weekly'),
            Habit(habit_name='Visit Hagrid', frequency='weekly'),
            Habit(habit_name='Attend Dueling Club', frequency='weekly')
        ]
        # Add completion dates to habits
        for habit in self.habits:
            if habit.frequency == 'daily':
                completion_dates = [datetime.now() - timedelta(days=i) for i in range(4)]
            else:
                completion_dates = [datetime.now() - timedelta(days=i*7) for i in range(4)]
            habit.completion_dates = [date.isoformat() for date in completion_dates]
            habit.streak = len(habit.completion_dates)
        
        self.analytics = Analytics(self.habits)

    def test_list_current_habits(self):
        habits_list = self.analytics.list_current_habits()
        self.assertEqual(set(habits_list), {'Practice Quidditch', 'Read a Chapter of \'Magical Theory\'', 'Brew a Potion', 'Visit Hagrid', 'Attend Dueling Club'})

    def test_habits_with_same_frequency(self):
        daily_habits = self.analytics.habits_with_same_frequency('daily')
        weekly_habits = self.analytics.habits_with_same_frequency('weekly')
        self.assertEqual(len(daily_habits), 2)
        self.assertEqual(len(weekly_habits), 3)
        self.assertTrue(all(habit.frequency == 'daily' for habit in daily_habits))
        self.assertTrue(all(habit.frequency == 'weekly' for habit in weekly_habits))

    def test_longest_run_streak_of_all(self):
        self.assertEqual(self.analytics.longest_run_streak_of_all(), 4)

    def test_longest_run_streak_for_habit(self):
        streak = self.analytics.longest_run_streak_for_habit('Practice Quidditch')
        self.assertEqual(streak, 4)

    def test_longest_streak(self):
        longest_streak_habit = self.analytics.longest_streak()
        self.assertEqual(longest_streak_habit.habit_name, 'Practice Quidditch')

    def test_most_missed(self):
        self.habits[0].mark_incomplete()  # Reduce streak of 'Practice Quidditch' habit
        most_missed_habit = self.analytics.most_missed()
        self.assertEqual(most_missed_habit.habit_name, 'Practice Quidditch')

if __name__ == '__main__':
    unittest.main()