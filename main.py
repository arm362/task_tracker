import os
import json
from datetime import datetime

def clean_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    print("1.My tasks")
    print("2.Add new task")
    print("3.Delete task")
    print("4.Update task")

def show_tasks():
    with open("tasks.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    for task_id, task in data["tasks"].items(): 
        print(f"Task id: {task_id}")
        print(f"Task name: {task['name']}")
        print(f"Task description: {task['description']}")
        print(f"Task status: {task['status']}")
        print(f"Task created date and time: {task['createdAt']}")
        print(f"Task last updated date and time: {task['updatedAt']}")
        print("\n=====================================================\n")

def add_task():
    name = input("\n Write task name: ")
    description = input("\nWrite task description: ")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists("tasks.json"):
         with open("tasks.json", "r", encoding="utf-8") as file:
            try:
                base_data = json.load(file)
            except json.JSONDecodeError:
                base_data = {"next_id": 1, "tasks": {}}
    else:
        base_data = {"next_id": 1, "tasks": {}}

    task_id = str(base_data["next_id"])
    
    new_task = {
        "name": name,
        "description": description,
        "status": "todo",
        "createdAt": current_time,
        "updatedAt": current_time
    }

    base_data["tasks"][task_id] = new_task

    base_data["next_id"] += 1

    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(base_data, file, indent=4, ensure_ascii=False)

    print(f"\n[\033[32m✓\033[0m] Task created!")

def delete_task():
    task_id = input("Write deleted task id: ")
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        print("You don't have any tasks")

def main(): 
    while True:
        print("\n============== \033[1;96mTask Tracker\033[0m ==============")    
        print("\n" "         \033[1mWhat do you want to do?\033[0m\n")
        show_menu()
        choice = input("\nEnter your choice: ").strip()

        match choice:
            case '1':
                clean_terminal()
                try:
                    show_tasks()
                except FileNotFoundError:
                    print("You don't have any tasks")
            case '2':
                clean_terminal()
                add_task()
            case '3':
                clean_terminal()
                delete_task()

if __name__ == "__main__":
    main()
