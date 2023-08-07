from collections import UserDict
from datetime import datetime
from re import match
# import pickle


class Field:
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    # Клас 'Field'- батьківський для таких класів як: (Name, Phone, Birthday, Email, Country, City, Street та House).
    # Коли ми створюємо екземпляри цих класів, значення, яке передає користувач зберігається в магічному методі '__init__'.

    @property
    def value(self):
        return self.__value
    # Магічний метод 'getter', який повертає значення, що ввів користувач.
  
    @value.setter
    def value(self, value):
        self.__value = value
    # Магічний метод 'setter', який предає введене користувачем значення у поле 'self.__value'.

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    ...
  

class Phone(Field):

    @Field.value.setter
    def value(self, value):
        if not match(r'\d{12}', value):
            raise ValueError
        self._Field__value = value
    # Магічний метод 'setter', який перевіряє на правильність введеного користувачем значення і записує у поле 'self.__value' значення, якщо
    # телефон був введений у форматі (XXXXXXXXXXXX), де Х - це цифра.

class Birthday(Field):

    @Field.value.setter
    def value(self, value):
        try:
            self._Field__value = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            print('Wrong format. Enter birthday in format dd.mm.YYYY. Days in range(31), month in range(12)')
            raise ValueError
        if self.value >= datetime.now().date():
            print('The user has not been born yet.')
            raise ValueError
        
    def __str__(self):
        return self.value.strftime('%d.%m.%Y')

    # @Field.value.setter
    # def value(self, value):
    #     try:
    #         self._Field__value = datetime.strptime(value, '%d.%m.%Y').date()
    #     except ValueError:
    #         print('Wrong format. Enter birthday in format dd.mm.YYYY')
    #         raise ValueError
    # Магічний метод 'setter', який перевіряє на правильність введеного користувачем значення і записує у поле 'self.__value' значення, якщо
    # дата народження була введена у форматі (DD.MM.YYYY).

class Email(Field):

    @Field.value.setter
    def value(self, value):
        if not match(r"[A-z][\dA-z\._]{1,}@[A-z]{2,}\.[A-z]{2,}", value):
            raise ValueError
        self._Field__value = value
    # Магічний метод 'setter', який перевіряє на правильність введеного користувачем значення і записує у поле 'self.__value' значення, якщо
    # email був введений у правильному форматі.

class Country(Field):

    @Field.value.setter
    def value(self, value):
        with open('countries.txt', 'r') as fh:
            readlines = fh.readlines()
            for line in readlines:
                if value.lower() == 'russia':
                    self._Field__value = 'a terrorist country'
                    return ''
                if value.capitalize() == line.replace('\n', ''):
                    self._Field__value = value
                    return ''
            raise ValueError
        
    # Магічний метод 'setter', який перевіряє на правильність введеного користувачем значення і записує у поле 'self.__value' значення, якщо
    # введена країна існує.

class City(Field):

    @Field.value.setter
    def value(self, value):
        if not match(r'^[A-z]{2,}$', value):
            raise ValueError
        self._Field__value = value
    # Магічний метод 'setter', який перевіряє на правильність введеного користувачем значення і записує у поле 'self.__value' значення, якщо
    # введений населений пункт складається тільки з літер та має довжину не менше 2-ох літер.

class Street(Field):

    @Field.value.setter
    def value(self, value):
        if not match(r'^[A-z\d\.\-\(\)\:\_\,\/ ]{2,}$', value):
            raise ValueError
        self._Field__value = value
    # Магічний метод 'setter', який перевіряє на правильність введеного користувачем значення і записує у поле 'self.__value' значення, якщо
    # назва введеної вулиці починається з літери та може містити тільки цифри та букви.

class House(Field):

    @Field.value.setter
    def value(self, value):
        if not match(r'[ A-z\d\-\\\/\.]{1,}', value):
            raise ValueError
        self._Field__value = value
    # Магічний метод 'setter', який перевіряє на правильність введеного користувачем значення і записує у поле 'self.__value' значення, якщо
    # введені назва/номер будинку складається з літер або цифр.


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None) -> None:
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.email = email
        self.address = ''

    def add_phone(self, phone: Phone) -> None:
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f'Phone {str(phone)} added successfully'
        return f"phone: {str(phone)} is present in contact's phones"
        
    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday
        return f'birthday added successfully'
    # метод добавдяє дату народження в поле self.birthday у стр форматі

    def add_email(self, email: Email):
        self.email = email
        return f'Email {str(email)} added successfully'
    
    def add_address(self, country: Country, city: City, street: Street = None, house: House = None):
        self.address = f'{country.value}/{city.value}/{street.value if street != None else "empty"}/{house.value if house != None else "empty"}'
        return 'Success'
    # метод добавляє адресу проживання у поле self.address
    
    def __str__(self) -> str:
        return f"User: {self.name} | phone(s): {', '.join(str(p) for p in self.phones)} | email: {self.email if self.email != None else ''} | address: {self.address} | bithday: {self.birthday if self.birthday != None else ''}"
    
class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record
        return f'User {str(record.name)} successfully added'
    
    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())