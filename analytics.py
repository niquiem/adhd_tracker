class Analytics:
    def __init__(self, user_habits): # Add user_habits parameter
        self.user_habits = user_habits

    def longest_streak(self): #Find the habit with the longest streak
        if not self.user_habits:
            return None
        return max(self.user_habits, key=lambda habit: habit.streak)

    def most_missed(self): #Find the habit with the most missed completions
        if not self.user_habits:
            return None
        return min(self.user_habits, key=lambda habit: len(habit.completion_dates))

    def list_current_habits(self): #List the current habits
        return [habit.habit_name for habit in self.user_habits]