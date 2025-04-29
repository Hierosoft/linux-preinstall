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


def formatted_ex(ex):
    return "{}: {}".format(type(ex), ex)


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
    ("quarterly", d0),
    ("bi-annually", d0),
    ("annually", d0),
    ("every 2 years", d0),
    ("every 3 years", d0),
    ("every 4 years", d0),
    ("every 5 years", d0)
])

well_defined_title_keys = {
    "domain reg": "annually",
}
# Set well_defined_keys
well_defined_keys = {
    "annual": "annually",
    "per yr": "annually",
    "per year": "annually",
    "annually": "annually",
    "every year": "annually",
    "once/year": "annually",
    "every month": "monthly",
    "per month": "monthly",
    "per 6mo": "bi-annually",
    "per 3mo": "quarterly",
}
approximate_title_amounts = {"domain reg": Decimal(20)}

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
    amount_str = None
    for idx, chunk in enumerate(line_parts):
        if (not chunk.startswith("$")) and (not chunk.startswith("~$")):
            continue
        next_word = None
        if idx + 1 < len(line_parts):
            next_word = line_parts[idx+1]
        if next_word and (next_word.lower() in ("bal", "balance")):
            # balance, rather than recurring
            logger.warning(
                "Got \"{chunk} {next_word}\" but"
                " no \"$\" recurring amount before it so skipping!")
            break  # since balance comes after payment amo
        amount_parts = chunk.split("/")
        if len(amount_parts) == 1:
            pass  # Keep going (See below for parsing).
        elif len(amount_parts) != 2:
            # logger.info(f"Invalid amount_parts length: {len(amount_parts)}"
            #             f" for {chunk} in entry {entry.title}")
            continue
        amount_str = amount_parts[0].lstrip("~$")  # TODO: mark ~ as approx
        try:
            amount = Decimal(amount_str)
        except Exception as ex:
            print(f"Decimal conversion failed for {repr(amount_str)}: "
                  + formatted_ex(ex))
            # logger.warning(f"Invalid amount: {amount_str}"
            #                f" in entry {entry.title}")
            break  # must break, or may overwrite with a different $ entry like balance!
        if len(amount_parts) < 2:
            break  # must break, or may overwrite with a different $ entry like balance!
        span_key = amount_parts[1]  # such as "mo" if amount_str were "$5/mo"
        span = spans.get(span_key)  # such as, convert "mo" to "monthly"
        break  # must break, or may overwrite with a different $ entry like balance!
        # if span is None:
        #     continue  # do not break
        # # Assuming only one valid chunk per entry
        # break
    # if amount_str is not None:
    #     if amount is None or span is None:
    #         logger.warning(f"Can't add to total since amount={amount}"
    #                        " (tried {repr(amount_str)}), span={repr(span)}")

    if span is None:
        for try_key, try_span in well_defined_keys.items():
            if try_key.lower() in first_line.lower():
                span = try_span
                break
            else:
                logger.debug(
                    f"[span indicator] {try_key.lower()}"
                    f" not in {repr(first_line)}")

    if span is None:
        for try_key, try_span in well_defined_title_keys.items():
            if try_key.lower() in entry.title.lower():
                span = try_span
                break
            else:
                logger.debug(
                    f"[span indicator] {try_key.lower()}"
                    f" not in {repr(entry.title.lower())}")

    if amount is None:
        for try_key, try_amount in approximate_title_amounts.items():
            if (try_key.lower() in entry.title.lower()):
                amount = try_amount
                logger.warning(
                    f"Approximate: ${try_amount}"
                    f" since no amount but is {repr(try_key)}")
                break
            else:
                logger.debug(
                    f"[approx $ indicator] {try_key.lower()}"
                    f" not in {repr(first_line)}")
    if span is not None and amount is not None:
        if span in totals:
            if (span == "monthly") and amount > Decimal(200):
                logger.warning(f"[UNEXPECTED AMOUNT] ${amount}")
            totals[span] += amount
        else:
            logger.warning(
                f"Span {span} not in totals for entry {repr(entry.title)}")
    else:
        logger.warning(
            f"Can't total (span={repr(span)}, amount={amount}) for entry:"
            f" {repr(entry.title)}, first_line: {repr(first_line)}")

# Print totals
for span, total in totals.items():
    print(f"{span}: {total}")
