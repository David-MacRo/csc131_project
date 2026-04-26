from typing import Optional, Any
import fitz
import re
import os

from config import SUMMARY_PATH, SLASH

def search_summaries_for_match(keys: list) -> None:
    matched_matter_ids = []
    files = os.listdir(SUMMARY_PATH)
    for file in files:
        summary = fitz.open(f"{SUMMARY_PATH}{SLASH}{file}")
        for page in summary:
            text = page.get_text().lower()
            filtered_text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
            for key in keys:
                filtered_key = re.sub(r'[^A-Za-z0-9 ]+', '', key)
                result = filtered_text.find(filtered_key.lower())
                if result != -1:
                    print(f"{filtered_key.upper()} FOUND IN {file}")
                    matter_id = int(re.sub(r'_.*', '', file))
                    if matter_id not in matched_matter_ids:
                        matched_matter_ids.append(matter_id)
    return matched_matter_ids