# Habit Tracker

A simple habit tracker application suited for ADHD-challenged thanks to random rewards to keep motivation and minimal distractions.

## Features

- Create and manage habits
- Track habit completion and streaks
- Assign rewards for completing tasks
- Store data about your habits
- Mark habits as incomplete ans update streaks
- Interactive command-line interface


## Getting Started

### Prerequisites

	•	Python 3.8+

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/habit-tracker.git
    cd habit-tracker
    ``` 
2. Install dependencies from `requirements.txt`:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

#### Locally

1. Run the application:
    ```sh
    python main.py
    ```

#### With Docker

1. Build the Docker image:
    ```sh
    docker build -t adhd-tracker .
    ```
2. Run the Docker container:
    ```sh
    docker run -it adhd-tracker

### Usage

**Command-Line Interface (CLI)**

The application provides an interactive CLI to manage your habits. Here’s a brief overview of the available commands:

	1.	Create a new user:
	    • The application will prompt you to enter a username.
	2.	Choose an existing user:
	    • Select a user from the list displayed by the application.
	3.	Add a habit:
	    • Enter the habit name and frequency (daily or weekly).
	4.	Complete a habit:
	    • Mark a habit as completed for the current date.
	5.	Delete a habit:
	    • Remove a habit from the database.
	6.	View habit analytics:
	    • Longest streak
	    • Most missed habit
        • Habits with the same periodicity
        • Longest run streak for a given habit

### Project Structure

	•	main.py - The entry point of the application, providing the CLI.
	•	habit.py - Contains the Habit class implementation.
	•	user.py - Contains the User class implementation.
	•	habittracker.py - Manages habit-related operations.
	•	reward.py - Handles the rewards system.
	•	analytics.py - Provides analytical functionalities for habits.
	•	database.py - Manages database operations.
	•	README.md - Project documentation and setup instructions.

### Data Persistence

The application uses SQLite to store habit data between sessions. The database schema includes tables for users and habits.