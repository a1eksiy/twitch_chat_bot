from functions import parse_message
import time
from datetime import datetime, timezone

"""
tests = [
    "   123 -  hello",
    "123; hello",
    "    123 hello",
    "dwdwawadwaw, 123"
]

for t in tests:
    print(t)
    dict = parse_message(t)
    if dict:
        print(dict)
    else:
        print("Unable to parse")

"""

now = datetime.now(timezone.utc)
print(now)