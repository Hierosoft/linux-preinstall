#!/usr/bin/env python3
from __future__ import print_function
import argparse
import re


class AptAction:
    def __init__(self):
        self.start_date = ""
        self.remove_packages = []
        self.side_effects = []
        self.command_line = ""
        self.purge_used = False
        self.subcommand = None  # New attribute for subcommand

    def add_remove_package(self, package_name):
        self.remove_packages.append(package_name)

    def add_side_effect(self, package_name):
        self.side_effects.append(package_name)

    def set_start_date(self, date):
        self.start_date = date

    def set_command_line(self, command):
        self.command_line = command

    def set_purge_used(self, used):
        self.purge_used = used

    def set_subcommand(self, subcommand):
        self.subcommand = subcommand

    def display(self):
        print("Last remove action found on %s:" % self.start_date)

        print("Packages removed:")
        for package in self.remove_packages:
            print(package)

        print("\nPackages removed as side effects:")
        for package in self.side_effects:
            print(package)

        print("\nPurge was %s in the last remove action." %
              ("used" if self.purge_used else "not used"))

        print("\nRedo command:")
        print(self.command_line)
        print('# Remove packages: "%s"' % self.remove_packages)
        print('# side effects: "%s"' % self.side_effects)
        undo_command = "apt install " + " ".join(self.remove_packages + self.side_effects)
        print("\nUndo command:")
        print(undo_command)


def get_last_remove_actions(count):
    # Read the apt history log
    try:
        with open('/var/log/apt/history.log', 'r') as file:
            history_lines = file.readlines()
    except FileNotFoundError:
        print("No apt history log found.")
        return

    remove_actions = []
    action = None

    # Iterate over each line to find remove actions
    for line in history_lines:
        if line.startswith("Start-Date:"):
            action = AptAction()  # Create a new action instance
            action.set_start_date(line.split(":", 1)[1].strip())

        elif line.startswith("Commandline:") and action is not None:
            action.set_command_line(line.split(":", 1)[1].strip())

        elif "Remove:" in line and action is not None:
            action.set_subcommand("remove")  # Set subcommand to "remove"
            # Split the line by commas first
            packages = line.split(":", 1)[1].split(",")
            for package in packages:
                package_name = package.strip()
                package_name = re.sub(r'\s*\(.*?\)', '', package_name)  # Remove parenthetical parts
                package_name = package_name.split(":")[0].strip()  # Keep only the package name
                action.add_remove_package(package_name)

        elif "End-Date:" in line and action is not None:
            if action.subcommand == "remove":  # Append only if subcommand is "remove"
                remove_actions.append(action)  # Save the current action
            action = None  # Reset for the next action

    # Limit to the requested count
    if count is not None:
        remove_actions = remove_actions[:count]

    for action in remove_actions:
        display_action(action)


def display_action(action):
    action.display()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Show last apt remove actions.")
    parser.add_argument('-n', '--count', type=int,
                        help='Number of remove actions to show (default: no limit)')

    args = parser.parse_args()
    print("Limit: %s\n" % args.count)
    get_last_remove_actions(args.count)
