import json
import uuid
import os
import firebase_admin
from firebase_admin import credentials, firestore

CONFIG_FILE = "config.json"

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def sent_file_to_base(token: str) -> bool:
    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            tasks_data = json.load(file)
        db.collection("users").document(token).set({"tasks_data": tasks_data})
        return True

    except Exception as e:
        print(f"\n\033[31mError saving to cloud: {e}\033[0m")
        return False


def get_or_create_user_token():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("token")
    else:
        new_token = str(uuid.uuid4())
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"token": new_token}, f, ensure_ascii=False, indent=4)
        return new_token


def get_user_token():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("token")
    except FileNotFoundError:
        return None

def load_tasks_from_cloud(token):
    try:
        doc = firestore.client().collection("users").document(token).get()
        if doc.exists:
            with open("tasks.json", "w", encoding="utf-8") as file:
                json.dump(doc.to_dict().get("tasks_data"), file, indent=4, ensure_ascii=False)
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    ...
