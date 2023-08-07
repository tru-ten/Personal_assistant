# Внаслідок перейменування пакетів оновлено імпорт пакетів
from contact_book_classes import AddressBook, Name, Phone, Birthday, Record, Email, Country, City, Street, House

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
        # Варто ще обробити помилки TypeError та AttribiteError. Вони точно будуть виникати під час роботи.
        except TypeError:
            return 'Wrong command or too many parameters are specified.'
        except AttributeError:
            return f"User {args[0]} doesn't exist. First create a record about this user."
    return inner


@error_handler
def greeting(*args):
    return 'Hello how can I help you?'


@error_handler
def helper(*args):
    res = ''
    for value in HANDLERS.values():
        res += f'{value[0]}\n'
    return 'Bot has such commands: \n' + res[0:-6]


@error_handler
def unknown_command():
    return 'Unknown command. Try again'


@error_handler
def exit_command(*args):
    return 'Good Bye!'


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
def show_all_command(*args):
    if len(contact_book) == 0:  # Якщо словник порожній.
        return 'Address book is now empty. Please add some users'
    else:
        print(f'There are {len(contact_book)} users in address book')
        return contact_book
    

user_inputs = ['y', 'yes', '+']  #список з варіантами відповідей, якщо користувач погоджується


exit_inputs = ['exit', 'break', '-'] # список з варіантами відповідей, якщо користувач хоче завершити виконання команди


def input_checking(func):
    def inner(class_, value):
        if class_ == Country:
            address = func(class_, value)
            return address
        print(f'Do you want to include {value}?')
        answer = input('Y/N: ').strip()
        if answer.lower() in user_inputs:
            address = func(class_, value) 
            return address
        return None
    return inner
    # функція(декоратор) запитує в користувача чи хоче він записати інформацію поля класу повідомленням "Do you want to include {value}",
    # де 'value' це країна/місто/вулиця/будинок. Функція повертає екземпляр класу, якщо введене значення користувача
    # пройшло перевірку функцією 'address_input', або повертає 'exit', якщо користувач ввів одну з команд для виходу.
    # Якщо користувач відповів на питання 'Do you want to include {value}?' - ні, то повертає 'None'


@input_checking
def address_input(class_, value):
    while True: 
        try:
            address_value = input(f'Enter a {value}: ').strip()
            if address_value.lower() in exit_inputs:
                return 'exit'
            country = class_(address_value)
            return country
        except:
            print('Wrong format, try again')
    # поки користувач не введе правильне значення або одну з команд для виходу, функція буде запитувати
    # користувача на введеня даних


def add_address(*args):
    name = Name(input('Enter the name of the contact: ').strip())
    #користувач вводить ім'я контакту 
    rec: Record = contact_book.get(str(name)) 
    #отримуємо інформацію про записаного користувача
    
    if rec: 
    #перевіряємо чи інсує запис з ім'ям, яке ввів користувач, якщо так, то продовжуємо
        city = None 
        street = None 
        house = None 
        # необов'язкові поля

        country = address_input(Country, 'country') #отримуємо країну, яку користувач хоче додати
        if country == 'exit': # перевіряємо чи функція повернула нам команду для закінчення додавання адреси
            return 'Command cancelled' # якщо так, то зупиняємо команду та відповідаємо користувачеві
              
        city = address_input(City, 'city') #               ^
        if city == 'exit': #                               | (інформація зверху)
            rec.add_address(country, None, street, house)# |
            return 'command canceled' #                    |
         
        street = address_input(Street, 'street') #         ^
        if street == 'exit': #                             | (інформація зверху)
            rec.add_address(country, city, None, house)# |
            return 'Command cancelled' #                   |
    
        house = address_input(House, 'house')#             ^
        if house == 'exit': #                              | (інформація зверху)
            rec.add_address(country, city, street, None)# |
            return 'Command cancelled' #                   |
            
        return rec.add_address(country, city, street, house) # записуємо адрес до інформації про людину
    return f'There is no contact with name: {name}' #повертаємо інформацію, якщо немає запису з ім'ям, яке ввів користувач


HANDLERS = {
    greeting: ('hello', 'hi', 'good afternoon'),
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
    helper: ('help', 'рудз'),
    add_address: ('add address', 'new address',)
}

FUNCS_NO_ARGS = [add_address, show_all_command, exit_command, greeting]


def parse_input(user_input):
    for cmd, keywords in HANDLERS.items():
        for kwd in keywords:
            if user_input.lower().startswith(kwd):
                if cmd in FUNCS_NO_ARGS:
                    return cmd, user_input
                data = user_input[len(kwd):].strip().split()
                return cmd, data
    return unknown_command, []
