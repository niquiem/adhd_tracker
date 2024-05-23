from user import User
from habit import Habit
from reward import Reward
from database import create_table, add_user_to_db, get_user_id
from analytics import Analytics

def create_user(username):
    add_user_to_db(username)
    user_id = get_user_id(username)
    return User(username, user_id)

def display_habits(user):
    print(f"\n{user.username}'s habits:")
    for habit in user.get_habits():
        print(f"- {habit.habit_name} ({habit.frequency}), Streak: {habit.streak}")

def main():
    create_table()
    
    print("Welcome to the Habit Tracker!")
    username = input("Enter your username: ")
    user = create_user(username)
    reward_system = Reward()
    analytics = Analytics(user.get_habits())

    while True:
        print("\nMenu:")
        print("1. Add a habit")
        print("2. View habits")
        print("3. Mark habit as complete")
        print("4. Mark habit as incomplete")
        print("5. View longest streak")
        print("6. View most missed habit")
        print("7. Add custom reward")
        print("8. View custom rewards")
        print("9. Delete a habit")
        print("10. Quit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            habit_name = input("Enter the habit name: ")
            frequency = input("Enter the habit frequency (daily/weekly): ")
            if frequency not in ["daily", "weekly"]:
                print("Invalid frequency. Please enter 'daily' or 'weekly'.")
                continue
            habit = Habit(habit_name, frequency)
            habit.set_reward(reward_system)
            user.add_habit(habit)
            analytics = Analytics(user.get_habits())  # Update analytics
            print(f"Habit '{habit_name}' added.")

        elif choice == '2':
            display_habits(user)

        elif choice == '3':
            habit_name = input("Enter the name of the habit you completed: ")
            habit = next((h for h in user.get_habits() if h.habit_name == habit_name), None)
            if habit:
                habit.mark_complete()
                print(f"Habit '{habit_name}' marked as complete.")
            else:
                print(f"Habit '{habit_name}' not found.")

        elif choice == '4':
            habit_name = input("Enter the name of the habit you want to mark as incomplete: ")
            habit = next((h for h in user.get_habits() if h.habit_name == habit_name), None)
            if habit:
                habit.mark_incomplete()
                print(f"Habit '{habit_name}' marked as incomplete.")
            else:
                print(f"Habit '{habit_name}' not found.")

        elif choice == '5':
            longest_streak_habit = analytics.longest_streak()
            if longest_streak_habit:
                print(f"Longest streak: {longest_streak_habit.habit_name} with streak of {longest_streak_habit.streak}")
            else:
                print("No habits found.")

        elif choice == '6':
            most_missed_habit = analytics.most_missed()
            if most_missed_habit:
                print(f"Most missed habit: {most_missed_habit.habit_name} with {len(most_missed_habit.completion_dates)} completions")
            else:
                print("No habits found.")

        elif choice == '7':
            custom_reward = input("Enter the custom reward: ")
            reward_system.add_custom_reward(custom_reward)
            print(f"Custom reward '{custom_reward}' added.")

        elif choice == '8':
            print("\nCustom Rewards:")
            for reward in reward_system.custom_rewards:
                print(f"- {reward}")

        elif choice == '9':
            habit_name = input("Enter the name of the habit to delete: ")
            user.remove_habit(habit_name)
            analytics = Analytics(user.get_habits())  # Update analytics
            print(f"Habit '{habit_name}' deleted.")
            display_habits(user)

        elif choice == '10':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()