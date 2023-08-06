# Внаслідок перейменування пакетів оновлено імпорт пакетів
from contact_book_classes import AddressBook, Name, Phone, Birthday, Record, Email

contact_book = AddressBook()

def error_handler(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return "No user"
        # під час виконання різних методів виникають різні помилки ValueError. Тому пропоную їх перехоплювати у методах, 
        # щоб користувач знав у чому проблема. Крім того нам ще треба продумавти логіку для перехоплення помилок типу AttribiteError.
        except ValueError as e:
            return e
        except IndexError:
            return 'Not enough parameters'
    return inner


def unknown_command(args):
    return "unknown_command"


def exit(args):
    return


@error_handler
def add_user(args):
    name = Name(args[0])
    rec = Record(name)
    if len(args)==2:
        phone = Phone(args[1])
        rec = Record(name, phone)
    elif len(args)==3:
        phone = Phone(args[1])
        birthday = Birthday(args[2])
        rec = Record(name, phone, birthday)
    contact_book.add_record(rec)
    return f'User {name.value} added!'


@error_handler
def add_phone_command(args):  # Додаємо номер телефону для вибраного користувача.
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = contact_book.get(str(name))
    if rec:
        return rec.add_phone(phone)


@error_handler
def add_birthday_command(args):  # додаємо дату народження для користувача
    name = Name(args[0])
    birthday = Birthday(args[1])
    rec: Record = contact_book.get(str(name))
    if rec:
        return rec.add_birthday(birthday)


@error_handler
def add_email_command(args):  # додаємо e-mail для користувача
    name = Name(args[0])
    email = Email(args[1])
    rec: Record = contact_book.get(str(name))
    if rec:
        return rec.add_email(email)
    

@error_handler
def show_user_command(args):  # Пошук телефона вибраного користувача.
    return contact_book[args[0]]


def show_all(args):
    if len(contact_book) == 0:  # Якщо словник порожній.
        return 'Address book is now empty. Please add some users'
    else:
        print(f'There are {len(contact_book)} users in address book')
        return contact_book


HANDLERS = {
    'add user': add_user,
    'add phone': add_phone_command,
    'add birthday': add_birthday_command,
    'add email': add_email_command,
    'show all': show_all,
    'show user': show_user_command,
    'exit': exit,
    'good bye': exit,
    'close': exit,
}


def parse_input(user_input):
    try:
        command, *args = user_input.split()
        command = command.lstrip()
        handler = HANDLERS[command.lower()]
    except KeyError:
        if args:
            command = command + ' ' + args[0]
            args = args[1:]
        handler = HANDLERS.get(command.lower(), unknown_command)
    except ValueError:
        handler = unknown_command
        args = None
    return handler, args
