import json
from collections import UserDict


class Field:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        if isinstance(other, Field):
            return self.value == other.value
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value


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
        return f"'{self.name.value}' {self.content.value} (tegs: {', '.join(tag.value for tag in self.tags)}) status: {str(self.status)} "
    
    def add_tag_in_tags(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)
        else:
            print(f"Tag {tag} already exists")
    
    def remove_tag(self, tag):
        self.tags.remove(tag)

class Notebook(UserDict):
    def __init__(self):
        self.data = {}
        self.tags_list = []
    
    def __str__(self):
        return "\n".join(str(note) for note in self.data.values())

    def __repr__(self):
        return str(self)
    
    """def __eq__(self, other):
        if isinstance(other, Field):
            return self.value == other.value"""
        
    def add_note(self, note):
        self.data[note.name.value] = note
        return f"Note '{note}' added successfully."
    
    def search_in_notes(self, field, search: str):
        result = []
        for note in self.data.values():
            if str(search).lower() in str(getattr(note, field)).lower():
                result.append(note)
        return result
    
    def delete_in_note(self, note):
        del self.data[note.name.value]
        print("Record deleted")
    
    def edit_in_note(self, note, field, new_value):
        setattr(note, field, new_value)
        print(f"Note updated: {note}")

    def edit_status_in_note(self, note):
        setattr(note, "status", False) 
        print(f"Note status updated: {note}")

    def sort_by_tags(self):
        notes = list(self.data.values())
        notes.sort(key=lambda note: note.tags)
        return notes
    
    def add_tag_note(self, new_tag):
        if new_tag.value not in self.tags_list:
            self.tags_list.append(new_tag.value)
            print(f"Тег {new_tag.value} додано")
        else:
            print(f"Тег {new_tag.value} вже існує")
    
    def search_in_tags(self, search):
        tags = []
        for tag in self.tags_list:
            if search.lower() in tag.lower():
                tags.append(tag)
        return tags
    
    def get_tag_values(self):
        return self.tags_list

    def add_tag_note(self, new_tag):
        if new_tag.value not in self.tags_list:
            self.tags_list.append(new_tag.value)
            print(f"Тег {new_tag.value} додано")
        else:
            print(f"Тег {new_tag.value} вже існує")
    
    
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
                        note.add_tag_in_tags(tag)
                    self.data[name.value] = note
                self.tags_list = data["tags"]
        except (FileNotFoundError):
            print(f"The file {file_path} is missing or does not contain valid JSON data.")