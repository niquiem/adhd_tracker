from datetime import datetime

class Habit:
    def __init__(self, habit_name, frequency):
        self.habit_name = habit_name
        self.frequency = frequency
        self.streak = 0
        self.creation_date = datetime.now()
        self.completion_dates = []
        self.reward = None

    def mark_complete(self):
        self.completion_dates.append(datetime.now().isoformat())
        self.streak += 1
        if self.reward:
            reward_message = self.reward.trigger()
            print(f"Reward for completing {self.habit_name}: {reward_message}")

    def check_streak(self):
        return self.streak
    
    def set_reward(self, reward):
        self.reward = reward