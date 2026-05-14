from form_700 import load_names, load_interests, load_name_interest_dict
from config import DATA_PATH, SLASH
import json

FOUND_INTEREST = ""
def match(matter_files: list) -> list:
    NAMES = load_names()
    INTERESTS = load_interests()
    NAME_INTEREST_DICT = load_name_interest_dict()

    # first stage has the most files
    # so do the simplest check which removes the most files
    print("Searching for matches...")
    files_with_interests = {}
    for file in matter_files:
        found_match, interest = check_file(file, INTERESTS)
        if found_match:
            files_with_interests.update({file : {"interest" : interest}})

    # print("files with interests:")
    # print(files_with_interests)

    # less performant checks, but less files *to* check
    output = []
    for file, interest in files_with_interests.items():
        for key, name in NAME_INTEREST_DICT.items():
            if key is None:
                continue
            if interest.get("interest") in key.lower():
                output.append({"name": name, "interest" : key.split("#")[0], "file" : file})
    
    # print("files_with_conflicts:")
    # print(files_with_interests)
    output_matches(output)

def output_matches(output):
    with open(f"{DATA_PATH}{SLASH}conflicts.json", "w") as file:
        json.dump(output, file, indent=4)

def check_file(filename: str, keys: list) -> bool:
    try: 
        with open(filename, "r") as file:
            contents = file.read().lower().split()
            for word in contents:
                for key in keys:
                    key = key.lower()
                    if key in word:
                        return True, key
    except:
        print(f"File read failure in matcher: {filename}")
    return False, None
