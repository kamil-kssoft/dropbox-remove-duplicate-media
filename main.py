import json
from duplicates.find_duplicates import find_duplicates
from duplicates.get_unique_directories import extract_unique_paths
from duplicates.remove_duplicates import remove_duplicates
from duplicates.resolve_original_files import resolve_original_files
from store.group_files import group_files
from store.move_files import move_files


with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

while True:
    print("Choose option:")
    print("1 - store files")
    print("2 - group files")
    print("3 - generate metadata for duplicated files")
    print("4 - extract unique paths from duplicates")
    print("5 - identify original files and their duplicates")
    print("6 - remove duplicates")
    print("0 - exit")

    option = input("Option: ")

    if option == "1":
        move_files(config)
    elif option == "2":
        group_files(config)
    elif option == "3":
        find_duplicates(config)
    elif option == "4":
        extract_unique_paths()
    elif option == "5":
        resolve_original_files(config)
    elif option == "6":
        remove_duplicates(config)
    elif option == "0":
        break
    else:
        print("Unknown option")
        input()

    print()
    print()