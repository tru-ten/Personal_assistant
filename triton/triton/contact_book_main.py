# Внаслідок перейменування пакетів оновлено імпорт пакетів
from contact_book_functions import parse_input, exit_command, start


def main():
    start()
    while True:
        
        user_input = input("\nTo see the list of available commands, type 'help' or '00'\nEnter your command and args (separated by 'space bar'): ")
        
        cmd, data = parse_input(user_input)
        
        result = cmd(*data)
        
        print(result)
        # Вихід з бота пропоную роботи не через Enter, бо це може бути випадково зроблене. А лише якщо користувач введе команду на вихід
        if cmd == exit_command:  
            break

if __name__ == "__main__":
    main()