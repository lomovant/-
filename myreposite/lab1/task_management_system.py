# Initial task dictionary
tasks = {
    "Write report": "in progress",
    "Check email": "done",
    "Prepare presentation": "pending",
    "Call client": "pending",
    "Develop project plan": "in progress"
}

def add_task(task_name, status="pending"):
    """Adds a new task with a status (default 'pending')."""
    if task_name not in tasks:
        tasks[task_name] = status
    else:
        print(f"Task '{task_name}' already exists.")

def remove_task(task_name):
    """Removes a task if it exists."""
    if task_name in tasks:
        del tasks[task_name]
    else:
        print(f"Task '{task_name}' not found.")

def update_task_status(task_name, new_status):
    """Updates the status of an existing task."""
    if task_name in tasks:
        tasks[task_name] = new_status
    else:
        print(f"Task '{task_name}' not found.")

# Test operations
add_task("Buy office supplies")       # Add a new task
update_task_status("Write report", "done")  # Update status
remove_task("Check email")            # Remove a task

# List of tasks with status "pending"
pending_tasks = [task for task, status in tasks.items() if status == "pending"]

# Output results
print("Task list:", tasks)
print("Pending tasks:", pending_tasks)
