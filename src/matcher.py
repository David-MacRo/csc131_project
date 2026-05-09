from form_700 import load_names, load_interests, load_name_interest_dict
def match(matter_files: list) -> list:
    NAMES = load_names()
    INTERESTS = load_interests()
    NAME_INTEREST_DICT = load_name_interest_dict()

    # first stage has the most files
    # so do the simplest check which removes the most files
    files_with_interests = []
    for file in matter_files:
        if check_file(file, INTERESTS):
            files_with_interests.append(file)

    print("files with interests:")
    print(files_with_interests)

    # less performant checks, but less files *to* check
    files_with_conflicts = []
    for name in NAMES:
        for file in files_with_interests:
            if check_file(file, [name]):
                if check_file(file, [NAME_INTEREST_DICT[name]]):
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
                        return True
    except:
        print(f"File read failure in matcher: {filename}")
    return False
