import pathlib
from normalize import normalize
import shutil

EXTENSIONS = {"images": [".jpg", ".gif", ".png", ".jpeg", ".svg"],
              "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
              "audio": [".mp3", ".ogg", ".aiff", ".wav", ".amr"],
              "video": [".avi", ".mp4", ".mov", ".mkv"],
              "archives": [".zip", ".rar", ".gz", ".tar"]}

CATEGORIES = {}

for key, exts in EXTENSIONS.items():
    for ext in exts:
        CATEGORIES[ext] = key


class UnsortedFile:
    def __init__(self, path: pathlib.Path):
        if not path.exists() or path.is_dir():
            raise ValueError("File doesn't exist or it's a folder")
        self.__path = path

    def normalize_name(self):
        normalized_str_name = normalize(self.stem)
        self.__path = self.__path.with_stem(normalized_str_name)

    def move(self, target_dir: pathlib.Path):
        if not target_dir.exists():
            target_dir.mkdir()
        new_name = target_dir.joinpath(self.name)
        while new_name.exists():
            new_name = new_name.with_stem(f"{new_name.stem}_1")
        self.__path = self.__path.replace(new_name)

    @property
    def category(self):
        return CATEGORIES.get(self.suffix, "other")

    @property
    def suffix(self):
        return self.__path.suffix

    @property
    def stem(self):
        return self.__path.stem

    @property
    def name(self):
        return self.__path.name

    @property
    def absolute(self):
        return str(self.__path.absolute())


class Sorter:
    def __init__(self, path: pathlib.Path):
        self.root = path
        if not self.root.exists() or self.root.is_file():
            raise ValueError("This path doesn't exist or it's a file")
        self.to_iter = list(self.root.glob("**/*"))
        self.paths = {category: self.root /
                      category for category in EXTENSIONS}
        self.paths["other"] = self.root / "other"
        self.is_sorted = False
        self.contains_archives = False
        self.__present_exts = {category: set() for category in EXTENSIONS}
        self.__present_exts["other"] = set()
        self.__present_files = {category: [] for category in EXTENSIONS}
        self.__present_files["other"] = []

    def delete_empty_dirs(self):
        for path in self.to_iter:
            if path.is_dir() and not path.name in EXTENSIONS and path.name != "other":
                shutil.rmtree(path)

    def sort(self):
        for path in self.to_iter:
            if path.is_file():
                file = UnsortedFile(path)
                cat = file.category
                file.move(self.paths[cat])
                file.normalize_name()
                self.__present_exts[cat].add(file.suffix)
                self.__present_files[cat].append(file.absolute)
        self.delete_empty_dirs()
        self.is_sorted = True
        self.contains_archives = self.paths['archives'].exists()

    def unpack_archives(self):
        if not self.is_sorted:
            raise ValueError("Sort folder first to unpack archives!")
        if not self.contains_archives:
            raise ValueError("No archives found!")
        for arch in self.paths["archives"].iterdir():
            try:
                shutil.unpack_archive(
                    str(arch), self.paths["archives"] / arch.stem)
            except Exception:
                continue

    def print_result(self):
        for category in [*EXTENSIONS.keys(), "other"]:
            print(f"\nFIle of category {category}:")
            if len(self.__present_files[category]) == 0:
                print(f"Category {category} is empty")
            else:
                print("\n".join(self.__present_files[category]))
                print(
                    f"Extensions of category {category}: {self.__present_exts[category]}")


def main():
    str_path = input("Enter path to folder to sort: ")
    path = pathlib.Path(str_path)
    if not path.exists():
        return f"Folder with path {path} doesn't exist"
    really = input(
        f"Do you really want to sort folder {path.absolute()}? (y/n)")
    if really != "y":
        return "Sort interrupted"
    sorter = Sorter(path)
    sorter.sort()
    if sorter.contains_archives:
        to_unpack = input("\nDo you want to unpack archives? (y/n)")
        if to_unpack == "y":
            sorter.unpack_archives()
    sorter.print_result()
    return "Ok"


if __name__ == "__main__":
    print(main())
