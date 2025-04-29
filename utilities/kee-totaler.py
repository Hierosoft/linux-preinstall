from pykeepass import PyKeePass
from getpass import getpass
from decimal import Decimal
from collections import OrderedDict
import logging

# Set up logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Ask for password
password = getpass("Enter password: ")

# Load the database
try:
    kp = PyKeePass('plist.kdbx', password=password)
except Exception as e:
    logger.error(f"Failed to open database: {e}")
    exit(1)

# Find the "Bills" group
bills_group = kp.find_groups(name='Bills', first=True)
if bills_group is None:
    logger.error("Bills group not found")
    exit(1)

# Get all entries in the group
entries = bills_group.entries

# Define spans dictionary
spans = {
    "6mo": "bi-annually",
    "per yr": "annually",
    "yr": "annually",
    "year": "annually",
    "mo": "monthly",
    "month": "monthly",
    "bi-annually": "bi-annually",
    "quarterly": "quarterly",
    "3mo": "quarterly",
    "3months": "quarterly",
    "wk": "weekly"
}

# Set d0
d0 = Decimal(0)

# Create totals OrderedDict
totals = OrderedDict([
    ("weekly", d0),
    ("monthly", d0),
    ("bi-annually", d0),
    ("annually", d0),
    ("every 2 years", d0),
    ("every 3 years", d0),
    ("every 4 years", d0),
    ("every 5 years", d0)
])

# Set well_defined_keys
well_defined_keys = {"per yr": "annually"}

# Update spans with totals keys
for key in totals.keys():
    spans[key] = key

# Iterate through each entry
for entry in entries:
    mtime = entry.mtime
    formatted_mtime = mtime.strftime("%Y-%m-%d %H:%M:%S")
    notes = entry.notes or ""
    lines = notes.split("\n")
    if lines:
        first_line = lines[0]
    else:
        first_line = ""
    print(f"{formatted_mtime} {first_line}")

    span = None
    amount = None
    line_parts = first_line.split()
    for chunk in line_parts:
        if not chunk.startswith("$"):
            continue
        amount_parts = chunk.split("/")
        if len(amount_parts) != 2:
            logger.warning(f"Invalid amount_parts length: {len(amount_parts)} for {chunk} in entry {entry.title}")
            continue
        amount_str = amount_parts[0].lstrip("$")
        try:
            amount = Decimal(amount_str)
        except:
            logger.warning(f"Invalid amount: {amount_str} in entry {entry.title}")
            continue
        span_key = amount_parts[1]
        span = spans.get(span_key)
        if span is None:
            continue
        # Assuming only one valid chunk per entry
        break

    if span is None:
        for try_key, try_span in well_defined_keys.items():
            if try_key in first_line:
                span = try_span
                break

    if span is not None and amount is not None:
        if span in totals:
            totals[span] += amount
        else:
            logger.warning(f"Span {span} not in totals for entry {entry.title}")
    else:
        logger.warning(f"Could not determine span or amount for entry: {entry.title}, first_line: {first_line}")

# Print totals
for span, total in totals.items():
    print(f"{span}: {total}")
