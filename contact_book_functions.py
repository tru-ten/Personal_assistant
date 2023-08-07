# Внаслідок перейменування пакетів оновлено імпорт пакетів
from contact_book_classes import AddressBook, Name, Phone, Birthday, Record, Email

contact_book = AddressBook()

def error_handler(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return f"No user with name {args[0]}. You need firstly create "
        # під час виконання різних методів виникають різні помилки ValueError. Тому пропоную їх перехоплювати у методах, 
        # щоб користувач знав у чому проблема. Крім того нам ще треба продумавти логіку для перехоплення помилок типу AttribiteError.
        except ValueError as e:
            return e
        except IndexError:
            return 'Not enough parameters'
        # Варто ще обробити помилки TypeError та AttribiteError. Вони точно будуть виникати під час роботи.
        except TypeError:
            return 'Wrong command or too many parameters are specified.'
        except AttributeError:
            return f"User {args[0]} doesn't exist. First create a record about this user."
    return inner


@error_handler
def helper():
    res = ''
    for value in HANDLERS.values():
        res += f'{value[0]}\n'
    return '\nType one of the available commands from the list below:\n\n' + res[0:-6]


@error_handler
def unknown_command():
    return 'Unknown command. Try again'


@error_handler
def exit_command():
    return 'Bye. Have a nice day. See you next time.'


@error_handler
def add_user_command(*args):
    name = Name(args[0])
    rec: Record = contact_book.get(str(name))
    if rec:
        return rec.add_user(name)
    rec = Record(name)
    return contact_book.add_record(rec)


@error_handler
def add_phone_command(*args):  # Додаємо номер телефону для вибраного користувача.
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = contact_book.get(str(name))
    if rec:
        return rec.add_phone(phone)


@error_handler
def add_birthday_command(*args):  # додаємо дату народження для користувача
    name = Name(args[0])
    birthday = Birthday(args[1])
    rec: Record = contact_book.get(str(name))
    if rec:
        return rec.add_birthday(birthday)


@error_handler
def add_email_command(*args):  # додаємо e-mail для користувача
    name = Name(args[0])
    email = Email(args[1])
    rec: Record = contact_book.get(str(name))
    if rec:
        return rec.add_email(email)
    

@error_handler
def days_to_birthday(*args):  # Повертає кількість днів до дня народження користувача.
    name = Name(args[0])
    rec: Record = contact_book.get(str(name))
    return rec.days_to_birthday()


@error_handler
def congrats_list_command(*args):  # Повертає список користувачів, які святкують ДН на протязі shift_days.
    if len(contact_book) == 0:  # Якщо словник порожній.
        return 'Address book is now empty. Please add some users'
    else:
        command_text = '''This command helps you to find out which users have a birthday during this period. 
Enter the number of days (an integer): '''
        print(f'There are {len(contact_book)} users in address book')
        shift_days = int(input(command_text))
        return contact_book.congrats_list(shift_days)


@error_handler
def birthdays_next_week():  # Користувачі, котрі святкують ДН наступного тижня.
    return contact_book.next_week_birthdays()


@error_handler
def birthdays_current_week():  # Користувачі, котрі святкують ДН поточного тижня.
    return contact_book.current_week_birthdays()


@error_handler
def birthdays_next_month():  # Користувачі, котрі святкують ДН наступного місяця.
    return contact_book.next_month_birthdays()


@error_handler
def birthdays_current_month():  # Користувачі, котрі святкують ДН поточного місяця.
    return contact_book.current_month_birthdays()


@error_handler
def show_user_command(*args):  # Пошук телефона вибраного користувача.
    return contact_book[args[0]]


@error_handler
def show_all_command():
    if len(contact_book) == 0:  # Якщо словник порожній.
        return 'Address book is now empty. Please add some users'
    else:
        print(f'There are {len(contact_book)} users in address book')
        return contact_book


HANDLERS = {
    show_all_command: ('show all', 'all phones', 'addressbook', 'phonebook', 'contactbook'),
    days_to_birthday: ('days to birthday', 'days to bd'),
    congrats_list_command: ('upcoming birthdays', 'closest birthdays'),
    birthdays_next_week: ('next week', ),
    birthdays_current_week: ('current week', ),
    birthdays_next_month: ('next month', ),
    birthdays_current_month: ('current month', ),
    add_phone_command: ('add phone', ),
    add_birthday_command: ('add birthday', 'birthday'),
    add_email_command: ('add email', ),
    add_user_command: ('add user', 'new user', 'create user', '+'),
    show_user_command: ('show user', 'phone', 'number', 'show'),
    exit_command: ('exit', 'bye', 'end', 'close', 'goodbye', 'учше'),
    helper: ('help', 'рудз')
}


def parse_input(user_input):
    for cmd, keywords in HANDLERS.items():
        for kwd in keywords:
            if user_input.lower().startswith(kwd):
                data = user_input[len(kwd):].strip().split()
                return cmd, data 
    return unknown_command, []
