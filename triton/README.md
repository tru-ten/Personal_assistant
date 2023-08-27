# Personal assistant TRITON

TRITON is a personal assistant for:

1. saving personal data of customers (or user contacts), such as name, phone numbers, address, email and birthdays;
2. saving notes with hashtags, with the ability to search, edit, delete, and sort them;
3. sorting files in the specified folder by categories (images, documents, videos, etc.).

### Installation

1. Download repository
2. Run setup.py file
3. Run pip install -e . in cmd in directory of projects

### Requirements

- Python 3.6 or newer

### Contributing and Improvements

Feature requests and bug fixes are welcome!

To contribute:

1. Fork this repository
2. Make changes and commit to your fork
3. Open a pull request to the main branch

### License

This project is released under the MIT License.

-----------------------------------------------
 
"Never memorise something that you can look up."
Albert Einstein
 
Once a colleague of a prominent physicist asked him for his phone number. And Einstein took out his notebook to dictate his number to him. So we believe that there is no need to fill your memory with information that can be easily found and noted down.
"Your personal assistant" (hereinafter - TRITON) is made so that you can easily get the necessary information, make changes and delete what you do not need.
Our application has three auxiliary functions:
1.	`Contacts book`
2.	`Notebook`
3.	`File sorter`
 
Now in more detail by section.
## 1.Working with the contact book.
TRITON knows how to do everything necessary so that you can easily find out information about loved ones, or just people with whom you are in contact.
TRITON adds, changes and deletes records about the user (name, telephone numbers, date of birth, e-mail address, residential address). For most fields in the record, check for the veracity of the entered information is taken into account.
- The phone must be in the format +380XXXXXXXXX, that is, we currently work with Ukrainian phone numbers. The phone number must start with the phone code "+380" and 9 more digits.
- Date of birth is entered in "dd.mm.YYYY" format. The input format is the most common, so it is taken as a basis. Birthday class fields of datetime type.
- The e-mail has a check that the characters "@" and "." must be present, and the domain name must consist of at least two letters.
- The address consists of four fields: Country, City, Street, House. Mandatory field "Country", it is checked for correctness using the list of all existing countries in the `countries.txt` directory.
TRITON is good at handling user birthday data and has many useful methods.
- You can find out how many days until the birthday of the selected user and, most importantly, what anniversary he will celebrate.
- Displays a date-sorted list of users celebrating birthdays `next week`, `next month`, `current week`, `current month`.
- Returns a date-sorted list of users who have a birthday within the entered number of days from today's date.
- You can even find out how many days a user lives in his life (if you are already so curious).
A search for the entire contact book is also implemented (the condition is at least 2 characters). Returns a list of all contacts where the search query is found.
When starting work with the contact book, the information is deserialized from the `contact_book.bin` file, if it does not exist, it is automatically created for work. And upon completion of work, all information is serialized. The pickle module was used for serialization.
TRITON displays a list of all contacts, can sort them by name or age of the user. Also displays information about the selected user.
The user can always get information about available operations at any stage of work by calling `help`. For convenience, you can enter a short command consisting of two numbers or the full name of the command. For example, `55` and `show all` are equivalent.
Also, TRITON is able to guess the command that the user wants to enter, if he accidentally mixed up characters. For example, when entering `aad user`, `edd user`, `dad user`, TRITON will analyze and offer to enter the correct `add user` command.

## 2. Working with a notebook.

Notebook is designed for creating, editing, searching and organizing text notes.

### Key Features

- Create, edit, and delete textual notes with titles and content
- Add multiple tags to notes for easy filtering and organization
- Search notes by title, content, tags, or status (active/inactive)
- Sort notes alphabetically by tags
- Display notes paginated for convenient viewing
- Save all notes to a JSON file and load them from there
- Support for Ukrainian and English languages
- Intuitive command-line interface

### Usage

The main menu provides these core options:

- View all notes
- Create a new note
- Find a note by parameters
- Sort notes by tags
- Save data and exit

Follow the prompts in the interface to create notes, add tags, search for entries, and more.

All notes are saved locally to the `notebook.json` file. This file is automatically created on first run if it doesn't exist.

On exit, all changes are automatically saved to `notebook.json`.

### Implementation

The Notebook class stores all notes in an internal dictionary and performs create, read, update, and delete operations.

Data is persisted using JSON serialization.


## 3. File sorter.

The file sorter is designed to sort files by categories: images, documents, audio, video, archives, other. The sorting takes place according to the file extension, namely:

- "images": jpg, gif, png, jpeg, svg;
- "documents": doc, docx, txt, pdf, xlsx, pptx;
- "audio": mp3, ogg, aiff, wav, amr,
- "video": avi, mp4, mov, mkv,
- "archives": zip, rar, gz, tar.

All files whose extensions are not included in the list will be sorted into the folder "other".
After starting the sorter, on request
`"Enter path to folder to sort: "`
You must enter the full path to the folder you want to sort.
To avoid accidental folder sorting, you will need to confirm that the user definitely wants to sort the specified folder.
When files with the same names are found, "_1" (underline with 1) will be added to the name of each subsequent copy, as many times as the file will be repeated.
When moving files, their names will be normalized - Cyrillic characters are converted to Latin, `"%", "\*", " ", "-", "."` replaced by underline.
If archives are found in the folder being sorted, they will be moved to the "archives" folder and an additional clarifying question will be displayed:
`Do you want to unpack archives? (y/n).`
If the answer is positive, a folder with the name of the archive will be created in the "archives" folder and the archive will be unpacked into it. If it is impossible to unpack, the message "Can't unpack" and the name of the corresponding archive will be displayed.
After sorting, a list of files by category will be displayed.
If certain files are added to the sorted folder, you can repeat the sorting procedure. Be careful, if the archives were unpacked, they will be sorted into folders.
