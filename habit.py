from datetime import datetime

class Habit:
    def __init__(self, habit_name, frequency, streak=0, completion_dates=None):
        self.habit_name = habit_name
        self.frequency = frequency
        self.streak = streak
        self.creation_date = datetime.now()
        self.completion_dates = completion_dates if completion_dates else []

    def mark_complete(self):
        self.completion_dates.append(datetime.now().isoformat())
        self.streak += 1
        if self.reward:
            reward_message = self.reward.trigger()
            print(f"Reward for completing {self.habit_name}: {reward_message}")

    def mark_incomplete(self):
        if self.completion_dates:
            self.completion_dates.pop()
            self.streak = max(0, self.streak - 1)
        else:
            print(f"No completions to remove for {self.habit_name}")

    def check_streak(self):
        return self.streak

    def set_reward(self, reward):
        self.reward = reward