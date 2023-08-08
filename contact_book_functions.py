# Внаслідок перейменування пакетів оновлено імпорт пакетів
from contact_book_classes import AddressBook, Name, Phone, Birthday, Record, Email
import time

contact_book = AddressBook()
filename = 'contact_book.bin'

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


# Додано програму, яка одразу після запуску завантажує contact_book з файлу та видає привітальне повідомлення.
def start():
    contact_book.load_from_file(filename)
    # Додаю невеликий привітальний текст. Тут в принципі можна й щось інше написати. І ще додав вивід кожного рядка за 1,5 секунди.
    invitation_text = ["Hello. I am your personal assistant.", 
                         "I will help you organize your contact book.", 
                         "Using the command 'help', you can find out the list of available operations.",
                          "Let's start and enjoy!!!" ]
    for string in invitation_text:
        time.sleep(0.2)
        print(string)
    

@error_handler
def helper():
    res = ''
    for value in HANDLERS.values():
        res += f'{value[0]} : {value[1]}\n'
    return '\nType one of the available commands from the list below:\n\n' + res


@error_handler
def unknown_command():
    return 'Unknown command. Try again'


@error_handler
def exit_command():
    contact_book.save_to_file(filename) 
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
    
    # Додаю функцію для пошуку збігів у contactbook. Повертає список контактів, у яких присутній збіг.
@error_handler
def search_command():  # Шукає задану послідовність символів у addressbook.
    if len(contact_book) == 0:  # Якщо словник порожній.
        command_text = '''Address book is now empty. Please add some users. 
It is very difficult to find a black cat in a dark room, especially if it is not there.'''
        return command_text
    else:
        match = input('Enter what you want to find. Two characters minimum: ')
        if len(match) < 2:
            return 'Search is too short. Enter at least 2 symbols.'
        return contact_book.search_match(match)


HANDLERS = {
    add_user_command: ('11', 'add user', 'new user', 'create user', '+'),
    add_phone_command: ('12', 'add phone'),
    add_birthday_command: ('13', 'add birthday', 'birthday'),
    add_email_command: ('14', 'add email', 'email'),
    # Сюди необхідно додати функції на редагування (21-27) та видалення записів (31-37)
    days_to_birthday: ('41', 'days to birthday', 'days to bd'),
    congrats_list_command: ('42', 'upcoming birthdays', 'closest birthdays'),
    birthdays_next_week: ('43', 'next week birthdays', 'next week'),
    birthdays_current_week: ('44', 'current week birthdays', 'current week'),
    birthdays_next_month: ('45', 'next month birthdays', 'next month'),
    birthdays_current_month: ('46', 'current month birthdays', 'current month'),
    show_all_command: ('55', 'show all', 'all phones', 'addressbook', 'contactbook', 'ірщц фдд'),
    show_user_command: ('66', 'show user', 'phone', 'number', 'show'),
    search_command: ('77', 'search', 'find', 'match', 'іуфкср', 'аштв', 'ьфеср'),
    exit_command: ('99', 'exit', 'bye', 'end', 'close', 'goodbye', 'учше'),
    helper: ('00', 'help', 'рудз')
}


def parse_input(user_input):
    for cmd, keywords in HANDLERS.items():
        for kwd in keywords:
            if user_input.lower().startswith(kwd):
                data = user_input[len(kwd):].strip().split()
                return cmd, data 
    return unknown_command, []
