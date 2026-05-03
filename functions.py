import re

def parse_message(raw_message : str):
    
    match = re.match(r"^\s*(\d+)\s*[,;\-\s]\s*(.+)$", raw_message)
    print(match)

    if not match:
        return None, None
    
    number = int(match.group(1))
    parsed_message = match.group(2)

    return number, parsed_message



