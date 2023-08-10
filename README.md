# Personal_assistant

## Notebook

Notebook - це консольний додаток записника для створення, редагування, пошуку та організації текстових заміток.

### Основні можливості

- Створюйте, редагуйте та видаляйте текстові замітки з заголовками та вмістом
- Додавайте довільну кількість тегів до заміток для зручної фільтрації та організації
- Шукайте замітки за заголовком, вмістом, тегами або статусом (активна/неактивна)
- Сортуйте замітки за тегами
- Відображайте замітки посторінково для зручного перегляду
- Зберігайте всі замітки в JSON-файл та завантажуйте їх звідти
- Підтримка української та англійської мов
- Інтуїтивний інтерфейс командного рядка

### Використання

Щоб розпочати роботу, запустіть `notes_main.py`.

Головне меню надає такі основні опції:

- Переглянути всі замітки
- Створити нову замітку
- Знайти замітку за параметрами
- Сортувати замітки за тегами
- Зберегти дані та вийти

Дотримуйтесь підказок в інтерфейсі, щоб створювати замітки, додавати теги, шукати потрібні записи тощо.

Всі замітки зберігаються локально у файлі `notebook.json`. Цей файл автоматично створюється при першому запуску, якщо він відсутній.

При виході з програми всі зміни автоматично зберігаються у `notebook.json`.

### Реалізація

Додаток реалізований з використанням об'єктно-орієнтованого підходу та таких основних класів:

- `Field` - представляє текстове поле (назва, вміст тощо)
- `Tag` - представляє тег
- `Note` - представляє окрему замітку
- `Notebook` - представляє колекцію заміток та надає методи для операцій

Клас Notebook зберігає всі замітки у внутрішньому словнику та виконує операції створення, читання, оновлення та видалення.

Збереження даних реалізовано за допомогою серіалізації в JSON.

### Вимоги

- Python 3.6 або новіший

### Внесок та покращення

Пропозиції щодо нового функціоналу та виправлення помилок вітаються!

Щоб долучитися:

1. Зробіть форк цього репозиторію
2. Внесіть зміни та закомітьте їх у свій форк
3. Відкрийте пул-реквест до основної гілки цього репозиторію

### Ліцензія

Цей проєкт поширюється під ліцензією MIT

## Notebook

Notebook is a command-line notebook application for creating, editing, searching, and organizing textual notes.

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

To get started, run `notes_main.py`.

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

The app is implemented using an object-oriented approach with these key classes:

- `Field` - represents a text field (name, content, etc)
- `Tag` - represents a tag
- `Note` - represents an individual note
- `Notebook` - represents a note collection and provides methods

The Notebook class stores all notes in an internal dictionary and performs create, read, update, and delete operations.

Data is persisted using JSON serialization.

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
