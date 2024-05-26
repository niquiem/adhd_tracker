from user import User
from habit import Habit
from habittracker import HabitTracker
from reward import Reward
from database import create_table, add_user_to_db, get_user_id, load_users_from_db, delete_user_from_db
from analytics import Analytics

def create_user(username):
    add_user_to_db(username)
    user_id = get_user_id(username)
    return User(username, user_id)

def display_habits(habit_tracker):
    print(f"\nHabits:")
    for habit in habit_tracker.view_all_habits():
        print(f"- {habit.habit_name} ({habit.frequency}), Streak: {habit.streak}")

def choose_user():
    users = load_users_from_db()
    if not users:
        print("No users found. Please create a new user.")
        return None

    print("\nUsers:")
    for idx, (user_id, username) in enumerate(users, start=1):
        print(f"{idx}. {username}")

    choice = input("Choose a user by number or type 'new' to create a new user: ")
    if choice.lower() == 'new':
        return None

    try:
        user_idx = int(choice) - 1
        if 0 <= user_idx < len(users):
            return users[user_idx]
    except ValueError:
        pass

    print("Invalid choice. Please try again.")
    return choose_user()
def delete_user():
    users = load_users_from_db()
    if not users:
        print("No users found.")
        return

    print("\nUsers:")
    for idx, (user_id, username) in enumerate(users, start=1):
        print(f"{idx}. {username}")

    choice = input("Choose a user by number to delete or type 'cancel' to go back: ")
    if choice.lower() == 'cancel':
        return

    try:
        user_idx = int(choice) - 1
        if 0 <= user_idx < len(users):
            user_id, username = users[user_idx]
            delete_user_from_db(user_id)
            print(f"User '{username}' deleted.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

def main():
    create_table()
    
    print("Welcome to the Habit Tracker!")
    user_info = choose_user()
    if not user_info:
        username = input("Enter a new username: ")
        user = create_user(username)
    else:
        user_id, username = user_info
        user = User(username, user_id)
    
    habit_tracker = HabitTracker(user.user_id)
    analytics = Analytics(habit_tracker.view_all_habits())

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
        print("10. Switch user")
        print("11. Delete user")
        print("12. Quit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            habit_name = input("Enter the habit name: ")
            frequency = input("Enter the habit frequency (daily/weekly): ")
            if frequency not in ["daily", "weekly"]:
                print("Invalid frequency. Please enter 'daily' or 'weekly'.")
                continue
            habit = Habit(habit_name, frequency)
            habit.set_reward(habit_tracker.reward)
            habit_tracker.add_habit(habit)
            analytics = Analytics(habit_tracker.view_all_habits())
            print(f"Habit '{habit_name}' added.")

        elif choice == '2':
            display_habits(habit_tracker)

        elif choice == '3':
            habit_name = input("Enter the name of the habit you completed: ")
            habit, reward_message = habit_tracker.mark_habit_complete(habit_name)
            if habit:
                print(f"Habit '{habit_name}' marked as complete.")
                if reward_message:
                    print(f"Reward: {reward_message}")
            else:
                print(f"Habit '{habit_name}' not found.")

        elif choice == '4':
            habit_name = input("Enter the name of the habit you want to mark as incomplete: ")
            habit = next((h for h in habit_tracker.view_all_habits() if h.habit_name == habit_name), None)
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
            habit_tracker.reward.add_custom_reward(custom_reward)
            print(f"Custom reward '{custom_reward}' added.")

        elif choice == '8':
            print("\nCustom Rewards:")
            for reward in habit_tracker.reward.custom_rewards:
                print(f"- {reward}")

        elif choice == '9':
            habit_name = input("Enter the name of the habit to delete: ")
            habit_tracker.remove_habit(habit_name)
            analytics = Analytics(habit_tracker.view_all_habits())  
            print(f"Habit '{habit_name}' deleted.")
            display_habits(habit_tracker)

        elif choice == '10':
            user_info = choose_user()
            if not user_info:
                username = input("Enter a new username: ")
                user = create_user(username)
            else:
                user_id, username = user_info
                user = User(username, user_id)
            habit_tracker = HabitTracker(user.user_id)
            analytics = Analytics(habit_tracker.view_all_habits())  

        elif choice == '11':
            delete_user()

        elif choice == '12':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()