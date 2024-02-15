# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# After successful login
if curr_user == "admin":
    is_admin = True
else:
    is_admin = False

# New Functions
def reg_user(username_password):
    '''Add a new user to the user.txt file'''
    while True:
        # - Request input of a new username
        new_username = input("New Username: ")

        # Check if the username already exists
        if new_username in username_password:
            print("Username already exists. Please choose a different username.")
        else:
            break
    
    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do not match")

def add_task(task_list, username_password):
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following:
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task, and
    - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

def view_all(task_list):
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labeling)'''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

def view_mine(task_list, curr_user):
    '''Reads the task from task.txt file and prints to the console in the 
       format of Output 2 presented in the task pdf (i.e. includes spacing
       and labeling)'''
    print("Your Tasks:")
    for i, t in enumerate(task_list, 1):
        if t['username'] == curr_user:
            disp_str = f"Task {i}:\n"
            disp_str += f"Title: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"Completed: \t {t['completed']}\n"
            print(disp_str)

def mark_task_complete(task_list, task_number):
    index = task_number - 1  # Adjust for 0-based index
    if 0 <= index < len(task_list):
        response = input(f"Do you want to mark Task {task_number} as complete (c), or mark it for edit (e)? ").lower()
        if response == 'c':
            task_list[index]['completed'] = True
            print(f"Task {task_number} marked as complete.")
        elif response == 'e':
            edit_task(task_list, task_number)
        else:
            print("Invalid response. Task not updated.")
    else:
        print("Invalid task number.")

def edit_task(task_list, task_number):
    index = task_number - 1  # Adjust for 0-based index
    if 0 <= index < len(task_list) and not task_list[index]['completed']:
        new_username = input("Enter new username (press Enter to keep current): ")
        new_due_date = input("Enter new due date (YYYY-MM-DD) (press Enter to keep current): ")

        # Update task details if user entered new values
        if new_username:
            task_list[index]['username'] = new_username
        if new_due_date:
            try:
                task_list[index]['due_date'] = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
            except ValueError:
                print("Invalid date format. Task not updated.")

        print(f"Task {task_number} updated.")
    else:
        print("Invalid task number or task is already completed.")

def generate_task_report(task_list):
    total_tasks = len(task_list)
    completed_tasks = sum(task['completed'] for task in task_list)
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < date.today())

    with open("task_overview.txt", "w") as report_file:
        report_file.write("Task Overview Report\n\n")
        report_file.write(f"Total tasks: {total_tasks}\n")
        report_file.write(f"Completed tasks: {completed_tasks}\n")
        report_file.write(f"Incomplete tasks: {incomplete_tasks}\n")
        report_file.write(f"Overdue tasks: {overdue_tasks}\n")
        report_file.write(f"Percentage of incomplete tasks: {incomplete_tasks / total_tasks * 100:.2f}%\n")
        report_file.write(f"Percentage of overdue tasks: {overdue_tasks / total_tasks * 100:.2f}%\n")

def generate_user_report(task_list, username_password):
    total_users = len(username_password)
    total_tasks = len(task_list)

    with open("user_overview.txt", "w") as report_file:
        report_file.write("User Overview Report\n\n")
        report_file.write(f"Total users: {total_users}\n")
        report_file.write(f"Total tasks: {total_tasks}\n")

        for username in username_password.keys():
            user_tasks = [task for task in task_list if task['username'] == username]
            total_user_tasks = len(user_tasks)
            completed_user_tasks = sum(task['completed'] for task in user_tasks)
            incomplete_user_tasks = total_user_tasks - completed_user_tasks
            overdue_user_tasks = sum(1 for task in user_tasks if not task['completed'] and task['due_date'].date() < date.today())

            report_file.write(f"\nUser: {username}\n")
            report_file.write(f"Total tasks assigned: {total_user_tasks}\n")
            report_file.write(f"Percentage of total tasks assigned: {total_user_tasks / total_tasks * 100:.2f}%\n")
            report_file.write(f"Percentage of completed tasks: {completed_user_tasks / total_user_tasks * 100:.2f}%\n")
            report_file.write(f"Percentage of incomplete tasks: {incomplete_user_tasks / total_user_tasks * 100:.2f}%\n")
            report_file.write(f"Percentage of overdue tasks: {overdue_user_tasks / total_user_tasks * 100:.2f}%\n")

def display_statistics(task_list, username_password):
    # Check if the report files exist, if not, generate them
    if not os.path.exists("tasks.txt") or not os.path.exists("user.txt"):
        print("Data files not found. Generating data files...")
        generate_task_report(task_list)
        generate_user_report(task_list, username_password)

    # Display statistics from the data files
    with open("tasks.txt", "r") as task_file:
        task_data = task_file.read().split("\n")
        num_tasks = len([t for t in task_data if t != ""])
        completed_tasks = sum(1 for t in task_data if t.endswith("Yes"))
        incomplete_tasks = num_tasks - completed_tasks
        overdue_tasks = sum(1 for t in task_data if not t.endswith("Yes") and datetime.strptime(t.split(";")[3], DATETIME_STRING_FORMAT).date() < date.today())

        print("Task Overview Report:")
        print(f"Total tasks: {num_tasks}")
        print(f"Completed tasks: {completed_tasks}")
        print(f"Incomplete tasks: {incomplete_tasks}")
        print(f"Overdue tasks: {overdue_tasks}")
        print(f"Percentage of incomplete tasks: {incomplete_tasks / num_tasks * 100:.2f}%")
        print(f"Percentage of overdue tasks: {overdue_tasks / num_tasks * 100:.2f}%")

    with open("user.txt", "r") as user_file:
        user_data = user_file.read().split("\n")
        num_users = len([u for u in user_data if u != ""])

        print("\nUser Overview Report:")
        print(f"Total users: {num_users}")
        print(f"Total tasks: {num_tasks}")

        for username in username_password.keys():
            user_tasks = [task for task in task_list if task['username'] == username]
            total_user_tasks = len(user_tasks)
            completed_user_tasks = sum(task['completed'] for task in user_tasks)
            incomplete_user_tasks = total_user_tasks - completed_user_tasks
            overdue_user_tasks = sum(1 for task in user_tasks if not task['completed'] and task['due_date'].date() < date.today())

            print(f"\nUser: {username}")
            print(f"Total tasks assigned: {total_user_tasks}")
            print(f"Percentage of total tasks assigned: {total_user_tasks / num_tasks * 100:.2f}%")
            print(f"Percentage of completed tasks: {completed_user_tasks / total_user_tasks * 100:.2f}%")
            print(f"Percentage of incomplete tasks: {incomplete_user_tasks / total_user_tasks * 100:.2f}%")
            print(f"Percentage of overdue tasks: {overdue_user_tasks / total_user_tasks * 100:.2f}%")

# Main Loop
while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
gr - Generate reports
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user(username_password)

    elif menu == 'a':
        add_task(task_list, username_password)

    elif menu == 'va':
        view_all(task_list)

    elif menu == 'vm':
        view_mine(task_list, curr_user)
        
        # Ask the user to select a task or return to the main menu
        selected_task = input("Enter task number to select or -1 to return to the main menu: ")
        if selected_task == '-1':
            continue

        # Handle task selection
        try:
            selected_task = int(selected_task)
            if 1 <= selected_task <= len(task_list):
                mark_task_complete(task_list, selected_task)
            else:
                print("Invalid task number. Returning to main menu.")
        except ValueError:
            print("Invalid input. Returning to main menu.")
    
    elif menu == 'gr' and is_admin:  # Check if user is admin
        generate_task_report(task_list)
        generate_user_report(task_list, username_password)
        print("Reports generated successfully.")

    elif menu == 'ds' and is_admin:  # Check if user is admin
        display_statistics(task_list, username_password)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice. Please Try again.")