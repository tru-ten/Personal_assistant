from collections import UserDict
from datetime import datetime
from re import match, search
import pickle


class WrongDateError(Exception):
    ...


class WrongPhoneFormat(Exception):
    ...


class NoDateError(Exception):
    ...


class WrongEmailError(Exception):
    ...

class Field:

    def __init__(self, value) -> None:
        self.value = value


    def __str__(self) -> str:
        return self.value


    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    ...


class Phone(Field):
    def __init__(self, value = None):
        self._value = None
        self.value = value


    @property
    def value(self):
        return self._phone


    @value.setter
    def value(self, new_phone):
        r_data = r'\d{12}'
        data = match(r_data, new_phone)
        if data:
            self._phone = new_phone
        else:
            raise WrongPhoneFormat


class Birthday(Field):
    
    def __init__(self, value = None):
        self._value = None
        self.value = value


    @property
    def value(self):
        return self._birthday


    @value.setter
    def value(self, new_birthday):
        matched = r'^(\d{1,2}\.{1}\d{1,2}\.\d{4})$'
        data = match(matched, str(new_birthday))
        if data:
            self._birthday = new_birthday
        else:
            raise WrongDateError


class Email(Field):
    def __init__(self, email = None):
        self._email = None
        self.email = email


    @property
    def value(self):
        return self._email
    

    @value.setter
    def value(self, new_email):
        matched = r"[A-z][\dA-z\._]{1,}@[A-z]{2,}\.[A-z]{2,}"
        data = match(matched, str(new_email))
        if data:
            self._email = new_email
        else:
            raise WrongEmailError
    

class Country():
    def __init__(self, value = 'Ukraine'):
        self.value = value
        self._value = None

    @property
    def value(self):
        return self._country
    
    @value.setter
    def value(self, new_country):
        rex = r'^[A-z]{2,}$'
        matched = match(rex, new_country)
        if matched:
            self._country = new_country
        else:
            raise ValueError


class City():
    def __init__(self, value = None):
        self.value = value
        self._value = None

    @property
    def value(self):
        return self._city
    
    @value.setter
    def value(self, new_city):
        rex = r'^[A-z]{2,}$'
        matched = match(rex, new_city)
        if matched:
            self._city = new_city
        else:
            raise ValueError
        
class Street():
    def __init__(self, value = None):
        self.value = value
        self._value = None

    @property
    def value(self):
        return self._street
    
    @value.setter
    def value(self, new_street):
        rex = r'[A-z]{1,}.{1,}'
        matched = match(rex, new_street)
        if matched:
            self._street = new_street
        else:
            raise ValueError
        
class House():
    def __init__(self, value = None):
        self.value = value
        self._value = None

    @property
    def value(self):
        return self._house
    
    @value.setter
    def value(self, new_house):
        rex = r'^[A-z\d]{1,}$'
        matched = match(rex, new_house)
        if matched:
            self._house = new_house
        else:
            raise ValueError


class Record:

    def __init__(self, name: Name, phone: Phone = None, birthday : Birthday = None) -> None:
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.phone = phone
        self.address = 'Ukraine' # Дефолтне значення, якщо користувач не ввів адрес
        if phone:
            self.phones.append(phone)
    

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone.value} changeed to {new_phone.value}"
        return f"{old_phone.value} is not present in phones of contact {self.name}"


    def add_address(self, country: Country ='Ukraine', city: City = None, street: Street = None, house: House = None):
        self.address = f'{country.value}|{city.value}|{street.value if street != None else "empty"}|{house.value if house != None else "empty"}'
        return 'Success'


    def days_to_birthday(self):
        if self.birthday:
            birthday_date = self.birthday.value.split('.')
            current_date = datetime.now()
            datetime_birthday = datetime(year=current_date.year, month=int(birthday_date[1]), day=int(birthday_date[0]))
            days_left = datetime_birthday - current_date
            if days_left.days > 0:
                return days_left.days
            elif days_left.days < 0:
                datetime_birthday_2 = datetime(year=current_date.year + 1, month=int(birthday_date[1]), day=int(birthday_date[0]))
                result = datetime_birthday_2 - current_date
                return result.days
            else:
                return 'Tomorrow is your birthday'
        raise NoDateError

        
    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} added to contact {self.name}"
        return f"{phone} is present in phones of contact {self.name}"
    

    def __str__(self) -> str:
        return f"{self.name}: phone(s) ({', '.join(str(p) for p in self.phones)}), address ({self.address}), bithday({self.birthday if self.birthday != None else ''})"


class AddressBook(UserDict):
    
    def __init__(self):
        super().__init__()


    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"
    

    def read_from_file(self):
        with open('address_book.bin', 'rb') as fh:
            lst_info = []
            try:    
                while True:
                    info = pickle.load(fh)
                    lst_info.append(info)
            except EOFError:
                pass
            return lst_info
            

    def find_rec_by_name(self, name: str, lst_data: list):
        lst_result = []
        for name_, value in self.data.items():
            find_rec = search(name, str(name_))
            if find_rec:
                lst_result.append(f'{name_}: {value.phones}')
        return lst_result

    
    def find_rec_by_phone(self, phone: str, lst_data: list):
        lst_result = []
        for name, value in self.data.items():
            str_value = ','.join([p.value for p in value.phones])
            find_rec = search(phone, str_value)
            if find_rec:
                lst_result.append(f'{name}: {value.phones}')
        return lst_result
    

    def save_to_file(self, filename):
        with open(filename, mode="wb") as file:
            pickle.dump(self.data, file)
            print("Address book save.")


    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.data = pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError):
            with open(filename, 'wb') as f:
                self.data = {}
                pickle.dump(self.data, f)


    def __next__(self):
        if self._iter_index >= len(self.data):
            raise StopIteration
        key = list(self.data.keys())[self._iter_index]
        self._iter_index += 1
        return key


    def __iter__(self):
        self._iter_index = 0
        return self


    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())