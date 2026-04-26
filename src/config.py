import json
import os

with open("src/config.json", 'r') as file:
    variables = json.load(file)

SLASH = ""
if(os.name == "NT"): #windows
    SLASH = "\\"
else:                #posix
    SLASH = "/"

BASE_URL = variables.get("base_url")
SOL_START = variables.get("sol_start")
SOL_END = variables.get("sol_end")
SUMMARY_PATH = "." + SLASH + variables.get("summary_path")
DATA_PATH = variables.get("data_path")

