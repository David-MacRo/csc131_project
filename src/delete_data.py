import os
import json
from config import DATA_PATH, SLASH

#clears out data from the data folder, for testing
def delete_data():
    CHECKED_URL_FILE = f"{DATA_PATH}{SLASH}checked_urls.json"
    SAVED_FILENAME_FILE = f"{DATA_PATH}{SLASH}filenames.json"
    EVENT_ITEM_ID_FILE = f"{DATA_PATH}{SLASH}event_item_ids.json"
    CONFLICTS_FILE = f"{DATA_PATH}{SLASH}conflicts.json"
    with open(SAVED_FILENAME_FILE, "r") as file:
        try:
            filenames = json.load(file)
        except:
            filenames = []
    for file_path in filenames:
        os.remove(file_path)
    os.remove(CHECKED_URL_FILE)
    os.remove(SAVED_FILENAME_FILE)
    os.remove(EVENT_ITEM_ID_FILE)
    os.remove(CONFLICTS_FILE)

delete_data()