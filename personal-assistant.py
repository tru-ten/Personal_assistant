from contact_book_main import main as main_contactbook
from notes_main import main as main_notebook
from sort_folder import main as main_sorter

invitation_text = "\nHello! I'm glad you're back. Let's start!!!\n"

def main():
    print(invitation_text)
    while True:
        user_input = input("Enter number from 1, 2 or 3 to start work with branch(press 0 to exit): ")
        if user_input == '1':
            print()
            main_contactbook()
        elif user_input == '2':
            main_notebook()
        elif user_input == '3':
            print(main_sorter())


        elif user_input == '0':
            confirm = input('\nAre you sure you want to finish work with Personal Assistant? Type (Y/N):')
            if confirm.lower() != 'y':
                print()
                continue  
            else: 
                break
        
        else:
            print('\nUnknown command. Type command from the list.\n')
            
        
if __name__ == "__main__":
    main()