from form_700 import load_names, load_interests, load_name_interest_dict

FOUND_INTEREST = ""
def match(matter_files: list) -> list:
    NAMES = load_names()
    INTERESTS = load_interests()
    NAME_INTEREST_DICT = load_name_interest_dict()

    # first stage has the most files
    # so do the simplest check which removes the most files
    files_with_interests = {}
    for file in matter_files:
        found_match, interest = check_file(file, INTERESTS)
        if found_match:
            files_with_interests.update({file : interest})

    print("files with interests:")
    print(files_with_interests)

    # less performant checks, but less files *to* check
    files_with_conflicts = []
    for name in NAMES:
        for file in files_with_interests.keys():
            found_match, interest = check_file(file, NAME_INTEREST_DICT.get(name))
            if found_match:
                files_with_conflicts.append(file)
    
    print("files_with_conflicts:")
    print(files_with_conflicts)



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
