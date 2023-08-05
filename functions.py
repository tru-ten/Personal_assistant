from classes import AddressBook, Name, Phone, Birthday, Record

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

def show_all(args):
    if len(contact_book)>0:
        result = ''
        for name, record in contact_book.items():
            phones = list(map(lambda x: x.value, record.phones))
            if record.birthday == None:
                birthday = record.birthday
            else:
                birthday = record.birthday.value
            result += f'Name: {name}, Phone: {phones}, Birthday: {birthday}\n'
        return result
    return 'Contact book is empty'

HANDLERS = {
    'add': add_user,
    'show all': show_all,
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
