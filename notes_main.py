from notes_class import Notebook, Note, Field, Tag

note_book = Notebook()

OPTIONS = {
        1: ["name", "text", Field],
        2: ["content", "text", Field],
        3: ["tags", "text", list],  
        4: []
    }

def get_input_int():
    try:
        user_input = int(input("Select a number >>> "))
        return user_input
    except ValueError:
        print("> Error. Enter a number.")  
    except KeyError:
        print("> Incorrect selection. Try again.")
    return get_input_int()

def numerator(list_result):
    print("")
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
    print(f"> Found note: \n{note}"
            f"\n\n{'Note menu':.^40}"
            "\n1 - delete"
            "\n2 - edit" 
            "\n3 - return to main menu")
    option = get_input_int()
    if option == 1:
        return note_book.delete_in_note(note) 
    elif option == 2:
        return note_menu("Notes Editor", edit_note, note)
    elif option == 3:
        return

def search_tags(note):
    search = input("Enter value for tags field (format input: text) >>> ")
    tag_list = note_book.search_in_tags(search)
    tag = numerator(tag_list)
    if tag:  
        print(f"tag {tag} found")
        return tag
    else:
        print("No search results found"
            "\n1 - add new tag"
            "\n2 - return to menu")
        option = get_input_int()
        if option == 1:
            add_tag_in_note(search, note)
        elif option == 2:
            return edit_tag(note)
        else:
            print("> Error. Enter a number.")
            return edit_tag(note)

def add_tag_in_note(tag_name, note):
    new_tag = Tag(tag_name)
    note.add_tag_in_tags(new_tag)
    note_book.add_tag_note(new_tag)
    return edit_tag(note)

def search_tag_in_tegs():
    list_tags = note_book.get_tag_values()
    if len(list_tags) == 0:
        tag = ' '
        return tag
    tag = numerator(list_tags)
    return tag

def search_tag_in_note(note):
    list_tags = note.get_tags()
    for index, tag in enumerate(list_tags):
        print(index + 1, tag)
    option_input = get_input_int()
    print(index)
    print(option_input)
    if index + 2 > option_input:
        option_input =-1
        tag = list_tags[option_input]
    else:
        print("> Error. Enter a number.")
        return search_tag_in_note(note)
    return tag

def edit_tag(note):
    while True:
        print(f"> Record: {note}"  
            f"\n\n{'Tag menu':.^40}"
            "\n1 - delete"
            "\n2 - add" 
            "\n3 - return to record menu")
        option = get_input_int()
        if option == 1:
            tag_search = search_tag_in_note(note)
            if tag_search:
                note.delete_tag_from_note(note, tag_search)
        elif option == 2:  
            tag_search = search_tags(note)
            print(tag_search)
            if tag_search != None:
                tag = Tag(tag_search) 
                note.add_tag_in_tags(tag)     
        elif option == 3:
            return content_note(note)

def edit_note(option, note):
    if option == 4:
        note_book.edit_status_in_note(note)
        return note_menu("Notes Editor", edit_note, note)
    try:
        search_params = OPTIONS[option]
    except KeyError:
        print("> Error: Invalid search parameter selected")
        return content_note(note)
    if not search_params:
        return print("> Error: Invalid search parameter selected")  
    if search_params[0] == "tags":
        return edit_tag(note)
    if search_params[0] == "status":
        return note_book.edit_status_in_note(note) 
    input_content = input(f"Enter search value for {search_params[0]} (format input: {search_params[1]}) >>> ")
    new_value = Field(input_content)
    note_book.edit_in_note(note, search_params[0], new_value)

def search_note(option, note):
    try:
        search_params = OPTIONS[option]
    except KeyError:
        print("> Error: Invalid search parameter selected") 
        return
    if not search_params:
        if option == 4:
            print(f"Enter value for status field (format input: True(1)/False(2))")
            input_status = get_input_int()
            if input_status == 1:
                search_status = True
            elif input_status == 2:
                search_status = False
            else:
                print("> Incorrect selection. Try again.")
                return search_note(option, note) 
            list_result = note_book.search_in_notes("status", search_status)
    else: 
        search_term = input(f"Enter value for {search_params[0]} field (format input: {search_params[1]}) >>> ")
        list_result = note_book.search_in_notes(search_params[0], search_term)
    
    result = numerator(list_result)
    if result:
        content_note(result)
    else:
        print("No search results found")
        return note_menu("Search in notes", search_note)

def note_menu(name, func, note=None):
    while True:
        print(f"\n{name:.^40}"
                "\n1 - by name"
                "\n2 - by content"
                "\n3 - by tag"
                "\n4 - by status"
                "\n5 - return to main menu")
        option = get_input_int()  
        return func(option, note)
    
def add_note():
    print("Create a note")
    name = input("Enter a name for the note: >>>")
    name = Field(name)
    content = input("Enter the content of the note: >>>")
    content = Field(content)
    note = Note(name, content)
    note_book.add_note(note)
    
    while True:
        print("1 add tag\n2 continue")
        option = get_input_int()
        if option == 1:
            tag = search_tag_in_tegs()
            if tag is not None:
                if tag == ' ':
                    print('The tag list is empty\n')
                    break
                tag = Tag(tag) 
                if tag not in note.tags:
                    note.add_tag_in_tags(tag)
                    print(f"A new tag {tag} has been added to the recording {name}")
            else:
                print(f"The tag {tag} already exists")
        elif option == 2:
            break

    print(note_book.add_note(note))

def show_comand(et_list, n):
    if n:
        result = ''
        page = 1
        for note in note_book.iterator(et_list, n):
            result = ''
            text = f"page {page}" 
            result += f"{text:.^80}\n" + note
            page += 1
            print(result)
            input("Next page (press Enter)")
    else:
        return note_book

def main(): #
    note_book.load_json('notebook.json')
    print("> Notebook data loaded.")

    while True:
        print(f"\n{'Notebook menu:':.^40}"
            "\n1 - show all notes"
            "\n2 - create note"
            "\n3 - search in notes"
            "\n4 - sort by tags"
            "\n5 - exit")
        
        user_input = get_input_int()

        if user_input == 1:
            print(f"\n{'All notes':.^80}")
            show_comand(note_book.values(), n=7)

        elif user_input == 2:
            add_note()

        elif user_input == 3:
            note_menu("Search in notes", search_note)

        elif user_input == 4:
            sorted_notes = note_book.sort_by_tags()
            print(f"\n{'Sort by tags':.^80}")
            show_comand(sorted_notes, n=7)

        elif user_input == 5:
            note_book.save_json('notebook.json')
            print("> Notebook data saved.")
            break

        else:
            print("> Incorrect selection. Try again.")

if __name__ == "__main__":
    main()
