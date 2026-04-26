from typing import Optional, Any
import json

from config import DATA_PATH, SLASH
from api_calls import _get, _get_all


def get_persons() -> list[dict]:
    return _get("persons")

def get_person_votes(person_id: int) -> list[dict]:
    return _get(f"persons/{person_id}/votes")

def find_all_event_items_voters(persons_data: list[dict]) -> dict:
    voted_items_ids = {}
    for person in persons_data:
        for vote in person["Votes"]:
            if vote["VoteEventItemId"] not in voted_items_ids:
                voted_items_ids.update({vote["VoteEventItemId"] : [{person["PersonLastName"] : vote["VoteValueName"]}]})
            else:
                voted_items_ids.get(vote["VoteEventItemId"]).append({person["PersonLastName"] : vote["VoteValueName"]})

    return voted_items_ids

def find_matter_votes(voted_item_ids: dict, matches: list) -> None:
    for matter_id in matches:
        print(voted_item_ids.get(matter_id))

def save_all_persons_votes() -> None:
    persons = get_persons()
    for person in persons[:]:
        votes = get_person_votes(person["PersonId"])
        if votes == []:
            persons.remove(person)
            continue
        print(person["PersonFullName"])
        person.update({"Votes": votes})
    with open(f"{DATA_PATH}{SLASH}persons.json", 'w') as file:
        json.dump(persons, file, indent=4)

def get_persons_from_file() -> list[dict]:
    with open(f"{DATA_PATH}{SLASH}persons.json", 'r') as file:
        return json.load(file)