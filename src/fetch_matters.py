from concurrent.futures import ThreadPoolExecutor
import os
import json
import urllib.request
import urllib.error
import time

from config import DATA_PATH, SLASH

def fetch_list(matter_links: list):
    #open checked from folder
    print("Checking saved URLs...")
    checked_urls = []
    CHECKED_URL_FILE = f"{DATA_PATH}{SLASH}checked_urls.json"
    SAVED_FILENAME_FILE = f"{DATA_PATH}{SLASH}filenames.json"
    try: 
        with open(CHECKED_URL_FILE, "r") as file:
            checked_urls = json.load(file)
    except:
        print("No saved URLs")
    
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
    try:
        with open(SAVED_FILENAME_FILE, "r") as file:
            complete_filenames = json.load(file)
    except:
        complete_filenames = []
    
    complete_filenames.extend(filename_list)
    
    with open(SAVED_FILENAME_FILE, "w") as file:
        json.dump(complete_filenames, file, indent=4)
    
    #append newly checked urls to folder
    print("Writing URLS...")
    try:
        with open(CHECKED_URL_FILE, "r") as file:
            complete_url = json.load(file)
    except:
        complete_url = []
    
    for link in matter_links:
        complete_url.append(link)
    
    with open(CHECKED_URL_FILE, "w") as file:
        json.dump(complete_url, file, indent=4)
    
    #return list of filenames
    print("Returning filename list...")
    return complete_filenames

def thread_task(matter_link: str) -> str:
    #aquire version data
    versions = json.loads(_urlopen(f"{matter_link}/Versions"))
    num_versions = len(versions)
    if(num_versions == 0):
        print(f"versions: {versions}")

    #pick which version and get it, starting with the newest version
    for i in range(num_versions-1,-1,-1):
        key = versions[i].get("Key")
        text = json.loads(_urlopen(f"{matter_link}/Texts/{key}"))

        #use this version if it has text
        if((text.get("MatterTextPlain") is None)):
            print(text)
            continue
    
    matter_id = text.get("MatterTextMatterId")
    filename = f"{DATA_PATH}{SLASH}texts{SLASH}matter_text_{matter_id}.txt"

    #store whichever version we picked
    with open(filename, "w", encoding='utf-8') as file:
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