import unittest
from unittest.mock import patch
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reward import Reward

class TestReward(unittest.TestCase):
    def setUp(self):
        self.reward = Reward()

    def test_initial_rewards(self):
        expected_rewards = [
            "Take a 5-minute break",
            "Go see if Hagrid made cookies",
            "Crochet hats for SPEW",
            "Read a chapter of Hogwarts: A History",
        ]
        self.assertEqual(self.reward.reward_pool, expected_rewards)
        self.assertEqual(self.reward.custom_rewards, [])

    def test_add_custom_reward(self):
        self.reward.add_custom_reward("Play a game of wizard's chess")
        self.assertIn("Play a game of wizard's chess", self.reward.custom_rewards)

    @patch('random.choice', return_value="Take a 5-minute break")
    def test_trigger_with_initial_rewards(self, mock_choice):
        reward = self.reward.trigger()
        self.assertEqual(reward, "Take a 5-minute break")
        mock_choice.assert_called_once_with(self.reward.reward_pool)

    def test_trigger_with_no_rewards(self):
        self.reward.reward_pool = []
        self.reward.custom_rewards = []
        reward = self.reward.trigger()
        self.assertEqual(reward, "No rewards available")

    @patch('random.choice', return_value="Play a game of wizard's chess")
    def test_trigger_with_custom_rewards(self, mock_choice):
        self.reward.add_custom_reward("Play a game of wizard's chess")
        reward = self.reward.trigger()
        self.assertEqual(reward, "Play a game of wizard's chess")
        mock_choice.assert_called_once_with(self.reward.reward_pool + self.reward.custom_rewards)

if __name__ == '__main__':
    unittest.main()