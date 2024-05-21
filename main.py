from habit import Habit
from user import User
from reward import Reward

def main():
    user = User("Harry")
    print(f"Created user: {user.username}")

    reward_system = Reward()

    habit1 = Habit("Practice Quidditch", "daily")
    habit2 = Habit("Read a Chapter of 'Magical Theory'", "daily")

    habit1.set_reward(reward_system)
    habit2.set_reward(reward_system)
    
    user.add_habit(habit1)
    user.add_habit(habit2)

    print(f"{user.username}'s habits:")
    for habit in user.get_habits():
        print(f"- {habit.habit_name} ({habit.frequency})")

    habit1.mark_complete()
    print(f"Habit {habit1.habit_name} marked complete. Current streak: {habit1.check_streak()}")

    user.remove_habit("Read a Chapter of 'Magical Theory'")
    print(f"After removing a habit, {user.username}'s habits:")
    for habit in user.get_habits():
        print(f"- {habit.habit_name} ({habit.frequency})")

if __name__ == "__main__":
    main()