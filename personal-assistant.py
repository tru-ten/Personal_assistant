from contact_book_functions import parse_input

def main():
    while True:
        user_input = input('enter command: ')
        handler, args = parse_input(user_input)
        result = handler(args)
        if result == 'good bye!':
            print(result)
            break
        print(result)

if __name__ == "__main__":
    main()