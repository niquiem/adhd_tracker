class Analytics:
    def __init__(self, user_habits):
        self.user_habits = user_habits

    def longest_streak(self):
        if not self.user_habits:
            return None
        return max(self.user_habits, key=lambda habit: habit.streak)

    def most_missed(self):
        if not self.user_habits:
            return None
        return min(self.user_habits, key=lambda habit: len(habit.completion_dates))

    def list_current_habits(self):
        return [habit.habit_name for habit in self.user_habits]