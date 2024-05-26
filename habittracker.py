from habit import Habit
from reward import Reward  
import database as db
import random

class HabitTracker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.habits = []
        self.reward = Reward()
        self.load_habits()

    def add_habit(self, habit):
        self.habits.append(habit)
        db.add_habit_to_db(habit, self.user_id)

    def remove_habit(self, habit_name):
        self.habits = [habit for habit in self.habits if habit.habit_name != habit_name]
        db.remove_habit_from_db(habit_name, self.user_id)

    def view_all_habits(self):
        return self.habits

    def load_habits(self):
        self.habits = db.load_habits_from_db(self.user_id)

    def mark_habit_complete(self, habit_name):
        habit = next((h for h in self.habits if h.habit_name == habit_name), None)
        if habit:
            habit.mark_complete()
            db.update_habit_in_db(habit, self.user_id)
            if random.random() < 0.5:
                reward_message = self.reward.trigger()
                return habit, reward_message
            else:
                return habit, None
        return None, None