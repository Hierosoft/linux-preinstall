#!/usr/bin/env python3

import gi
import argparse
gi.require_version('Gio', '2.0')
from gi.repository import Gio

def search_settings(schema, search_term, prefix=''):
    """
    Searches through GSettings schema for keys containing the search term.

    :param schema: The GSettings schema to search.
    :param search_term: The term to search for in keys.
    :param prefix: The prefix to prepend to the key name.
    """
    # settings = Gio.Settings.new(schema)
    # for key in settings.list_keys():
    for key in schema.list_keys():
        if search_term in key:
            full_key = f"{prefix}.{key}" if prefix else key
            print(full_key)

def main():
    parser = argparse.ArgumentParser(description="Search GSettings for keys containing a specified term.")
    parser.add_argument('search_term', type=str, help="The term to search for in GSettings keys.")
    args = parser.parse_args()

    search_term = args.search_term

    # Initialize the GSettings Schema Source
    schema_source = Gio.SettingsSchemaSource.get_default()

    if not schema_source:
        print("Failed to get the default GSettings schema source.")
        return

    # Get all schema IDs (non-recursive)
    schemas = schema_source.list_schemas(False)

    for schema_branches in schemas:
        for schema_branch in schema_branches:
            schema = schema_source.lookup(schema_branch, True)
            if not schema:
                continue
            keys = schema.list_keys()
            if not keys:
                continue
            for key in keys:
                if search_term in key:
                    full_key = f"{schema_branch}.{key}"
                    print(full_key)

if __name__ == '__main__':
    main()
