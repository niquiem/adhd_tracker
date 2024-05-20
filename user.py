class User:
    def __init__(self, username):
        self.username = username
        self.habits = []

    def add_habit(self, habit):
        self.habits.append(habit)

    def remove_habit(self, habit_name):
        self.habits = [habit for habit in self.habits if habit.habit_name != habit_name]

    def get_habits(self):
        return self.habits