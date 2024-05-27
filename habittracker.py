from habit import Habit
from reward import Reward  
import database as db
import random

class HabitTracker:
    def __init__(self, user_id):
        """
        Initialize the HabitTracker with a user ID.

        :param user_id: ID of the user whose habits are being tracked
        """
        self.user_id = user_id
        self.habits = []
        self.reward = Reward()
        self.load_habits()

    def add_habit(self, habit): # Add a new habit to the tracker and database
        self.habits.append(habit)
        db.add_habit_to_db(habit, self.user_id)

    def remove_habit(self, habit_name): # Remove a habit from the tracker and database
        self.habits = [habit for habit in self.habits if habit.habit_name != habit_name]
        db.remove_habit_from_db(habit_name, self.user_id)

    def view_all_habits(self): # View all habits being tracked
        return self.habits

    def load_habits(self): # Load habits for the user from the database
        self.habits = db.load_habits_from_db(self.user_id)

    def mark_habit_complete(self, habit_name): # Mark a habit as complete and update the database
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