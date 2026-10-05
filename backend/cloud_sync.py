import json
import requests

API_KEY = "AIzaSyB7KgUBAGWdYpvzMVSz8nzfkt726tgAFAo"
PROJECT_ID = "task-tracker-6565"

def get_new_token() -> str | None:
  url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"

  response = requests.post(url, json={"returnSecureToken": True})

  if response.status_code == 200:
    return response.json().get("localId")

  print("Error to get token:", response.text)
  return None

def sent_file_to_base(token):
    with open("tasks.json", "r", encoding="utf-8") as file:
        data: dict[str, Any] = json.load(file)

  url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/users/{token}?updateMask.fieldPaths=tasks_data"

  payload = {"fields": {"tasks_data": {"stringValue": tasks_content}}}

  response = requests.patch(url, json=payload)

  return response.status_code == 200
  
if __name__ == "__main__":
  token = get_new_token()

  if token:
    success = send_file_to_base(token)

    if success:
      print(f"SUCCESS! Your token: {token}")
    else:
      print("Error, tasks not save.")
