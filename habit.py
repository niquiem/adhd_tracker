from datetime import datetime

class Habit:
    def __init__(self, habit_name, frequency):
        self.habit_name = habit_name
        self.frequency = frequency
        self.streak = 0
        self.creation_date = datetime.now()
        self.completion_dates = []

    def mark_complete(self):
        self.completion_dates.append(datetime.now().isoformat())
        self.streak += 1

    def check_streak(self):
        return self.streak