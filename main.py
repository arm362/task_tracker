import os
import json
from datetime import datetime
from typing import Any


def clean_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu() -> None:
    print("1.Tasks list")
    print("2.Add new task")
    print("3.Delete task")
    print("4.Update task")

def show_tasks() -> None:
    with open("tasks.json", "r", encoding="utf-8") as file:
        data: dict[str, Any] = json.load(file)
    for task_id, task in data["tasks"].items(): 
        print(f"\nTask id: {task_id}")
        print(f"Task name: {task['name']}")
        print(f"Task description: {task['description']}")
        print(f"Task status: {task['status']}")
        print(f"Task created date and time: {task['createdAt']}")
        print(f"Task last updated date and time: {task['updatedAt']}")
        print("\n=====================================================\n")

def add_task() -> None:
    name = input("\n Write task name: ")
    description = input("\nWrite task description: ")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists("tasks.json"):
         with open("tasks.json", "r", encoding="utf-8") as file:
            try:
                base_data: dict[str, Any] = json.load(file)
            except json.JSONDecodeError:
                base_data: dict[str, Any] = {"next_id": 1, "tasks": {}}
    else:
        base_data: dict[str, Any] = {"next_id": 1, "tasks": {}}

    task_id: str = str(base_data["next_id"])
    
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

def delete_task() -> None:
    task_id = input("Write deleted task id: ")
    if os.path.exists("tasks.json"):
        try:
            with open("tasks.json", "r", encoding="utf-8") as file:
                data: dict[str, Any] = json.load(file)
                data["tasks"].pop(task_id)

            with open("tasks.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"\n[\033[32m✓\033[0m] Task deleted!")
        except KeyError:
            print("\n\033[31mYou don't have a task with this id\033[0m")
    else:
        print("\n\033[31mYou don't have any tasks\033[0m")

def update_task() -> None:
    task_id = input("Write updated task id: ")
    if os.path.exists("tasks.json"):
        try:
            with open("tasks.json", "r", encoding="utf-8") as file:
                data: dict[str, Any] = json.load(file)
                print("\nWhat would you like to update?")
                print("1.name")
                print("2.description")
                print("3.status")
                choice = input("\nEnter your choice: ")
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                match choice:
                    case '1':
                        new_name = input("Write new name: ")
                        data["tasks"][task_id]["name"] = new_name
                        data["tasks"][task_id]["updatedAt"] = current_time
                        with open("tasks.json", "w", encoding="utf-8") as new_file:
                            json.dump(data, new_file, indent=4, ensure_ascii=False)
                        print("\n\033[32mTask name is updated\033[0m!")
                    case '2':
                        new_description = input("Write new description: ")
                        data["tasks"][task_id]["description"] = new_description
                        data["tasks"][task_id]["updatedAt"] = current_time
                        with open("tasks.json", "w", encoding="utf-8") as new_file:
                            json.dump(data, new_file, indent=4, ensure_ascii=False)
                        print("\n\033[32mTask description is updated\033[0m!")
                    case '3':
                        new_status = input("\nWrite new status(todo/in-progress/done): ")
                        if new_status == 'todo' or new_status == 'in-progress' or new_status == 'done':
                            data["tasks"][task_id]["status"] = new_status
                            data["tasks"][task_id]["updatedAt"] = current_time
                            with open("tasks.json", "w", encoding="utf-8") as new_file:
                                json.dump(data, new_file, indent=4, ensure_ascii=False)
                            print("\n\033[32mTask status is updated\033[0m!")
                        else:
                            print("\033[31mWrite only this status(todo/in-progress/done)\033[0m")

        except KeyError:
            print("\n\033[31mYou don't have a task with this id\033[0m")
    else:
        print("\n\033[31mYou don't have tasks\033[0m")

def main() -> None:
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
                    print("\033[31mYou don't have any tasks\033[0m")
            case '2':
                clean_terminal()
                add_task()
            case '3':
                clean_terminal()
                delete_task()
            case '4':
                clean_terminal()
                update_task()

if __name__ == "__main__":
    main()
