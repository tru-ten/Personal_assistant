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
    
    def __str__(self):
        return str(self.value)
    

class Note:

    def __init__(self, name: Field, content: Field, tag: Tag = None) -> None:
        self.name = name
        self.content = content
        self.tags = []
        if tag:
            self.tags.append(tag)
        self.status = True


    def __str__(self):
        if self.tags is None:
            self.tags = ""
        tags_str = ', '.join(tag.value for tag in self.tags)
        return f"'{self.name.value}' {self.content.value} (tegs: {tags_str}) status: {str(self.status)} "
    
    def add_tag_in_tags(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)
        else:
            print(f"Tag {tag} already exists")
    
    def delete_tag_from_note(self, note, tag):
        note.tags.remove(tag)
        print(f"Tag {tag} deleted from note {note.name}")
    
    def remove_tag(self, tag):
        try:
            self.tags.remove(tag)
        except ValueError:
            print('There is no such tag in this note\n')
    
    def get_tag_values(self):
        return self.tags_list
    
    def get_tags(note):
        return note.tags


class Notebook(UserDict):

    def __init__(self):
        self.data = {}
        self.tags_list = []
    
    def __str__(self):
        return "\n".join(str(note) for note in self.data.values())

    def __repr__(self):
        return str(self)
    
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
        if note.status:
            status = False
        else:
            status = True
        setattr(note, "status", status) 
        print(f"Note status updated: {note}")

    def sort_by_tags(self):
        notes = list(self.data.values())
        notes.sort(key=lambda note: note.tags)
        return notes
    
    def add_tag_note(self, new_tag):
        if new_tag.value not in self.tags_list:
            self.tags_list.append(new_tag.value)
            print(f"Tag {new_tag.value} added")
        else:
            print(f"Tag {new_tag.value} already exists")
    
    def delete_tag_from_note(self, note, tag):
        if tag in note.tags:
            note.tags.remove(tag)
            print(f"Tag {tag} deleted from note {note.name}")
        else:
            print(f"Tag {tag} not found in note {note.name}")
    
    def search_in_tags(self, search):
        tags = []
        for tag in self.tags_list:
            if search.lower() in tag.lower():
                tags.append(tag)
        return tags
    
    def get_tag_values(self):
        return self.tags_list

    def iterator(self, et_list, n):
        count = 0
        page = ""
        for note in et_list:
            page += (str(note)) + "\n"
            count += 1
            if count >= n:
                yield page
                count = 0
                page = ""
        if page:
            yield page
        
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
            Notebook.save_json(self, file_path)
            print("Notebook.json file is created")