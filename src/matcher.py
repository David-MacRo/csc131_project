from agendas import get_event_item_ids_from_file
from config import DATA_PATH, SLASH, BASE_URL
from form_700 import load_names, load_interests, load_name_interest_tuples

import json
import urllib
import time
FOUND_INTEREST = ""
def match(matter_files: list) -> list:
    NAMES = load_names()
    INTERESTS = load_interests()
    NAME_INTEREST_TUPLES = load_name_interest_tuples()
    EVENT_ITEM_ID_DICT = get_event_item_ids_from_file()

    # first stage has the most files
    # so do the simplest check which removes the most files
    print("Searching for matches...")
    files_with_interests = []
    for file in matter_files:
        interests = check_file(file, INTERESTS)
        if(len(interests) > 0):
            files_with_interests.append([file, interests])

    # print("files with interests:")
    # print(files_with_interests)

    # less performant checks, but less files *to* check
    '''
    output = []
    for file, interest in files_with_interests.items():
        for key, name in NAME_INTEREST_DICT.items():
            if key is None:
                continue
            if interest.get("interest") in key.lower():
                output.append({"name": name, "interest" : key.split("#")[0], "file" : file})
    '''

    output = []
    for filename, interests in files_with_interests:
        names = []
        #conflict -> names
        for tuple in NAME_INTEREST_TUPLES:
            for entry in tuple[1:]:
                for interest in interests:
                    if(interest == entry):
                        names.append([tuple[0], interest])
        #filename -> matter ID
        file_matter_ID = int("".join(char for char in filename if char.isdigit()))
        
        #matterID -> eventItemID
        file_event_item_ID = 0
        for event_ID, pairs in EVENT_ITEM_ID_DICT.items():
            for event_item_ID, matter_ID in pairs:
                if(file_matter_ID == matter_ID):
                    file_event_item_ID = event_item_ID
        
        #name + eventItemID -> votes
        data = json.loads(_urlopen(f"{BASE_URL}/eventitems/{file_event_item_ID}/votes/"))

        #voted -> conflict
        for name, interest in names:
            for voter in data:
                voter_name = voter["VotePersonName"].lower()
                if(name == voter_name):
                    print("Found!")
                    print(voter)
                    '''
                    {
                        'VoteId': 6835, 
                        'VoteGuid': 'A2C3F851-3A0D-49D6-9892-3AB5FDD1CB91', 
                        'VoteLastModifiedUtc': '2019-12-26T18:37:34.82', 
                        'VoteRowVersion': 'AAAAAABONqQ=', 
                        'VotePersonId': 547, 
                        'VotePersonName': 'Lynda Hopkins', 
                        'VoteValueId': 16, 
                        'VoteValueName': 'Aye', 
                        'VoteSort': 5, 
                        'VoteResult': 1, 
                        'VoteEventItemId': 29394
                    }
                    '''
                    vote_value_name = voter["VoteValueName"]
                    if((vote_value_name == "Aye") | (vote_value_name == "Nay")):
                        conflict = {"name":name, "interest":interest, "file":filename, "vote":"TODO"}
                        print(conflict)
                        output.append(conflict)
    
    # print("files_with_conflicts:")
    # print(files_with_interests)
    output_matches(output)

def output_matches(output):
    with open(f"{DATA_PATH}{SLASH}conflicts.json", "w") as file:
        json.dump(output, file, indent=4)

def check_file(filename: str, keys: list) -> list:
    found = []
    try: 
        with open(filename, "r") as file:
            contents = file.read().lower().split()
            for word in contents:
                for key in keys:
                    key = key.lower()
                    if key in word:
                        found.append(key)
    except Exception as e:
        print(e)
        print(f"File read failure in matcher: {filename}")
    return found

def _urlopen(url: str) -> any:
    wait_length = 0.5
    while True:
        wait_length = wait_length * 2
        try:
            with urllib.request.urlopen(url, timeout=20) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            print(f"  [HTTP {exc.code}] {url}")
            time.sleep(wait_length)
        except Exception as exc:
            print(f"  [ERROR] {url} – {exc}")
            time.sleep(wait_length)