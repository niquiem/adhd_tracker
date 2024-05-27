import random

class Reward:
    def __init__(self):
        """
        Initialize the Reward class with a pool of default rewards
        and an empty list for custom rewards.
        """
        self.reward_pool = [
            "Take a 5-minute break",
            "Go see if Hagrid made cookies",
            "Crochet hats for SPEW",
            "Read a chapter of Hogwarts: A History",
        ]
        self.custom_rewards = []

    def add_custom_reward(self, reward): # Add a custom reward to the list
        self.custom_rewards.append(reward)

    def trigger(self): # Trigger a random reward from the pool or custom rewards
        all_rewards = self.reward_pool + self.custom_rewards
        if all_rewards:
            return random.choice(all_rewards)
        return "No rewards available"