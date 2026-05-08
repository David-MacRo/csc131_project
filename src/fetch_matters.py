from concurrent.futures import ThreadPoolExecutor

import json
from config import DATA_PATH, SLASH

def fetch_list(matter_links: list, folder: str):
    #open checked from folder
    with open(f"{DATA_PATH}{SLASH}checked_urls.json", "a") as file:
        checked_urls = json.load(file)
    #remove already checked items from list
    for link in matter_links[:]:
        if link in checked_urls:
            matter_links.remove(link)
    #create threads and split into sublists
        #split lists
        #init threads
    WORKERS = 10
    files = []
    with ThreadPoolExecutor(max_workers = WORKERS) as exe:
        iter = exe.map(thread_task, matter_links)
        files = list(iter)
        

    #await threads

    #merge returned filename sublists

    #write out filename list to folder
    with open(f"{DATA_PATH}{SLASH}checked_matters.json", "a") as file:
        for filename in checked_matters:
            file.write(f"filename\n")
    #append newly checked urls to folder
    with open(f"{DATA_PATH}{SLASH}checked_urls.json", "w") as file:
        checked_urls = json.load(file)
        for link in matter_links:
            checked_urls.append(link)
        file.write(checked_urls)
    #return list of filenames

def thread_task(matter_link: str, folder: str) -> str:    
    filename = f"{folder}/{matter_link}"
    return filename