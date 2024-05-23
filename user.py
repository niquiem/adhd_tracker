from database import add_habit_to_db, load_habits_from_db
from habit import Habit

class User:
    def __init__(self, username, user_id=None):
        self.username = username
        self.user_id = user_id
        self.habits = self.load_habits()

    def add_habit(self, habit):
        self.habits.append(habit)
        add_habit_to_db(habit, self.user_id)

    def remove_habit(self, habit_name):
        self.habits = [habit for habit in self.habits if habit.habit_name != habit_name]

    def get_habits(self):
        return self.habits

    def load_habits(self):
        habits_data = load_habits_from_db(self.user_id)
        habits = []
        for habit_data in habits_data:
            habit = Habit(habit_data[0], habit_data[1], habit_data[2], habit_data[3].split(','))
            habits.append(habit)
        return habits
