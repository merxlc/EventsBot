import json
import random

class IdInfo:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
    def __repr__(self):
        return repr(self.__dict__)

class Event:
    def __init__(self, category, name, description, time, ids):
        self.category = category
        self.name = name
        self.description = description
        self.time = time
        self.ids = ids
        self.uid = random.randint(1, 1000000)
    def __repr__(self):
        final = f'\n<{self.category}> {self.name}: ({self.uid} at {self.time})\n'
        final += f'| {self.description}\n'
        final += f'| {self.ids.__repr__()}'
        return final
    def ser(self):
        return {
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "time": self.time,
            "uid": self.uid,
            "ids": self.ids.__dict__
        }
    def deser(data):
        new = Event("", "", "", "", "")
        new.__dict__ = data
        new.__dict__["ids"] = IdInfo(**new.__dict__["ids"])
        return new
    def save_to_file(self):
        with open("events.json", "r") as file:
            data = json.loads(file.read())
        cat = data[self.category]
        cat[self.uid] = self.ser()
        with open("events.json", "w") as file:
            file.write(json.dumps(data, indent=4))
    def delete(self):
        with open("events.json", "r") as file:
            data = json.loads(file.read())
        cat = data[self.category]
        del cat[str(self.uid)]
        with open("events.json", "w") as file:
            file.write(json.dumps(data, indent=4))
    def delete_from_file(category, uid):
        with open("events.json", "r") as file:
            data = json.loads(file.read())
        cat = data[category]
        del cat[str(uid)]
        with open("events.json", "w") as file:
            file.write(json.dumps(data, indent=4))
    def load():
        final = {}
        with open("events.json", "r") as file:
            data = json.loads(file.read())
        for category in data:
            final[category] = []
            for event in data[category]:
                final[category].append(Event.deser(data[category][event]))
        return final
    def find_prop(**props):
        events = Event.load()
        all_events = []
        for category in events:
            for event in events[category]:
                all_events.append(event)
        for event in all_events:
            ids = event.ids
            passing = True
            for condition in props:
                if ids.__dict__[condition] != props[condition]:
                    passing = False
            if passing:
                return event