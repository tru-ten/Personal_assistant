from notes_class import Notebook


note_book = Notebook()


def show_comand():
    print("Всі нотатки:")
    print(note_book)
    input("повернутися в Меню (натиснути Enter)")


def main():
    note_book.load_json('notebook.json')
    print("Notebook дані завантажено.")

    while True:
        print("Меню:"
            "\n1. Створити новий нотаток"
            "\n2. Показати всі нотатки"
            "\n3. Пошук нотатку за тегом"
            "\n4. Видалити нотатку"
            "\n5. Вийти")
        user_input = int(input("Виберіть опцію: "))

        if user_input == 1:
            pass

        elif user_input == 2:
            show_comand()

        elif user_input == 3:
            pass

        elif user_input == 4:
            pass

        elif user_input == 5:
            note_book.save_json('notebook.json')
            print("Notebook дані збережено.")
            break

        else:
            print("Некоректний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
