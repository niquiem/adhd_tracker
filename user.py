from database import add_habit_to_db, load_habits_from_db
from habit import Habit

class User:
    def __init__(self, username, user_id=None):
        """
        Initialize a new User object.

        Args:
            username (str): The username of the user.
            user_id (int, optional): The ID of the user in the database. Defaults to None.

        Attributes:
            username (str): The username of the user.
            user_id (int, optional): The ID of the user in the database.
            habits (list): The list of habits associated with the user, loaded from the database.
        """
        self.username = username
        self.user_id = user_id
        self.habits = self.load_habits()

    def add_habit(self, habit): # Add a new habit to the user's list of habits if it doesn't already exist
        #Raise an error if the habit already exists
        if any(existing_habit.habit_name == habit.habit_name for existing_habit in self.habits):
            raise ValueError(f"Habit '{habit.habit_name}' already exists.")
        self.habits.append(habit)
        add_habit_to_db(habit, self.user_id)

    def remove_habit(self, habit_name): # Remove a habit from the user's list of habits
        self.habits = [habit for habit in self.habits if habit.habit_name != habit_name]

    def get_habits(self): # Get the list of habits associated with the user
        return self.habits

    def load_habits(self): # Load the habits associated with the user from the database and return them as a list of Habit objects
        habits_data = load_habits_from_db(self.user_id)
        habits = []
        for habit_data in habits_data:
            habits.append(habit_data)
        return habits