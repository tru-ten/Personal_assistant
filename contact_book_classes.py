from collections import UserDict
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

    @Field.value.setter
    def value(self, value):
        if not re.match(r'[A-z\d]{1,}', value):
            print('Wrong format.')
            raise ValueError
        self._Field__value = value


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
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None, country: Country = None, city: City = None, street: Street = None, house: House = None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday
        self.email = email
        self.country = country
        self.city = city
        self.street = street
        self.house = house


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


    def change_phone(self, old_phone: Phone, new_phone: Phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f'Old phone: {old_phone} was changed to new: {new_phone}'
        return f"Phone: {old_phone} is not present in {self.name}'s phones" 
    

    def delete_phone(self, phone):
        for p in self.phones:
            if phone.value == p.value:
                self.phones.remove(p)
                return f'Phone: {phone} in contact {self.name} was deleted successfully'
        return f"Phone: {phone} is not present in {self.name}'s list of phones"


    # Функція додає дату народження користувача. Враховано, що дата народження не може бути у майбутньому.
    def add_birthday(self, birthday: Birthday):
        if self.birthday:
            return f'Birthday for user {self.name} already exists. Use command "change birthday".'
        self.birthday = birthday
        return f'Birthday for user {self.name} was added successfully.'
        

    def change_birthday(self, birthday: Birthday):
        if not self.birthday:
            return f'Birthday for contact {self.name} is not included. Use command "add birthday".'
        self.birthday = birthday
        return f'Birthday for contact {self.name} was changed successfully'
    

    def delete_birthday(self):
        if not self.birthday:
            return f"You haven't included birthday for contact {self.name} yet"
        self.birthday = None
        return f'Birthday for contact {self.name} was successfully deleted'


    # Функція додає email користувача. Перевірка на правильність прописана у класі Email.
    def add_email(self, email: Email):
        if not self.email:
            self.email = email
            return f'E-mail for user {self.name} was added successfully'
        return 'Email for contact {self.name} already exists. Use command "change email"'
    

    def change_email(self, email: Email):
        if not self.email:
            return f'Email for contact {self.name} is not included. Use command "add email".'
        self.email = email
        return f'Email for contact {self.name} was changed successfully'
    

    def delete_email(self):
        if not self.email:
            return f"You haven't included birthday for contact {self.name} yet"
        self.email = None
        return f'Email for contact {self.name} was deleted successfully'
    

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
        self.country = country
        self.city = city
        self.street = street
        self.house = house
        return f'Address for user {self.name} was added successfully'
    # метод добавляє адресу проживання у поле self.address
        

    def change_country(self, country: Country):
        self.country = country
        return f'Country address for user {self.name} was changed successfully'
    

    def delete_country(self):
        if not self.country:
            return 'You have not included country address yet'
        self.country = None
        return f'Country address for contact {self.name} was deleted successfully'
    

    def change_city(self, city: City):
        self.city = city
        return f'City address for user {self.name} was changed successfully'
    

    def delete_city(self):
        if not self.city:
            return 'You have not included city address yet'
        self.city = None
        return f'City address for contact {self.name} was deleted successfully'
    

    def change_street(self, street: Street):
        self.street = street
        return f'Street address for user {self.name} was changed successfully'
    

    def delete_street(self):
        if not self.street:
            return 'You have not included street address yet'
        self.street = None
        return f'Street address for contact {self.name} was deleted successfully'


    def change_house(self, house: House):
        self.house = house
        return f'House address for user {self.name} was changed successfully'
    

    def delete_house(self):
        if not self.house:
            return 'You have not included house address yet'
        self.house = None
        return f'House address for contact {self.name} was deleted successfully'


    def __str__(self) -> str:
        return f"User: {self.name} | phones: {', '.join(str(p) for p in self.phones)} | birthday: {self.birthday} " \
               f"| email: {self.email} | address: {self.country}/{self.city}/{self.street}/{self.house}"    
    # Рядкове представлення для одного запису у contact_book


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record.name} was added successfully"
    

    def change_rec_name(self, old_name: Name, new_name: Name):
        for key in self.data.keys():
            if key == old_name.value:
                old_rec = self.data.pop(key)
                old_rec.name = new_name
                self.data.update({str(new_name): old_rec})
                return f'Contact with name {old_name} was changed to name {new_name}'
        return f'There is not contact with name: {old_name}'
    

    def delete_rec(self, name: Name):
        for key in self.data.keys():
            if str(key) == name.value:
                self.data.pop(key)
                return f'Contact with name: {name} was deleted successfully'
        return f'There is not contact with name: {name}'
    

    def save_to_file(self, filename):
        with open(filename, mode="wb") as file:
            pickle.dump(self.data, file)
            print("Contack book has saved.")


    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.data = pickle.load(f)
                print("Contact book has loaded.")
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
        congrats_list = []
        for record in self.data.values():
            res = record.days_to_birthday_int_numbers()
            if 0 <= res <= shift_days:
                congrats_list.append(str(record))
        if len(congrats_list) == 0:
            return f'No users are celebrating birthday in the next {shift_days} days'
        else:
            print(f'\n{len(congrats_list)} users are celebrating their birthday in the next {shift_days} days: ')
            return '\n'.join(el for el in congrats_list)
        

    def next_week_birthdays(self):
        next_week_list = []
        today = datetime.now().date().weekday()
        for record in self.data.values():
            res = record.days_to_birthday_int_numbers()
            if 7 - today <= res < 14 - today:
                next_week_list.append(str(record))
        if len(next_week_list) == 0:
            return f'No users are celebrating birthday in the next week'
        else:
            print(f'\n{len(next_week_list)} users are celebrating their birthday in the next week: ')
            return '\n'.join(el for el in next_week_list)
        

    def current_week_birthdays(self):
        current_week_list = []
        today = datetime.now().date().weekday()
        for record in self.data.values():
            res = record.days_to_birthday_int_numbers()
            if - today <= res < 7 - today:
                current_week_list.append(str(record))
        if len(current_week_list) == 0:
            return f'No users are celebrating birthday in the current week'
        else:
            print(f'\n{len(current_week_list)} users are celebrating their birthday in the current week: ')
            return '\n'.join(el for el in current_week_list)


    def next_month_birthdays(self, record: Record = None):
        next_month_list = []
        current_month = datetime.now().date().month
        for record in self.data.values():
            if not record.birthday:
                continue
            else:
                if record.birthday.value.month == current_month + 1:
                    next_month_list.append(str(record))
        if len(next_month_list) == 0:
            return f'No users are celebrating birthday in the next month'
        else:
            print(f'\n{len(next_month_list)} users are celebrating their birthday in the next month: ')
            return '\n'.join(el for el in next_month_list)
        

    def current_month_birthdays(self, record: Record = None):
        current_month_list = []
        current_month = datetime.now().date().month
        for record in self.data.values():
            if not record.birthday:
                continue
            else:
                if record.birthday.value.month == current_month:
                    current_month_list.append(str(record))
        if len(current_month_list) == 0:
            return f'No users are celebrating birthday in the current month'
        else:
            print(f'\n{len(current_month_list)} users are celebrating their birthday in the current month: ')
            return '\n'.join(el for el in current_month_list)


    def __repr__(self):
        return str(self)


    def __str__(self) -> str:  # Рядкове представлення для усіх записів у contact_book
        return "\n".join(str(r) for r in self.data.values())
