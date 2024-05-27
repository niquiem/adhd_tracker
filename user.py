from database import add_habit_to_db, load_habits_from_db
from habit import Habit

class User:
    def __init__(self, username, user_id=None):
        self.username = username
        self.user_id = user_id
        self.habits = self.load_habits()

    def add_habit(self, habit): # Add a habit to the user's list of habits and save it to the database
        self.habits.append(habit)
        add_habit_to_db(habit, self.user_id)

    def remove_habit(self, habit_name): # Remove a habit from the user's list of habits
        self.habits = [habit for habit in self.habits if habit.habit_name != habit_name]

    def get_habits(self): # Return the user's list of habits
        return self.habits

    def load_habits(self): # Load the user's habits from the database
        habits_data = load_habits_from_db(self.user_id)
        #Sprint(f"habits_data: {habits_data}")  # Debugging line: Uncomment to see the raw habits data from the database
        habits = []
        for habit_data in habits_data:
            #print(f"habit_data: {habit_data}")  # Debugging line: Uncomment to see each habit's data
            habits.append(habit_data)  # Directly append the Habit object
        return habits