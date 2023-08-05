from collections import UserDict

class Field:
    def __init__(self, value) -> None:
        self.value = value

class Name(Field):
    ...

class Phone(Field):
    ...

class Birthday(Field):
    ...

class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phone: Phone) -> None:
        if phone.value not in self.phones:
            self.phones.append(phone)

class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record
