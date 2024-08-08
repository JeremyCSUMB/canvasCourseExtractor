import json
from datetime import datetime

def format_date(date_string):
    if date_string:
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return 'No due date'

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def save_text(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)