import json
import os

TASKS_FILE = "tasks.json"

class Task:
    """
    Represents a single task in the to-do list.
    
    Attributes:
        title (str): The title of the task.
        description (str): A detailed description of the task.
        category (str): The category the task belongs to (e.g., Work, Personal).
        completed (bool): The completion status of the task.
    """
    def __init__(self, title, description, category, completed=False):
        """Initializes a Task object."""
        self.title = title
        self.description = description
        self.category = category
        self.completed = completed

    def mark_completed(self):
        """Marks the task as completed."""
        self.completed = True
        
    def to_dict(self):
        """Converts the task object to a dictionary for JSON serialization."""
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        """Creates a Task object from a dictionary."""
        return Task(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            completed=data.get('completed', False) # Default to False if not present
        )

    def __str__(self):
        """Returns a string representation of the task."""
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.title} ({self.category})\n    Description: {self.description}"

def save_tasks(tasks):
    """
    Saves a list of tasks to the JSON file.

    Args:
        tasks (list): A list of Task objects.
    """
    with open(TASKS_FILE, 'w') as f:
        # Convert each Task object to its dictionary representation
        json.dump([task.to_dict() for task in tasks], f, indent=4)
    print("Tasks saved successfully!")

def load_tasks():
    """
    Loads tasks from the JSON file.

    Returns:
        list: A list of Task objects. Returns an empty list if the file doesn't exist.
    """
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r') as f:
            tasks_data = json.load(f)
            # Convert each dictionary back into a Task object
            return [Task.from_dict(data) for data in tasks_data]
    except (json.JSONDecodeError, FileNotFoundError):
        # Handle cases where the file is empty or corrupted
        return []

def add_task(tasks):
    """
    Prompts the user for task details and adds a new task to the list.

    Args:
        tasks (list): The current list of tasks.
    """
    print("\n--- Add a New Task ---")
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    category = input("Enter task category (e.g., Work, Personal, Urgent): ")
    
    new_task = Task(title, description, category)
    tasks.append(new_task)
    print(f"\nTask '{title}' added successfully!")

def view_tasks(tasks):
    """
    Displays all the tasks in the list.

    Args:
        tasks (list): The list of tasks to display.
    """
    print("\n--- Your To-Do List ---")
    if not tasks:
        print("Your to-do list is empty. Add a task to get started!")
        return

    for i, task in enumerate(tasks):
        print(f"{i + 1}. {task}")
    print("-------------------------")

def mark_task_completed(tasks):
    """
    Marks a specific task as completed.

    Args:
        tasks (list): The current list of tasks.
    """
    view_tasks(tasks)
    if not tasks:
        return
        
    try:
        task_num = int(input("Enter the task number to mark as completed: "))
        if 1 <= task_num <= len(tasks):
            tasks[task_num - 1].mark_completed()
            print(f"Task {task_num} marked as completed.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def delete_task(tasks):
    """
    Deletes a specific task from the list.

    Args:
        tasks (list): The current list of tasks.
    
    Returns:
        list: The updated list of tasks.
    """
    view_tasks(tasks)
    if not tasks:
        return tasks
        
    try:
        task_num = int(input("Enter the task number to delete: "))
        if 1 <= task_num <= len(tasks):
            removed_task = tasks.pop(task_num - 1)
            print(f"Task '{removed_task.title}' deleted successfully.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    return tasks

def main():
    """
    The main function to run the to-do list application.
    """
    tasks = load_tasks()
    
    print("====================================")
    print("  Welcome to Your To-Do List App  ")
    print("====================================")

    while True:
        print("\n--- Main Menu ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Save and Exit")
        
        choice = input("Choose an option (1-5): ")

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            mark_task_completed(tasks)
        elif choice == '4':
            tasks = delete_task(tasks)
        elif choice == '5':
            save_tasks(tasks)
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please select an option from 1 to 5.")

# This ensures the main function is called when the script is executed
if __name__ == "__main__":
    main()
