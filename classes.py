from collections import UserDict
from datetime import datetime
import re


class Field:
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
       
    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    ...


# Для перевірки на правильність введення номеру телефону, використовуємо регулярний вираз, що українські номери 
# обов'язково мають починатися з '+380' і ще 9 цифр. 
class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not re.match(r'^\+380\d{9}$', value):
            print('Wrong format. Phone number should be in the format +380XXXXXXXXX.')
            raise ValueError
        self.__value = value


# Для перевірки на правильність введення дати народження, необхідно щоб ми записували ці об'єкти як об'єкти
# типу datetime у форматі '%d.%m.%Y'. Це необхідно щоб одразу запобігти введенню 'дивних' даних на кшталт
# "2/2/42", '50.20.2000' чи навіть '29.02.2001'.
# Також варто уникати дат народження, які є у майбутньому. Це враховано у методі add_birthday класу Record.
class Birthday(Field):
    @property
    def value(self):
        return self.__value
        
    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            print('Wrong format. Enter birthday in format dd.mm.YYYY. Days in range(31), month in range(12)')
            raise ValueError
        
    def __str__(self):
        return self.value.strftime('%d-%m-%Y')


# Для перевірки на правильність введення email пропоную використати регулярний вираз, який був у нас у автоперевірці.
class Email(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not re.match(r'[A-Za-z]{1}[\w\.]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}\b', value):
            print('Wrong format. Email should be in the format xxxxxx@xxx.xx')
            raise ValueError
        self.__value = value


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday
        self.email = email

    # Функція додає телефон до списку телефонів користувача. Перевіряє чи вже введено такий телефон раніше.
    def add_phone(self, phone: Phone) -> None:
        if phone.value not in self.phones:
            self.phones.append(phone)
            return f"phone {phone} was added to contact {self.name}"
        return f"phone: {phone} is already registered for user {self.name}"

    # Функція додає дату народження користувача. Враховано, що дата народження не може бути у майбутньому.
    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday
        if self.birthday.value >= datetime.now().date():
            return f'The user has not yet been born'
        return f'Birthday for user {self.name} was added successfully'

    # Функція додає email користувача. Перевірка на правильність прописана у класі Email.
    def add_email(self, email: Email):
        self.email = email
        return f'E-mail for user {self.name} was added successfully'
    
    # Рядкове представлення для одного запису у contact_book 
    def __str__(self) -> str:
        return f"User: {self.name} | phones: {', '.join(str(p) for p in self.phones)} | birthday: {self.birthday} " \
               f"| email: {self.email}"
    

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record.name} was added successfully"

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:  # Рядкове представлення для усіх записів у contact_book
        return "\n".join(str(r) for r in self.data.values())
