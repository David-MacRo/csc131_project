import json

with open("config.json", 'r') as file:
    variables = json.load(file)

BASE_URL = variables.get("base_url")
SOL_START = variables.get("sol_start")
SOL_END = variables.get("sol_end")
SUMMARY_PATH = variables.get("summary_path")
DATA_PATH = variables.get("data_path")