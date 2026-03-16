import json

with open("json_storage/celebrities.json", "r", encoding='utf-8') as f:
    CELEBRITIES = json.load(f)