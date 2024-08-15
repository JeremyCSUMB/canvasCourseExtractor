import json
from datetime import datetime, timedelta

def format_date(date_string):
    if date_string:
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        pacific_offset = timedelta(hours=-7)
        dt_pacific = dt + pacific_offset
        return dt_pacific.strftime('%Y-%m-%d %I:%M:%S %p PT')
    return 'No due date'

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def save_text(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)
