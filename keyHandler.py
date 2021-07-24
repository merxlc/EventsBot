import json

def load_keys():
    with open('keys.json', 'r') as file:
        return json.loads(file.read())

def save_keys(keydict):
    with open('keys.json', 'w') as file:
        file.write(json.dumps(keydict, indent=4))

def get_keys(user):
    keys = load_keys()
    try:
        return keys[str(user)]
    except Exception:
        return 0

def add_key(user):
    keys = load_keys()
    if user in keys.keys():
        keys[user] += 1
    else:
        keys[user] = 1
    save_keys(keys)