from functools import reduce

class Analytics:
    def __init__(self, user_habits):  # Add user_habits parameter
        self.user_habits = user_habits

    def longest_streak(self):  # Find the habit with the longest streak
        if not self.user_habits:
            return None
        return max(self.user_habits, key=lambda habit: habit.streak)

    def most_missed(self):  # Find the habit with the most missed completions
        if not self.user_habits:
            return None
        return min(self.user_habits, key=lambda habit: len(habit.completion_dates))

    def list_current_habits(self):  # List the current habits
        return list(map(lambda habit: habit.habit_name, self.user_habits))

    def habits_with_same_frequency(self, frequency):  # List habits with the same frequency
        return list(filter(lambda habit: habit.frequency == frequency, self.user_habits))

    def longest_run_streak_of_all(self):  # Longest run streak of all habits
        if not self.user_habits:
            return 0
        return max(map(lambda habit: habit.streak, self.user_habits))

    def longest_run_streak_for_habit(self, habit_name):  # Longest run streak for a given habit
        habit = next(filter(lambda habit: habit.habit_name == habit_name, self.user_habits), None)
        return habit.streak if habit else 0