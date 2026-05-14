import json
from concurrent.futures import ThreadPoolExecutor

from api_calls import _get, _get_all 
from config import SOL_START, SOL_END, DATA_PATH, SLASH, SUMMARY_PATH

def fetch_events(start: str = SOL_START, end: str = SOL_END) -> list[dict]:
    """
    Return Board of Supervisors meeting events within the requested date window.

    Parameters
    ----------
    start : ISO date string, inclusive (e.g. "2020-01-01")
    end   : ISO date string, inclusive (e.g. "2025-12-31")

    Defaults to the 5-year statute of limitations window (2020–2025).
    """
    print(f"Fetching events from {start} to {end}...")

    odata_filter = (
        f"EventDate ge datetime'{start}T00:00:00'"
        f" and EventDate le datetime'{end}T23:59:59'"
    )
    events = _get_all("events", {"$filter": odata_filter, "$orderby": "EventDate asc"})
    print(f"    Found {len(events)} event(s).")
    return events

def fetch_agenda_items(event_id: int) -> list[dict]:
    items = _get(f"events/{event_id}/eventitems", {"AgendaNote": 1})
    return items

def fetch_event_item_ids() -> None:
    events = fetch_events()
    def thread_task(event):
        event_items = fetch_agenda_items(event["EventId"])
        result = []
        for item in event_items:
            if item is None:
                continue
            if item["EventItemId"] is not None and item["EventItemPassedFlag"] is not None:
                result.append([item["EventItemId"], item["EventItemMatterId"]])
        return result

    
    WORKERS = 100
    full_list = []
    with ThreadPoolExecutor(max_workers = WORKERS) as exe:
        iter = exe.map(thread_task, events)
    for sub_list in iter:
        full_list.extend(sub_list)

    return full_list
def list_matter_links(event_item_ids):
    matter_links = []
    for item_id, matter_id in event_item_ids:
        if matter_id is None:
            continue
        matter_links.append(f"https://webapi.legistar.com/v1/sonoma-county/matters/{matter_id}")
    # with open(f"{DATA_PATH}{SLASH}matter_links.json", 'w') as file:
    #     json.dump(matter_links, file, indent=4)
    return matter_links

def save_event_item_ids() -> None:
    event_item_ids = fetch_event_item_ids()
    with open(f"{DATA_PATH}{SLASH}event_item_ids.json", 'w') as file:
        json.dump(event_item_ids, file, indent=4)

def get_event_item_ids_from_file() -> list[dict]:
    with open(f"{DATA_PATH}{SLASH}event_item_ids.json", 'r') as file:
        return json.load(file)