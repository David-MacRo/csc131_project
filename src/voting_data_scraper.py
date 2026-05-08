from persons import save_all_persons_votes, get_persons_from_file, find_all_event_items_voters, find_matter_votes
from agendas import save_event_item_ids, get_event_item_ids_from_file, save_event_item_votes, fetch_matter_text, save_all_matter_texts, list_matter_links
from fetch_matters import fetch_list

def main() -> None:
    # gets all persons who have voted and their votes and saves it to a file
    # can be commented out after it has been ran once for testing
    # save_all_persons_votes()

    # opens the file containing all persons and their votes
    # persons = get_persons_from_file()

    # finds who voted for each event item (isnt used currently)
    # voted_items_ids = find_all_event_items_voters(persons)

    # gets item ids that have been voted on
    # can be commented out after it has been ran once for testing
    # save_event_item_ids()

    # # opens the file containing the item ids that have been voted on
    event_item_ids = get_event_item_ids_from_file()
    matter_links = list_matter_links(event_item_ids)
    fetch_list(matter_links, "Aa")

    # downloads the "Summary Report" for the agendas that have been voted on
    # can be commented out after it has been ran once for testing
    # save_event_item_votes(event_item_ids)
    # save_all_matter_texts(event_item_ids)

    # parses the previous event item voters list to see who voted and how they voted on the matched matter
    # find_matter_votes(voted_items_ids, matches)

if __name__ == "__main__":
    main()
