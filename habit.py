from datetime import datetime

class Habit:
    def __init__(self, habit_name, frequency, streak=0, completion_dates=None):
        """
        Initialize a Habit object.

        :param habit_name: Name of the habit
        :param frequency: Periodicity of the habit (e.g., daily, weekly)
        :param streak: Current streak of consecutive completions (default is 0)
        :param completion_dates: List of dates when the habit was completed (default is None, which initializes an empty list)
        """
        self.habit_name = habit_name
        self.frequency = frequency
        self.streak = streak
        self.creation_date = datetime.now()
        self.completion_dates = completion_dates if completion_dates else []
        self.reward = None

    def mark_complete(self): # Mark the habit as complete for the current date
        self.completion_dates.append(datetime.now().isoformat())
        self.streak += 1
        if self.reward:
            reward_message = self.reward.trigger()
            print(f"Reward for completing {self.habit_name}: {reward_message}")

    def mark_incomplete(self): # Mark the habit as incomplete by removing the most recent completion date
        if self.completion_dates:
            self.completion_dates.pop()
            self.streak = max(0, self.streak - 1)
        else:
            print(f"No completions to remove for {self.habit_name}")

    def check_streak(self): # Check the current streak of the habit
        return self.streak

    def set_reward(self, reward): # Set a reward for completing the habit
        self.reward = reward