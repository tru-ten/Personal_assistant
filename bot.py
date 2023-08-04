from address_book import City, Street, House, Country, AddressBook, Name, Phone, Record, Field, Birthday, WrongDateError, WrongPhoneFormat, NoDateError
from pickle import load

adress_book = AddressBook()

filename = 'address_book.bin'

def input_error(func):
    
    def wrapper(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return 'wrong name, please try again'
        except ValueError:
            return 'wrong format, please try again'
        except IndexError:
            return 'Please enter some data'
        except WrongDateError:
            return 'Plaese enter a DOB in format x(x).x(x).xxxx'
        except WrongPhoneFormat:
            return 'Please enter a phone in format "380123456789"'
        except NoDateError:
            return 'There is no DOB in this contact'

    return wrapper


@input_error
def generator_records(*args):
    num = args[0]
    i = 0
    if len(adress_book) < int(num):
        return f'There are only {len(adress_book)} record(s) in the adress_book, but you entered {num}'
    for val in adress_book.values():
        if i == int(num):
            break
        i += 1
        print(val)
    return 'Success!'


@input_error
def add_address(*args):
    name = Name(args[0])
    rec: Record = adress_book.get(str(name))
    country = Country(args[1])
    city = City(args[2])
    if rec:
        if len(args) == 5:
            street = Street(args[3])
            house = House(args[4])
            return rec.add_address(country, city, street, house)
        elif len(args) == 4:
            street = Street(args[3])
            return rec.add_address(country, city, street)
        else:
            return rec.add_address(country, city)
    return f'There is no contact with name: {name}'
        
            

@input_error
def find_by_name(*args):
    name = args[0]
    lst_data = adress_book.read_from_file()
    lst_result = adress_book.find_rec_by_name(name, lst_data)
    if len(lst_result) != 0:
        for rec in lst_result:
            print(rec)
        return 'Success'
    return 'No matches'


@input_error
def find_by_nums(*args):
    phone = args[0]
    lst_data = adress_book.read_from_file()
    lst_result = adress_book.find_rec_by_phone(phone, lst_data)
    if len(lst_result) != 0:
        for rec in lst_result:
            print(rec)
        return 'Success'
    return 'No matches'


@input_error
def read_from_file(*args):
    data = adress_book.read_from_file()
    print(data)
    if len(data) != 0:
        for rec in data:
            for name, data in rec.items():
                print(f'{name}: phone(s) {data.phones}, birthday ({data.birthday}), address ({data.address})')
        return 'Success'
    return 'No data was added'


@input_error
def find_phone(*args):
    name = args[0]
    if name in adress_book.keys():
        rec: Record = adress_book.get(name)
        return f'name: {name}, phone: {rec.phones}'
    return f'name: {name} is not present'

    
@input_error
def show_all(*args):
    return adress_book


@input_error
def hello(*args):
    return 'How can I help you?'


@input_error
def change_phone(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = adress_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


@input_error
def days_to_birthday(*args):
    name = args[0]
    if name in adress_book.keys():
        rec: Record = adress_book.get(str(name))
        return rec.days_to_birthday()
    return f"you haven't included date of birth or you have included wrong name"


@input_error
def add_command(*args):
    name = Name(args[0])
    rec: Record = adress_book.get(str(name))

    if rec:
        phone = Phone(args[1])
        return rec.add_phone(phone)
    
    if len(args) == 1:
        rec = Record(name)
        return adress_book.add_record(rec)
    
    elif len(args) == 2:
        phone = Phone(args[1])
        rec = Record(name, phone)
        return adress_book.add_record(rec)

    elif len(args) == 3:
        phone = Phone(args[1])
        birthday = Birthday(args[2])
        rec = Record(name, phone, birthday)
        return adress_book.add_record(rec)
    return 'something wrong, please try again'


def no_command(*args):
    return 'Unknown command'


dict_of_func = {
                'add': add_command,
                'change': change_phone, 
                'phone': find_phone, 
                'hello': hello, 
                'show_all': show_all,
                'birthday' : days_to_birthday,
                'generate' : generator_records,
                'read' : read_from_file,
                'find_num' : find_by_nums,
                'find_name' : find_by_name,
                'add_address': add_address
                }


@input_error
def parser(text: str) -> tuple[callable, tuple[str]]:
    func_name_num = text.split()
    if func_name_num[0] in dict_of_func.keys():
        return dict_of_func.get(func_name_num[0]), text.replace(func_name_num[0], '').strip().split()
    return no_command, text.replace(func_name_num[0], '').strip().split()
    

def main():
    adress_book.load_from_file(filename)
    while True:
        user_input = input('>>>')
        if user_input.lower() == 'exit' or user_input.lower() == 'close' or user_input.lower() == 'good bye':
            adress_book.save_to_file(filename)
            print('Bye!')
            break
        if user_input == '' or user_input == ' ':
            print(no_command(user_input))
            continue
        command, data = parser(user_input.lower())
        result = command(*data)
        print(result)


if __name__ == '__main__':
    main()