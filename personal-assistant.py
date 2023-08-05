from functions import parse_input

def main():
    while True:
        user_input = input('=> ')
        handler, args = parse_input(user_input)
        result = handler(args)
        if not result:
            print('Exit')
            break
        print(result)

if __name__ == "__main__":
    main()