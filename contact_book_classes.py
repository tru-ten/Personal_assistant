from collections import UserDict, defaultdict
from datetime import datetime
import pickle  # модуль для зберігання та читання інформації.
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

    @Field.value.setter
    def value(self, value):
        if not re.match(r'^\+380\d{9}$', value):
            print('Wrong format. Phone number should be in the format +380XXXXXXXXX.')
            raise ValueError
        self._Field__value = value


# Для перевірки на правильність введення дати народження, необхідно щоб ми записували ці об'єкти як об'єкти
# типу datetime у форматі '%d.%m.%Y'. Це необхідно щоб одразу запобігти введенню 'дивних' даних на кшталт
# "2/2/42", '50.20.2000' чи навіть '29.02.2001'.
# Також варто уникати дат народження, які є у майбутньому. Це враховано у методі add_birthday класу Record.
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


# Для перевірки на правильність введення email пропоную використати регулярний вираз, який був у нас у автоперевірці.
class Email(Field):

    @Field.value.setter
    def value(self, value):
        if not re.match(r'[A-Za-z]{1}[\w.]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}\b', value):
            print('Wrong format. Email should be in the format xxxxxx@xxx.xx')
            raise ValueError
        self._Field__value = value


class Country(Field):

    @Field.value.setter
    def value(self, value):
        with open('countries.txt', 'r') as fh:
            readlines = fh.readlines()
            for line in readlines:
                if value.lower() == 'russia':
                    self._Field__value = 'a terrorist country'
                    return ''
                elif value.lower() == line.lower().strip():
                    lst_value = value.lower().strip().split(' ')
                    capitalize_value = [i.capitalize() for i in lst_value]
                    self._Field__value = ' '.join(capitalize_value)
                    return ''
            raise ValueError
        
    # Магічний метод 'setter', який перевіряє на правильність введеного користувачем значення і записує у поле 'self.__value' значення, якщо
    # введена країна існує.

class City(Field):

    @Field.value.setter
    def value(self, value):
        if not re.match(r'^[A-z]{2,}$', value):
            raise ValueError
        self._Field__value = value
    # Магічний метод 'setter', який перевіряє на правильність введеного користувачем значення і записує у поле 'self.__value' значення, якщо
    # введений населений пункт складається тільки з літер та має довжину не менше 2-ох літер.

class Street(Field):

    @Field.value.setter
    def value(self, value):
        if not re.match(r'^[A-z\d\.\-\(\)\:\_\,\/ ]{2,}$', value):
            raise ValueError
        self._Field__value = value
    # Магічний метод 'setter', який перевіряє на правильність введеного користувачем значення і записує у поле 'self.__value' значення, якщо
    # назва введеної вулиці починається з літери та може містити тільки цифри та букви.

