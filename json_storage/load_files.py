import json
import os

with open(os.path.join(os.path.dirname(__file__), "celebrities.json"), "r", encoding='utf-8') as f:
    CELEBRITIES = json.load(f)

with open(os.path.join(os.path.dirname(__file__), "topics.json"), "r", encoding='utf-8') as f:
    TOPICS = json.load(f)