import json
from collections import UserDict


class Field:

    def __init__(self, value):
        self.__value = None
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.value == other.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


class Tag(Field):

    def __str__(self):
        return f"{self.value}"


class Note:

    def __init__(self, name: Field, content: Field, tag: Tag = None):
        self.name = name
        self.content = content
        self.tags = []
        if tag:
            self.tags.append(tag)
        self.status = True

    def __str__(self):
        return f"# '{self.name.value}': {self.content.value} (tegs: {', '.join(tag.value for tag in self.tags)})"

    def add_tag(self, tag):
        self.tags.append(tag)


class Notebook(UserDict):
    def add_note(self, note):
        self.data[note.name.value] = note
        return f"Note '{note.name}' added successfully."

    def __str__(self):
        return "\n".join(str(note) for note in self.data.values())

    def __repr__(self):
        return str(self)

    def save_json(self, file_path):
        json_data = {
            "tags": list(tags_list),
            "records": []
        }

        for note in self.data.values():
            json_record = {
                "name": note.name.value,
                "content": note.content.value,
                "tags": [tag.value for tag in note.tags],
                "status": note.status
            }
            json_data["records"].append(json_record)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=2, ensure_ascii=False)

    def load_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for record in data["records"]:
                    name = Field(record["name"])
                    content = Field(record["content"])
                    tags = [Tag(tag) for tag in record["tags"]]
                    note = Note(name, content)
                    for tag in tags:
                        note.add_tag(tag)
                    self.data[name.value] = note
                global tags_list
                tags_list = data["tags"]
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"The file {file_path} is missing or does not contain valid JSON data.")
            return None