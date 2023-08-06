from notes_class import Notebook, Note


note_book = Notebook()

OPTIONS_SEARCH = {
        1: ["name", "text"],
        2: ["content", "text"],
        3: ["tags", "text"],  
        4: ["status", "true/false"],
        5: []
    }

def get_input_int():
    try:
        user_input = int(input("Виберіть номер: "))
        return user_input
    except ValueError:
        print("!!! Помилка: Введіть число:")
        return get_input_int()

def edit_note(record):
    print(f"Знайдено запис: \n{record}"
            "\n.............."
            "\nМеню запису:"
            "\n1. видалити"
            "\n2. редагувати"
            "\n3. змінити статус"
            "\n4. головне меню")
    option = get_input_int()
    
    if option == 1:
        pass   
    elif option == 2:
        pass
    elif option == 3:
        pass
    elif option == 4:
        record = None
        return
    else:
        print("Некоректний вибір. Спробуйте ще раз.")



def search_note(option):
    try:
        search_params = OPTIONS_SEARCH[option]
    except KeyError:
        print("!!! Помилка: Невірний вибір параметра пошуку")
        return

    if not search_params:
        return

    search_term = input(f"Введіть значення для пошуку в {search_params[0]} (format input: {search_params[1]}): ")
    
    result = (note_book.search_in_notes(search_params[0], search_term))
    
    if len(result) == 1:
        return edit_note(result[0])
    
    elif len(result) > 0:
        dict_results = {i+1: record for i, record in enumerate(result)}
        for id, record in dict_results.items():
            print(id, record)
        option = get_input_int()       
        if option in dict_results: 
            selected = dict_results[option]
            return edit_note(selected)
    else:
        print("Результатів пошуку немає")
        return search_menu()


def search_menu():
    while True:
        print(".............."
            "\nПошук в нотатках:"
            "\n1. за назвою"
            "\n2. за вмістом"
            "\n3. за тегом"
            "\n4. за статусом"
            "\n5. повернутися на головне меню")
    
        option = get_input_int()  
        search_note(option)
        if option in OPTIONS_SEARCH:
            break


def show_comand():
    print("Всі нотатки:")
    print(note_book, '\n')
    #input("повернутися в Меню (натиснути Enter)")


def main():
    note_book.load_json('notebook.json')
    print("Notebook дані завантажено.")

    while True:
        print(".............."
            "\nМеню нотатків:"
            "\n1. показати всі"
            "\n2. створити"
            "\n3. пошук"
            "\n4. вийти")
        
        user_input = get_input_int()

        if user_input == 1:
            show_comand()

        elif user_input == 2:
            pass

        elif user_input == 3:
            search_menu()

        elif user_input == 4:
            note_book.save_json('notebook.json')
            print("Notebook дані збережено.")
            break

        else:
            print("Некоректний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
