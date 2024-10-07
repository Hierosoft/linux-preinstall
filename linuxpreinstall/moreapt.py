#!/usr/bin/env python3
from __future__ import print_function

import argparse
import re

def get_last_remove_actions(count):
    # Read the apt history log
    try:
        with open('/var/log/apt/history.log', 'r') as file:
            history_lines = file.readlines()
    except FileNotFoundError:
        print("No apt history log found.")
        return

    remove_actions = []
    current_action = []
    command_line = ""

    # Iterate over each line to find remove actions
    for line in history_lines:
        if line.startswith("Commandline:"):
            command_line = line.split(":", 1)[1].strip()  # Capture command line
        elif "Remove:" in line:
            if current_action:  # Save previous action if it exists
                remove_actions.append((current_action, command_line))
                current_action = []
            current_action.append(line)
        elif "End-Date:" in line and current_action:
            current_action.append(line)  # Close the current action
            remove_actions.append((current_action, command_line))
            current_action = []
            command_line = ""  # Reset command line after processing the action
        elif current_action:
            current_action.append(line)  # Keep adding lines to the current action

    # Limit to the requested count
    remove_actions = remove_actions[-count:]

    for action, cmd in remove_actions:
        display_action(action, cmd)

def display_action(action, command_line):
    # Extract action date
    action_date = ''
    for line in action:
        if line.startswith("Start-Date:"):
            action_date = line.split(":", 1)[1].strip()
            break

    print("Last remove action found on %s:" % action_date)

    # Initialize UNDO_COMMAND
    undo_command = "apt install"

    # Collect removed packages
    print("Packages removed:")
    removed_packages = []

    for line in action:
        if "Remove:" in line:
            # Split the line by commas first
            packages = line.split(",")

            for package in packages:
                # Clean package name by stripping whitespace and removing version info
                package_name = package.strip()  # Start with stripped package string
                package_name = re.sub(r'\s*\(.*?\)', '', package_name)  # Remove parenthetical parts
                package_name = package_name.split(":")[0].strip()  # Keep only the package name
                removed_packages.append(package_name)
                undo_command += " %s" % package_name
                print(package_name)

    # Check for side effects
    print("\nPackages removed as side effects:")
    side_effects = []

    # Check term.log for any removed packages logged as a side effect
    try:
        with open('/var/log/apt/term.log', 'r') as file:
            term_lines = file.readlines()
    except FileNotFoundError:
        print("No apt term log found.")
        return

    # Track whether we have found a relevant remove action
    found_remove_action = False

    for line in term_lines:
        if found_remove_action:
            # Collect side effects until we hit a non-matching line
            if re.match(r'^\s+\w+', line):
                side_effect_package = line.strip().split()[0]
                package_name = re.sub(r'\s*\(.*?\)', '', side_effect_package).strip()
                package_name = package_name.split(":")[0].strip()  # Keep only the package name
                side_effects.append(package_name)
            else:
                break
        if "The following packages will be REMOVED:" in line:
            found_remove_action = True

    for package in side_effects:
        undo_command += " %s" % package
        print(package)

    # Check if purge was used
    purge_used = any("purge" in line for line in action)
    if purge_used:
        print("\nPurge was used in the last remove action.")
    else:
        print("\nPurge was not used in the last remove action.")

    # Display redo and undo commands
    print("\nRedo command:")
    # Construct the redo command using the captured command_line variable
    redo_command = command_line
    print(redo_command)

    print("\nUndo command:")
    print(undo_command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Show last apt remove actions.")
    parser.add_argument('-n', '--count', type=int, default=1,
                        help='Number of remove actions to show (default: 1)')

    args = parser.parse_args()

    get_last_remove_actions(args.count)
