from concurrent.futures import ThreadPoolExecutor
import os
import json
import urllib.request
import urllib.error
import time

from config import DATA_PATH, SLASH

def fetch_list(matter_links: list):
    #open checked from folder
    print("Checking filenames...")
    checked_urls = []
    CHECKED_FILENAME = f"{DATA_PATH}{SLASH}checked_urls.json"
    if(os.stat(CHECKED_FILENAME).st_size != 0):
        with open(CHECKED_FILENAME, "r") as file:
            checked_urls = json.load(file)
    #remove already checked items from list
    print("Removing duplicate items...")
    for link in matter_links[:]:
        if link in checked_urls:
            matter_links.remove(link)
    #create threads and split into sublists
    print("Initiating threads...")
    
    WORKERS = 100
    filename_list = []
    
    with ThreadPoolExecutor(max_workers = WORKERS) as exe:
        iter = exe.map(thread_task, matter_links)
    print("Threads complete.")
    filename_list = list(iter)
    

    #write out filename list to folder
    print("Writing filenames...")
    with open(f"{DATA_PATH}{SLASH}filenames.json", "a") as file:
        for filename in filename_list:
            pass
            #TODO: Uncomment following line!
            #file.write(f"{filename}\n")
    #append newly checked urls to folder
    print("Writing URLS...")
    with open(f"{DATA_PATH}{SLASH}checked_urls.json", "a") as file:
        for link in matter_links:
            checked_urls.append(link)
        #TODO: Uncomment following line!
        #json.dump(checked_urls, file)
    
    #return list of filenames
    print("Returning filename list...")
    return filename_list

def thread_task(matter_link: str) -> str:  
    versions = json.loads(_urlopen(f"{matter_link}/Versions"))
    key = versions[0].get("Key")
    
    text = json.loads(_urlopen(f"{matter_link}/Texts/{key}"))
    matter_text_id = text.get("MatterTextId")

    filename = f"{DATA_PATH}{SLASH}matter_text_{matter_text_id}.txt".encode("ascii", "ignore")
    with open(filename, "w") as file:
        if(text["MatterTextPlain"] is not None):
            file.write(text["MatterTextPlain"])
        else:
            file.write("")

    return filename

def _urlopen(url: str) -> any:
    wait_length = 0.5
    while True:
        wait_length = wait_length * 2
        try:
            with urllib.request.urlopen(url, timeout=20) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            #print(f"  [HTTP {exc.code}] {url}")
            time.sleep(wait_length)
        except Exception as exc:
            #print(f"  [ERROR] {url} – {exc}")
            time.sleep(wait_length)