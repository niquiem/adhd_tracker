from habit import Habit

def main():
    # Creating a new habit for testing
    new_habit = Habit("Exercise", "daily")
    print(f"Created habit: {new_habit.habit_name} with frequency: {new_habit.frequency}")
    new_habit.mark_complete()
    print(f"Habit {new_habit.habit_name} marked complete. Current streak: {new_habit.check_streak()}")

if __name__ == "__main__":
    main()