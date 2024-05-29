from user import User
from habit import Habit
from habittracker import HabitTracker
from reward import Reward
from database import create_table, add_user_to_db, get_user_id, load_users_from_db, delete_user_from_db
from analytics import Analytics

# Function to create a new user and add them to the database
def create_user(username):
    add_user_to_db(username)
    user_id = get_user_id(username)
    return User(username, user_id)

# Function to display all habits
def display_habits(habit_tracker):
    print(f"\nHabits:")
    for habit in habit_tracker.view_all_habits():
        print(f"- {habit.habit_name} ({habit.frequency}), Streak: {habit.streak}")

# Function to choose a user from the database
def choose_user():
    users = load_users_from_db()
    if not users:
        print("No users found. Please create a new user.")
        return None

    while True:
        print("\nUsers:")  # Display all users
        for idx, (user_id, username) in enumerate(users, start=1):
            print(f"{idx}. {username}")

        try:
            choice = input("Choose a user by number or type 'new' to create a new user: ")
        except EOFError:
            print("\nEOFError: No input received. Exiting...")
            return None

        if choice.lower() == 'new':
            return None

        try:
            user_idx = int(choice) - 1
            if 0 <= user_idx < len(users):
                return users[user_idx]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Function to delete a user from the database
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

# Main function to run the Habit Tracker
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

    while True:  # Main menu
        print("\nMenu:")
        print("1. Add a habit")
        print("2. View habits")
        print("3. Mark habit as complete")
        print("4. Mark habit as incomplete")
        print("5. Add custom reward")
        print("6. View custom rewards")
        print("7. Delete a habit")
        print("8. Switch user")
        print("9. Delete user")
        print("10. View longest streak")
        print("11. View most missed habit")
        print("12. View habits with same periodicity")
        print("13. View longest run streak for a habit")
        print("14. Quit")

        choice = input("Choose an option: ")

        if choice == '1':  # Add a habit
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

        elif choice == '2':  # View habits
            display_habits(habit_tracker)

        elif choice == '3':  # Mark habit as complete
            habit_name = input("Enter the name of the habit you completed: ")
            habit, reward_message = habit_tracker.mark_habit_complete(habit_name)
            if habit:
                print(f"Habit '{habit_name}' marked as complete.")
                if reward_message:
                    print(f"Reward: {reward_message}")
            else:
                print(f"Habit '{habit_name}' not found.")

        elif choice == '4':  # Mark habit as incomplete
            habit_name = input("Enter the name of the habit you want to mark as incomplete: ")
            habit = next((h for h in habit_tracker.view_all_habits() if h.habit_name == habit_name), None)
            if habit:
                habit.mark_incomplete()
                print(f"Habit '{habit_name}' marked as incomplete.")
            else:
                print(f"Habit '{habit_name}' not found.")

        elif choice == '5':  # Add custom reward
            custom_reward = input("Enter the custom reward: ")
            habit_tracker.reward.add_custom_reward(custom_reward)
            print(f"Custom reward '{custom_reward}' added.")

        elif choice == '6':  # View custom rewards
            print("\nCustom Rewards:")
            for reward in habit_tracker.reward.custom_rewards:
                print(f"- {reward}")

        elif choice == '7':  # Delete a habit
            habit_name = input("Enter the name of the habit to delete: ")
            habit_tracker.remove_habit(habit_name)
            analytics = Analytics(habit_tracker.view_all_habits())
            print(f"Habit '{habit_name}' deleted.")
            display_habits(habit_tracker)

        elif choice == '8':  # Switch user
            user_info = choose_user()
            if not user_info:
                username = input("Enter a new username: ")
                user = create_user(username)
            else:
                user_id, username = user_info
                user = User(username, user_id)
            habit_tracker = HabitTracker(user.user_id)
            analytics = Analytics(habit_tracker.view_all_habits())

        elif choice == '9':  # Delete user
            delete_user()

        elif choice == '10':  # View longest streak
            longest_streak_habit = analytics.longest_streak()
            if longest_streak_habit:
                print(f"Longest streak: {longest_streak_habit.habit_name} with streak of {longest_streak_habit.streak}")
            else:
                print("No habits found.")

        elif choice == '11':  # View most missed habit
            most_missed_habit = analytics.most_missed()
            if most_missed_habit:
                print(f"Most missed habit: {most_missed_habit.habit_name} with {len(most_missed_habit.completion_dates)} completions")
            else:
                print("No habits found.")

        elif choice == '12':  # View habits with the same periodicity
            frequency = input("Enter the frequency (daily/weekly): ")
            if frequency not in ["daily", "weekly"]:
                print("Invalid periodicity. Please enter 'daily' or 'weekly'.")
                continue
            same_frequency_habits = analytics.habits_with_same_frequency(frequency)
            if same_frequency_habits:
                print(f"\nHabits with {frequency} periodicity:")
                for habit in same_frequency_habits:
                    print(f"- {habit.habit_name} with streak of {habit.streak}")
            else:
                print(f"No habits with {frequency} periodicity found.")

        elif choice == '13':  # View longest run streak for a habit
            habit_name = input("Enter the name of the habit: ")
            longest_streak = analytics.longest_run_streak_for_habit(habit_name)
            if longest_streak > 0:
                print(f"The longest streak for '{habit_name}' is {longest_streak}")
            else:
                print(f"Habit '{habit_name}' not found or has no streak.")

        elif choice == '14':  # Quit the program
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()