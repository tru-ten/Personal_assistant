import json
from collections import UserDict


class Field:

    def __init__(self, value):
        self.value = value

    """def __eq__(self, other):
        if isinstance(other, Field):
            return self.value == other.value"""

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)


class Tag(Field):
    ...


class Note:

    def __init__(self, name: Field, content: Field, tag: Tag = None) -> None:
        self.name = name
        self.content = content
        self.tags = []
        if tag:
            self.tags.append(tag)
        self.status = True

    def __str__(self):
        return f"'{self.name.value}' {self.content.value} (tegs: {', '.join(tag.value for tag in self.tags)}) статус: {str(self.status)} "

    def add_tag(self, tag):
        self.tags.append(tag)


class Notebook(UserDict):
    def __init__(self):
        self.data = {}
        self.tags_list = []
        
    def add_note(self, note):
        self.data[note.name.value] = note
        return f"Note '{note.name}' added successfully."

    def __str__(self):
        return "\n".join(str(note) for note in self.data.values())

    def __repr__(self):
        return str(self)
    
    
    def search_in_notes(self, option, search: str):
        result = []
        for record in self.data.values():
            if str(search).lower() in str(getattr(record, option)).lower():
                result.append(record)
        return result

    def save_json(self, file_path):
        json_data = {
            "tags": self.tags_list,
            "notes": []
        }

        for note in self.data.values():
            json_note = {
                "name": note.name.value,
                "content": note.content.value,
                "tags": [tag.value for tag in note.tags],
                "status": note.status
            }
            json_data["notes"].append(json_note)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=2, ensure_ascii=False)

    def load_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for record in data["notes"]:
                    name = Field(record["name"])
                    content = Field(record["content"])
                    tags = [Tag(tag) for tag in record["tags"]]
                    note = Note(name, content)
                    for tag in tags:
                        note.add_tag(tag)
                    self.data[name.value] = note
                self.tags_list = data["tags"]
        except (FileNotFoundError):
            print(f"The file {file_path} is missing or does not contain valid JSON data.")