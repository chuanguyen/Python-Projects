import json
import requests

response = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = json.loads(response.text)

todos_by_user = {}

for todo in todos:
    if todo["completed"]:
        try:
            todos_by_user[todo["userId"]] += 1
        except KeyError:
            todos_by_user[todo["userId"]] = 1

top_users = sorted(todos_by_user.items(), key=lambda x: x[1], reverse=True)

print(top_users)

obj = 3 + 8j

def encode_complex(obj):
    if isinstance(obj, complex):
        return (obj.real, obj.imag)
    else:
        type_name = obj.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

obj_json = json.dumps(obj, default=encode_complex)
print(json.loads(obj_json))
