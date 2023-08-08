from notes_class import Notebook, Note, Field, Tag

note_book = Notebook()

OPTIONS = {
        1: ["name", "text", Field],
        2: ["content", "text", Field],
        3: ["tags", "text", list],  
        4: ["status", "true/false"],
        5: []
    }

def get_input_int():
    try:
        user_input = int(input("Виберіть номер: "))
        return user_input
    except ValueError:
        print("Помилка. Введіть число.")  
    except KeyError:
        print("Некоректний вибір. Спробуйте ще раз.")
    return get_input_int()

def numerator(list_result):
    if len(list_result) > 0:
        dict_results = {i+1: record for i, record in enumerate(list_result)}
        for id, record in dict_results.items():
            print(id, record)
        option_input = get_input_int()
        if option_input in dict_results:
            result = dict_results[option_input]
            return result
    elif len(list_result) == 0:
        return None

def content_note(note):
    print(f"Знайдено запис: \n{note}"
            "\n.............."
            "\nМеню запису:"
            "\n1. видалити"
            "\n2. редагувати"
            "\n3. змінити статус"
            "\n4. головне меню")
    option = get_input_int()
    if option == 1:
        return note_book.delete_in_note(note) 
    elif option == 2:
        return note_menu("Редактор нотатків:", edit_note, note)
    elif option == 3:
        return note_book.edit_status_in_note(note) 
    elif option == 4:
        return

def search_tags(note):
    search = input(f"Введіть значення для поля tags (format input: text): ")
    tag_list = note_book.search_in_tags(search)
    tag = numerator(tag_list)
    if tag:  
        print(f"знайдено тег {tag}")
        return tag
    else:
        print("Результатів пошуку немає"
              "\n1 додати новий тег"
              "\n2 повернутися в меню")
        option = get_input_int()
        if option == 1:
            add_tag_in_note(search, note)
        elif option == 2:
            return edit_tag(note)

def add_tag_in_note(tag_name, note):
    new_tag = Tag(tag_name)
    note.add_tag_in_tags(new_tag)
    note_book.add_tag_note(new_tag)
    return edit_tag(note)

def search_tag_in_tegs():
    list_tags = note_book.get_tag_values()
    tag = numerator(list_tags)
    return tag

def edit_tag(note):
    while True:
        print(f"Запис: {note}"
            "\n............."
            "\nменю тег"
            "\n1 видалити"
            "\n2 додати"
            "\n3 повернуимсь в меню запису")
        option = get_input_int()
        if option == 1:
            tag_search = search_tag_in_tegs()
            print(tag_search)
            if tag_search:
                tag = Tag(tag_search)
                note.remove_tag(tag)
        elif option == 2:  
            tag_search = search_tags(note)
            tag = Tag(tag_search)    
            note.add_tag_in_tags(tag)     
        elif option == 3:
            return content_note(note)

def edit_note(option, note):
    try:
        search_params = OPTIONS[option]
    except KeyError:
        return print("!!! Помилка: Невірний вибір параметра пошуку")    
    if not search_params:
        return print("!!! Помилка: Невірний вибір параметра пошуку")  
    if search_params[0] == "tags":
        return edit_tag(note)
    if search_params[0] == "status":
        return note_book.edit_status_in_note(note)  
    input_content = input(f"Введіть значення для пошуку в {search_params[0]} (format input: {search_params[1]}): ")
    new_value = Field(input_content)
    note_book.edit_in_note(note, search_params[0], new_value)

def search_note(option, note):
    try:
        search_params = OPTIONS[option]
    except KeyError:
        print("!!! Помилка: Невірний вибір параметра пошуку")
        return
    if not search_params:
        return
    search_term = input(f"Введіть значення для поля {search_params[0]} (format input: {search_params[1]}): ")
    list_result = note_book.search_in_notes(search_params[0], search_term)
    result = numerator(list_result)
    if result:
        content_note(result)
    else:
        print("Результатів пошуку немає")
        return note_menu("Пошук в нотатках:", search_note)

def note_menu(name, func, note=None):
    while True:
        print(".............."
            f"\n{name}"
            "\n1. за назвою"
            "\n2. за вмістом"
            "\n3. за тегом"
            "\n4. за статусом"
            "\n5. повернутися на головне меню")
        option = get_input_int()  
        return func(option, note)
    
def add_note():
    print("Створення нотатка")
    name = input("Введіть назву нотатки: ")
    name = Field(name)
    content = input("Введіть вміст нотатки: ") 
    content = Field(content)
    note = Note(name, content)
    note_book.add_note(note)
    while True:
        print("1 додати тег\n2 продовжити")
        option = get_input_int()
        if option == 1:
            tag = search_tag_in_tegs()
            tag = Tag(tag)
            if tag not in note.tags:
                note.add_tag_in_tags(tag)
                print(f"До запису {name} додано новий тег {tag}")  
            else:
                print(f"Тег {tag} вже існує")
        elif option == 2:
            break
    print(note_book.add_note(note))

def show_comand():
    print("Всі нотатки:")
    print(note_book, '\n')
    input("повернутися в Меню (натиснути Enter)")

def main():
    note_book.load_json('notebook.json')
    print("Notebook дані завантажено.")

    while True:
        print(".............."
            "\nМеню нотатків:"
            "\n1 показати всі"
            "\n2 створити"
            "\n3 пошук"
            "\n4 сортування за тегами"
            "\n5 вийти")
        
        user_input = get_input_int()

        if user_input == 1:
            show_comand()

        elif user_input == 2:
            add_note()

        elif user_input == 3:
            note_menu("Пошук в нотатках:", search_note)

        elif user_input == 4:
            sorted_notes = note_book.sort_by_tags()
            for note in sorted_notes:
                print(note)

        elif user_input == 5:
            note_book.save_json('notebook.json')
            print("Notebook дані збережено.")
            break

        else:
            print("Некоректний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
