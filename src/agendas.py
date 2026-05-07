from typing import Optional, Any
import json
import urllib.request

from api_calls import _get, _get_all 
from config import SOL_START, SOL_END, DATA_PATH, SLASH

def fetch_events(start: str = SOL_START, end: str = SOL_END) -> list[dict]:
    """
    Return Board of Supervisors meeting events within the requested date window.

    Parameters
    ----------
    start : ISO date string, inclusive (e.g. "2020-01-01")
    end   : ISO date string, inclusive (e.g. "2025-12-31")

    Defaults to the 5-year statute of limitations window (2020–2025).
    """
    print(f"Fetching events from {start} to {end} …")

    odata_filter = (
        f"EventDate ge datetime'{start}T00:00:00'"
        f" and EventDate le datetime'{end}T23:59:59'"
    )
    events = _get_all("events", {"$filter": odata_filter, "$orderby": "EventDate asc"})
    print(f"  Found {len(events)} event(s).")
    return events

def fetch_agenda_items(event_id: int) -> list[dict]:
    items = _get(f"events/{event_id}/eventitems", {"AgendaNote": 1})
    # print(items)
    return items

def fetch_event_item_detail(event_id: int, event_item_id: int) -> list[dict]:
    detail = _get(f"events/{event_id}/eventitems/{event_item_id}")
    return detail

def fetch_event_item_ids() -> None:
    events = fetch_events()
    event_item_ids = {}
    for event in events:
        event_items = fetch_agenda_items(event["EventId"])
        event_item_ids.update({event["EventId"]: []})

        for item in event_items:
            # print(item)
            if item is None:
                continue
            if item["EventItemId"] is not None and item["EventItemPassedFlag"] is not None:
                event_item_ids[event['EventId']].append([item["EventItemId"], item["EventItemMatterId"]])
        
    return {event_id: event_item_id_list for event_id, event_item_id_list in event_item_ids.items() if event_item_id_list != []}

def fetch_event_item_votes(event_item_id: int) -> None:
    event_item_votes = _get(f"eventitems/{event_item_id}/votes")
    return event_item_votes

def fetch_all_votes(event_item_ids) -> None:
    event_item_votes = {}
    for event_id, item_ids in event_item_ids.items():
        for item_id, matter_id in item_ids:
            votes = fetch_event_item_votes(item_id)
            print(votes)
            if votes != []:
                event_item_votes.update({item_id: votes})
    return event_item_votes


def fetch_event_item_summary(event_id: int, event_item_id: int) -> None:
    detail = fetch_event_item_detail(event_id, event_item_id)
    for attachment in detail["EventItemMatterAttachments"]:
        if "summary" in attachment["MatterAttachmentName"].lower():
            req = urllib.request.Request(attachment["MatterAttachmentHyperlink"])
            with urllib.request.urlopen(req) as response:
                summary = response.read()
            # summary = requests.get(attachment["MatterAttachmentHyperlink"])
                pdf = open(f"summaries{SLASH}{event_item_id}_Summary_Report" + ".pdf", 'wb')
                pdf.write(summary)
                pdf.close()
                print(f"Downloading summary report for: {event_id} - {event_item_id}")

def fetch_all_summaries(event_item_ids) -> None:
    for event_id, item_ids in event_item_ids.items():
        for item_id in item_ids:
            fetch_event_item_summary(event_id, item_id)

def save_event_item_votes(event_item_ids) -> None:
    event_item_votes = fetch_all_votes(event_item_ids)
    with open(f"{DATA_PATH}{SLASH}event_item_votes.json", 'w') as file:
        json.dump(event_item_votes, file, indent=4)

def save_event_item_ids() -> None:
    event_item_ids = fetch_event_item_ids()
    with open(f"{DATA_PATH}{SLASH}event_item_ids.json", 'w') as file:
        json.dump(event_item_ids, file, indent=4)

def get_event_item_ids_from_file() -> list[dict]:
    with open(f"{DATA_PATH}{SLASH}event_item_ids.json", 'r') as file:
        return json.load(file)