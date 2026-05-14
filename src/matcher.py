from concurrent.futures import ThreadPoolExecutor
import json
import urllib
import time

from agendas import get_event_item_ids_from_file
from config import DATA_PATH, SLASH, BASE_URL
from form_700 import load_names, load_interests, load_name_interest_tuples

def match(matter_files: list) -> list:
    NAMES = load_names()
    INTERESTS = load_interests()
    NAME_INTEREST_TUPLES = load_name_interest_tuples()
    EVENT_ITEM_ID_DICT = get_event_item_ids_from_file()

    # first stage has the most files
    # so do the simplest check which removes the most files
    print("Searching texts for interest...")
    files_with_interests = []
    for file in matter_files:
        interests = check_file(file, INTERESTS)
        if(len(interests) > 0):
            files_with_interests.append([file, interests])
    print(f"    Found {len(files_with_interests)} text(s) with interests.")
    #define thread task for threading
    def thread_task(tuple):
        filename = tuple[0]
        interests = tuple[1]
        names = []
        conflicts = []
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
        for event_item_ID, matter_ID in EVENT_ITEM_ID_DICT:
            if(file_matter_ID == matter_ID):
                file_event_item_ID = event_item_ID
        
        #name + eventItemID -> votes
        data = json.loads(_urlopen(f"{BASE_URL}/eventitems/{file_event_item_ID}/votes/"))

        #voted -> conflict
        for name, interest in names:
            for voter in data:
                voter_name = voter["VotePersonName"].lower()
                if(name == voter_name):
                    vote_value_name = voter["VoteValueName"]
                    if((vote_value_name == "Aye") | (vote_value_name == "Nay")):
                        conflict = {"name":name, "interest":interest, "file":filename, "vote":vote_value_name, "matterID": file_matter_ID}
                        if conflict not in conflicts:
                            conflicts.append(conflict)
        return conflicts

    # less performant checks, but less files *to* check
    print("Starting threads to match each text...")
    WORKERS = 100
    output = []
    
    with ThreadPoolExecutor(max_workers = WORKERS) as exe:
        iter = exe.map(thread_task, files_with_interests)
    print("    Threads complete.")

    for file_return_list in iter:
        if(file_return_list is not None):
            output.extend(file_return_list)
    print(f"    Found {len(output)} conflict(s).")

    #for filename, interests in files_with_interests:
       
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