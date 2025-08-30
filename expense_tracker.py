# Personal Expense Tracker
import csv
from datetime import datetime
import os  # Used to check if the file exists

# --- Configuration ---
# Use a constant for the filename for easy modification.
FILENAME = "expenses.csv"
# Define the headers for our CSV file.
HEADERS = ["date", "amount", "category", "description"]

# --- Helper Functions ---

def initialize_file():
    """Creates the CSV file with headers if it doesn't exist."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
        print(f"'{FILENAME}' created for storing expenses.")

def load_expenses():
    """Loads all expenses from the CSV file into a list of dictionaries."""
    initialize_file()  # Ensure file exists before reading
    expenses = []
    try:
        with open(FILENAME, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert amount back to float
                row['amount'] = float(row['amount'])
                expenses.append(row)
    except Exception as e:
        print(f"Error loading expenses: {e}")
    return expenses

def save_expenses(expenses):
    """Saves the list of expenses back to the CSV file."""
    try:
        with open(FILENAME, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(expenses)
    except Exception as e:
        print(f"Error saving expenses: {e}")

# --- Core Features ---

def add_expense(expenses):
    """Prompts the user to add a new expense and appends it to the list."""
    print("\n--- Add New Expense ---")
    
    # Get Date
    date_str = input("Enter date (YYYY-MM-DD) or leave blank for today: ").strip()
    if not date_str:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        # Validate date format
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            date = date_str
        except ValueError:
            print("Invalid date format. Using today's date.")
            date = datetime.now().strftime("%Y-%m-%d")
            
    # Get Amount
    while True:
        try:
            amount = float(input("Enter amount (e.g., 50.75): "))
            if amount <= 0:
                print("Amount must be positive.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")

    # Get Category
    category = input("Enter category (e.g., Food, Transport, Rent, Entertainment): ").strip().title()

    # Get Description
    description = input("Enter a brief description: ").strip()

    # Create and add the expense
    new_expense = {
        "date": date,
        "amount": amount,
        "category": category,
        "description": description
    }
    expenses.append(new_expense)
    save_expenses(expenses) # Save immediately
    print("\nExpense added successfully!")
    print(f"  Date: {date}, Amount: ₹{amount:.2f}, Category: {category}, Desc: {description}")


def view_summaries(expenses):
    """Displays summaries of expenses."""
    if not expenses:
        print("\nNo expenses logged yet. Please add an expense first.")
        return

    print("\n--- Expense Summaries ---")
    
    # 1. Total Overall Spending
    total_spending = sum(item['amount'] for item in expenses)
    print(f"\nTotal Overall Spending: ₹{total_spending:.2f}")

    # 2. Spending by Category
    print("\nSpending by Category:")
    spending_by_category = {}
    for expense in expenses:
        category = expense['category']
        amount = expense['amount']
        if category in spending_by_category:
            spending_by_category[category] += amount
        else:
            spending_by_category[category] = amount
    
    # Print sorted categories for better readability
    for category, total in sorted(spending_by_category.items()):
        print(f"  - {category}: ₹{total:.2f}")

    # 3. Spending over time (Monthly)
    print("\nSpending by Month:")
    spending_by_month = {}
    for expense in expenses:
        # Extract month in YYYY-MM format
        month = datetime.strptime(expense['date'], "%Y-%m-%d").strftime("%Y-%m")
        amount = expense['amount']
        if month in spending_by_month:
            spending_by_month[month] += amount
        else:
            spending_by_month[month] = amount

    for month, total in sorted(spending_by_month.items()):
        print(f"  - {month}: ₹{total:.2f}")



def delete_expense(expenses):
    """Lists expenses and allows the user to delete one."""
    if not expenses:
        print("\nNo expenses to delete.")
        return

    print("\n--- Delete an Expense ---")
    # Display all expenses with an index
    for i, expense in enumerate(expenses):
        print(f"{i + 1}. {expense['date']} - {expense['category']} - ₹{expense['amount']:.2f} ({expense['description']})")

    while True:
        try:
            choice = int(input("\nEnter the number of the expense to delete (or 0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(expenses):
                deleted_expense = expenses.pop(choice - 1)
                save_expenses(expenses)
                print(f"Successfully deleted expense: {deleted_expense['description']}")
                break
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
def plot_expenses_by_category(expenses):
    """Generates and displays a bar chart of spending by category."""
    print("\n--- Generating Expense Plot ---")
    if not expenses:
        print("No data to plot.")
        return
        
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n'matplotlib' library not found.")
        print("Please install it to use this feature: pip install matplotlib")
        return

    # Aggregate data
    spending_by_category = {}
    for expense in expenses:
        category = expense['category']
        amount = expense['amount']
        spending_by_category[category] = spending_by_category.get(category, 0) + amount

    if not spending_by_category:
        print("No categories found to plot.")
        return

    # Sort data for a cleaner plot
    sorted_categories = sorted(spending_by_category.items(), key=lambda item: item[1], reverse=True)
    categories = [item[0] for item in sorted_categories]
    amounts = [item[1] for item in sorted_categories]

    # Create plot
    plt.figure(figsize=(10, 6))
    plt.bar(categories, amounts, color='skyblue')
    plt.xlabel("Category")
    plt.ylabel("Amount Spent (₹)")
    plt.title("Total Spending by Category")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() # Adjust layout to make room for rotated labels
    
    print("Displaying plot. Close the plot window to continue.")
    plt.show()


# --- Main Application Loop ---

def main():
    """The main function that runs the user menu and application loop."""
    expenses = load_expenses()
    
    print("\nWelcome to your Personal Expense Tracker!")
    
    while True:
        print("\n--- Main Menu ---")
        print("1. Add an Expense")
        print("2. View Expense Summaries")
        print("3. Delete an Expense ")
        print("4. Plot Expenses by Category ")
        print("5. Exit")

        choice = input("Please choose an option (1-5): ").strip()

        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            view_summaries(expenses)
        elif choice == '3':
            delete_expense(expenses)
        elif choice == '4':
            plot_expenses_by_category(expenses)
        elif choice == '5':
            # Data is already saved after each addition/deletion
            print("Goodbye! Your expenses are saved.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

# --- Entry point of the script ---
if __name__ == "__main__":
    main()