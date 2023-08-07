from contact_book_classes import AddressBook, Name, Phone, Birthday, Record, Email, Country, City, Street, House

contact_book = AddressBook()

def error_handler(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return "No user"
        except ValueError:
            return 'Give me name and phone please'
        except IndexError:
            return 'Not enough parameters'
    return inner


def unknown_command(args):
    return "unknown_command"


def exit(args):
    return 'good bye!'


def greeting(args):
    return 'Hello, how can I help you?'


@error_handler
def add_user(args):
    name = Name(args)
    rec : Record = contact_book.get(str(name))
    if rec: 
        return f'User {name} already exist'
    rec = Record(name)
    return contact_book.add_record(rec)
    # створюємо новий запис з ім'ям людини

@error_handler
def add_phone(args):
    lst_args = args.split(', ')
    name = Name(lst_args[0])
    rec: Record = contact_book.get(str(name))
    if rec:
        phone = Phone(lst_args[1])
        return rec.add_phone(phone)
    return f'There is no contact with name: {name}'
    # записуємо номер телефону до інформації про людину

@error_handler
def add_birthday(args):
    lst_args = args.split(', ')
    name = Name(lst_args[0])
    rec: Record = contact_book.get(str(name))
    if rec:
        birthday = Birthday(lst_args[1])
        return rec.add_birthday(birthday)
    return f'There is no contact with name: {name}'
    # записуємо дату народження до інформації про людину

@error_handler
def add_email(args):
    lst_args = args.split(', ')
    name = Name(lst_args[0])
    rec: Record = contact_book.get(str(name))
    if rec:
        email = Email(lst_args[1])
        return rec.add_email(email)
    return f'There is no contact with name: {name}'
    # записуємо email до інформації про людину

def add_address(args):
    name = Name(input('Enter the name of the contact: ').strip()) #користувач вводить ім'я контакту
    rec: Record = contact_book.get(str(name)) #отримуємо інформацію про записаного користувача
    user_inputs = ['y', 'yes', '+'] #список з варіантами відповідей, якщо користувач погоджується
    if rec: #перевіряємо чи інсує запис з ім'ям, яке ввів користувач, якщо так, то продовжуємо
        street = None #необов'язкове поле
        house = None #необов'язкове поле
        country = Country(input('Enter a country: ').strip()) #отримуємо країну, яку користувач хоче додати
        city = City(input('Enter the city/town/village: ').strip()) #отримуємо населенний пункт, який користувач хоче додати
        print('Do you want to include street?') #запитуємо в користувача чи він хоче додати назву вулиці
        answer = input('Y/N: ').strip() # користувач відповідає так/ні
        if answer.lower() in user_inputs: # перевіряємо чи відповідь у нашому списку з варіантами 'так'
            street = Street(input('Enter the street: ').strip()) #якщо так, запитуємо назву вулиці 
        print('Do you want to include house address?') #запитуємо чи користувач хоче добавити номер будинку
        answer_2 = input('Y/N: ').strip() # користувач відповідає так/ні
        if answer_2.lower() in user_inputs: # перевіряємо чи відповідь у нашому списку з варіантами 'так'
            house = House(input('Enter the house address: ').strip()) #якщо так, запитуємо номер будинку
        return rec.add_address(country, city, street, house) # записуємо адрес до інформації про людину
    return f'There is no contact with name: {name}' #повертаємо інформацію, якщо немає запису з ім'ям, яке ввів користувач


def show_all(args):
    return contact_book
# повертає всі записи з контактної книги


HANDLERS = {
    add_user: ('add contact',),
    add_phone: ('add phone',),
    add_birthday: ('add birthday',),
    add_email: ('add email',),
    add_address: ('add address',),
    greeting: ('hello',),
    show_all: ('show all',),
    exit: ('exit', 'close', 'good bye'),
}
# словник з ключами 'функціями' та значеннями 'командами користувача'


FUNCS_NO_ARGS = [add_address, show_all, exit, greeting]
# словник з функціями, яким не портібно приймати дані від користувача


@error_handler
def parse_input(user_input):
    user_command = user_input.strip()
    for funcs, commands in HANDLERS.items():
        if user_command in commands:
            func = funcs
            if func in FUNCS_NO_ARGS:
                return func, user_command
            user_args = input('enter some data: ')
            return func, user_args.strip()
    return unknown_command, user_input

    """
    Парсер приймає команду, що ввів користувач. Обробляє введену команду, щоб вона була у правильному форматі.
    Дальше, парсер шукає цю команду в значеннях(values) нашого словника, де ключі це назви функцій,
    а значення - це команди, які користувач повинен ввести, щоб викликати функцію, яка йому потрібна.
    Дальше, якщо команда в значеннях, змінна func це буде функція, яку ми витягнули з ключів.
    Якщо команда не в значеннях ми повертаємо користувачеві 'unknown command'.
    Потім парсер перевіряє чи ця команда є в списку команд, яким не потрібно приймати певну інформацію для виклику.
    Якщо ця команда є в списку, то повертаємо функцію та яку-небуть інформацію, щоб наша функція 'main' могла запустити виконання команди.
    Якщо команди немає в списку, то ми просимо користувача ввести потрібну інформацію і повертаємо функцію з цією інформацією.   
    """