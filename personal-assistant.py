# Внаслідок перейменування пакетів оновлено імпорт пакетів
from contact_book_functions import parse_input, exit_command

def main():
    while True:
        user_input = input('\nEnter your command and args: ')
        
        cmd, data = parse_input(user_input)
        
        result = cmd(*data)
        
        print(result)
        # Вихід з бота пропоную роботи не через Enter, бо це може бути випадково зроблене. А лише якщо користувач введе команду на вихід
        if cmd == exit_command:   
            break

if __name__ == "__main__":
    main()