from habit import Habit
from user import User
from reward import Reward
from database import create_table, add_user_to_db, get_user_id

def main():
    create_table()

    username = "Harry"
    add_user_to_db(username)
    user_id = get_user_id(username)

    user = User(username, user_id)
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

    longest_streak_habit = user.get_longest_streak()
    if longest_streak_habit:
        print(f"Longest streak: {longest_streak_habit.habit_name} with streak of {longest_streak_habit.streak}")

    most_missed_habit = user.get_most_missed_habit()
    if most_missed_habit:
        print(f"Most missed habit: {most_missed_habit.habit_name} with {len(most_missed_habit.completion_dates)} completions")

    user.remove_habit("Read a Chapter of 'Magical Theory'")
    print(f"After removing a habit, {user.username}'s habits:")
    for habit in user.get_habits():
        print(f"- {habit.habit_name} ({habit.frequency})")

if __name__ == "__main__":
    main()