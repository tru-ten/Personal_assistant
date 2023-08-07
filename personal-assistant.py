# Внаслідок перейменування пакетів оновлено імпорт пакетів
from contact_book_functions import parse_input, exit_command
import time

def main():
    # Додаю невеликий привітальний текст. Тут в принципі можна й щось інше написати. І ще додав вивід кожного рядка за 1,5 секунди.
    invitation_text = ["Hello. I am your personal assistant.", 
                         "I will help you organize your contact book.", 
                         "Using the command 'help', you can find out the list of available operations.",
                          "Let's start and enjoy!!!" ]
    for string in invitation_text:
        print(string)
        time.sleep(0.1)
    while True:
        
        user_input = input("\nTo see the list of available commands, type 'help'\nEnter your command and args (separated by 'space bar'): ")
        
        cmd, data = parse_input(user_input)
        
        result = cmd(*data)
        
        print(result)
        # Вихід з бота пропоную роботи не через Enter, бо це може бути випадково зроблене. А лише якщо користувач введе команду на вихід
        if cmd == exit_command:   
            break

if __name__ == "__main__":
    main()