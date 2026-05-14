from agendas import save_event_item_ids, get_event_item_ids_from_file, list_matter_links
from fetch_matters import fetch_list
from matcher import match
import os
import webbrowser

def main() -> None:
    # gets item ids that have been voted on
    # can be commented out after it has been ran once for testing
    save_event_item_ids()

    # # opens the file containing the item ids that have been voted on
    event_item_ids = get_event_item_ids_from_file()
    matter_links = list_matter_links(event_item_ids)
    matter_text_list = fetch_list(matter_links)
    match_list = match(matter_text_list)

    print("Opening UI...")
    webbrowser.open("http://localhost:8000/src")
    os.system("python -m http.server")


if __name__ == "__main__":
    main()
