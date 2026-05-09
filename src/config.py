import json
import os

SLASH = ""
if(os.name == "NT"): #windows
    SLASH = "\\"
else:                #posix
    SLASH = "/"

with open(f"src{SLASH}config.json", 'r') as file:
    variables = json.load(file)

BASE_URL = variables.get("base_url")
SOL_START = variables.get("sol_start")
SOL_END = variables.get("sol_end")
FORM_700_NAME = variables.get("form_700_name")
SUMMARY_PATH = f".{SLASH}{variables.get("summary_path")}"
DATA_PATH = f".{SLASH}{variables.get("data_path")}"