class House(Field):

    @Field.value.setter
    def value(self, value):
        if not re.match(r'[ A-z\d\-\\\/\.]{1,}', value):
            raise ValueError
        self._Field__value = value
    # Магічний метод 'setter', який перевіряє на правильність введеного користувачем значення і записує у поле 'self.__value' значення, якщо
    # введені назва/номер будинку складається з літер або цифр.


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday
        self.email = email
        self.address = ''

    def add_user(self, name: Name):
        if not name.value:
            self.name = name
            return f"Record for user {name} was created"
        return f"Record for user {name} already exist in this address book"
    
    # Функція додає телефон до списку телефонів користувача. Перевіряє чи вже введено такий телефон раніше.
    def add_phone(self, phone: Phone) -> None:
        if phone.value not in [phone_.value for phone_ in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} was added to contact {self.name}"
        return f"phone: {phone} is already registered for user {self.name}"

    # Функція додає дату народження користувача. Враховано, що дата народження не може бути у майбутньому.
    def add_birthday(self, birthday: Birthday):
        if self.birthday:
            return f'Birthday for user {self.name} already exists. Use command "change birthday".'
        else:
            self.birthday = birthday
            return f'Birthday for user {self.name} was added successfully.'

    # Функція додає email користувача. Перевірка на правильність прописана у класі Email.
    def add_email(self, email: Email):
        self.email = email
        return f'E-mail for user {self.name} was added successfully'
    
    def days_to_birthday(self):  # Функція повертає кількість днів до дня народження користувача.
        if not self.birthday:
            return f'No data for birthday of user {self.name}'
        today = datetime.now().date()
        bd_current_year = self.birthday.value.replace(year=today.year)
        bd_next_year = self.birthday.value.replace(year=today.year + 1)
        diff_years = today.year - self.birthday.value.year
        if (bd_current_year - today).days == 0:
            return f"Today {self.name} celebrate {diff_years} birthday. Don't forget to buy a gift."
        elif (bd_current_year - today).days > 0:
            diff_days = (bd_current_year - today).days
            return f"There are {diff_days} days left until the {self.name}'s {diff_years} birthday"
        diff_days = (bd_next_year - today).days
        return f"There are {diff_days} days left until the {self.name}'s {diff_years + 1} birthday"
    
    def days_to_birthday_int_numbers(self) -> int:  # Функція повертає кількість днів до дня народження користувача.
        if not self.birthday:
            return -1 # якщо дати народження нема, то повертає -1
        today = datetime.now().date()
        bd_current_year = self.birthday.value.replace(year=today.year)
        bd_next_year = self.birthday.value.replace(year=today.year + 1)
        if (bd_current_year - today).days == 0:
            return 0
        elif (bd_current_year - today).days > 0:
            diff_days = (bd_current_year - today).days
            return diff_days
        diff_days = (bd_next_year - today).days
        return diff_days
    
    def add_address(self, country: Country, city: City = None, street: Street = None, house: House = None):
        self.address = f'{country.value}/{city.value if city != None else "empty"}/{street.value if street != None else "empty"}/{house.value if house != None else "empty"}'
        return 'Success'
    # метод добавляє адресу проживання у поле self.address
    
    def how_much_user_live(self) -> int:
        if not self.birthday:
            return -1
        else:
            today = datetime.now().date()
            living_days = (today - self.birthday.value).days
            return living_days

    # Рядкове представлення для одного запису у contact_book
    def __str__(self) -> str:
        return f"User: {self.name} | phones: {', '.join(str(p) for p in self.phones)} | birthday: {self.birthday if self.birthday != None else ''} " \
               f"| email: {self.email if self.email != None else ''} | address: {self.address} "    


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record.name} was added successfully"
    
    def save_to_file(self, filename):
        with open(filename, mode="wb") as file:
            pickle.dump(self.data, file)
            print("\nContack book has saved.")

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.data = pickle.load(f)
                print("\nContact book has loaded.")
        except (FileNotFoundError, pickle.UnpicklingError):
            with open(filename, 'wb') as f:
                self.data = {}
                pickle.dump(self.data, f)

    def search_match(self, match):
        found_match = []
        for item in self.data.values():
            if match in str(item):
                found_match.append(str(item))
        if len(found_match) == 0:  # Якщо не знайшло збігів
            return f"\nNo matches found for '{match}' in whole addressbook"
        else:
            print(f"\nWe found matches for '{match}' in {len(found_match)} contacts in whole contactbook: ")
            return '\n'.join(el for el in found_match)
    
    def congrats_list(self, shift_days, record: Record = None):
        congrats_dict = {}
        for record in self.data.values():
            res = record.days_to_birthday_int_numbers()
            if 0 <= res <= shift_days:
                congrats_dict[str(record)] = res
        new_dict = defaultdict(list)
        for rec, res in congrats_dict.items():
            new_dict[res].append(rec)
        sorted_list = sorted(new_dict.items())
        if len(congrats_dict) == 0:
            return f'No users are celebrating birthday in the next {shift_days} days'
        else:
            almost_list = []
            for el in sorted_list:
                almost_list.append(el[1])
            congrats_list = []
            for lst in almost_list:
                for el in lst:
                    congrats_list.append(el)
            print(f'\n{len(congrats_dict)} users are celebrating their birthday in the next {shift_days} days: ')
            return '\n'.join(el for el in congrats_list)
        
    def next_week_birthdays(self):
        next_week_dict = {}
        today = datetime.now().date().weekday()
        for record in self.data.values():
            res = record.days_to_birthday_int_numbers()
            if 7 - today <= res < 14 - today:
                next_week_dict[str(record)] = res
        new_dict = defaultdict(list)
        for rec, res in next_week_dict.items():
            new_dict[res].append(rec)
        sorted_list = sorted(new_dict.items())
        if len(next_week_dict) == 0:
            return f'No users are celebrating birthday in the next week'
        else:
            almost_list = []
            for el in sorted_list:
                almost_list.append(el[1])
            congrats_list = []
            for lst in almost_list:
                for el in lst:
                    congrats_list.append(el)
            print(f'\n{len(congrats_list)} users are celebrating their birthday in the next week: ')
            return '\n'.join(el for el in congrats_list)
        
    def current_week_birthdays(self):
        current_week_dict = {}
        today = datetime.now().date().weekday()
        for record in self.data.values():
            res = record.days_to_birthday_int_numbers()
            if 0 <= res < 7 - today:
                current_week_dict[str(record)] = res
        new_dict = defaultdict(list)
        for rec, res in current_week_dict.items():
            new_dict[res].append(rec)
        sorted_list = sorted(new_dict.items())
        if len(current_week_dict) == 0:
            return f'No users are celebrating birthday in the next week'
        else:
            almost_list = []
            for el in sorted_list:
                almost_list.append(el[1])
            congrats_list = []
            for lst in almost_list:
                for el in lst:
                    congrats_list.append(el)
            print(f'\n{len(congrats_list)} users are celebrating their birthday in the next week: ')
            return '\n'.join(el for el in congrats_list)

    def next_month_birthdays(self, record: Record = None):
        next_month_dict = {}
        current_month = datetime.now().date().month
        for record in self.data.values():
            if not record.birthday:
                continue
            else:
                if current_month == 12:
                    if record.birthday.value.month == current_month - 11:
                        next_month_dict[str(record)] = record.birthday.value.day
                    new_dict = defaultdict(list)
                    for rec, res in next_month_dict.items():
                        new_dict[res].append(rec)
                    sorted_list = sorted(new_dict.items())
                else:    
                    if record.birthday.value.month == current_month + 1:
                        next_month_dict[str(record)] = record.birthday.value.day
                    new_dict = defaultdict(list)
                    for rec, res in next_month_dict.items():
                        new_dict[res].append(rec)
                    sorted_list = sorted(new_dict.items())
        if len(next_month_dict) == 0:
            return f'No users are celebrating birthday in the next month'
        else:
            almost_list = []
            for el in sorted_list:
                almost_list.append(el[1])
            congrats_list = []
            for lst in almost_list:
                for el in lst:
                    congrats_list.append(el)
            print(f'\n{len(congrats_list)} users are celebrating their birthday in the next month: ')
            return '\n'.join(el for el in congrats_list)
        
    def current_month_birthdays(self, record: Record = None):
        current_month_dict = {}
        current_month = datetime.now().date().month
        for record in self.data.values():
            if not record.birthday:
                continue
            else:
                if record.birthday.value.month == current_month:
                    current_month_dict[str(record)] = record.birthday.value.day
        new_dict = defaultdict(list)
        for rec, res in current_month_dict.items():
            new_dict[res].append(rec)
        sorted_list = sorted(new_dict.items())
        if len(current_month_dict) == 0:
            return f'No users are celebrating birthday in the current month'
        else:
            almost_list = []
            for el in sorted_list:
                almost_list.append(el[1])
            congrats_list = []
            for lst in almost_list:
                for el in lst:
                    congrats_list.append(el)
            print(f'\n{len(congrats_list)} users are celebrating their birthday in the current month: ')
            return '\n'.join(el for el in congrats_list)

    def sort_by_name(self, record: Record=None):  # Функція сортує по імені всю книгу контактів.
        contactbook_dict = {}
        for record in self.data.values():
            contactbook_dict[record.name.value] = str(record)
        return '\n'.join(el for el in sorted(contactbook_dict.values()))
    
    def sort_by_age(self, record: Record=None):  # Функція сортує contactbook по віку користувача.
        contactbook_dict = {}
        no_birthday_list = []
        for record in self.data.values():
            if record.birthday:
                res = record.how_much_user_live()
                contactbook_dict[str(record)] = res
            else:
                no_birthday_list.append(str(record))
        print(contactbook_dict)
        new_dict = defaultdict(list)
        for rec, res in contactbook_dict.items():
            new_dict[res].append(rec)
        sorted_list = sorted(new_dict.items(), reverse=True)
        if len(contactbook_dict) == 0:
            return f'No data for birthday in all records.'
        else:
            almost_list = []
            for el in sorted_list:
                almost_list.append(el[1])
                print(el)
            print(almost_list)
            contactbook_list = []
            for lst in almost_list:
                for el in lst:
                    contactbook_list.append(el)
        print(no_birthday_list)
        print(f'\nThere are still {len(no_birthday_list)} users without birthday: ')
        for el in no_birthday_list:
            print(el)
        print('\nYour contactbook is sorted due to the age of users: \n')
        return '\n'.join(el for el in contactbook_list)

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:  # Рядкове представлення для усіх записів у contact_book
        return "\n".join(str(r) for r in self.data.values())
