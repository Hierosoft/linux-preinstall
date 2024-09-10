#!/usr/bin/env python3

import gi
gi.require_version('Gio', '2.0')
from gi.repository import Gio


def main():
    # Get the default schema source
    schema_source = Gio.SettingsSchemaSource.get_default()
    print(f"Default schema source: {schema_source}")

    # List all schemas (recursively) using list_schemas(True)
    schemas = schema_source.list_schemas(True)
    print("Schemas:")

    # Iterate through the list of lists of schemas
    for schema_branches in schemas:
        for schema_branch in schema_branches:
            print(f"- {schema_branch}")

    print("\nDetails for schemas and keys:")

    # Iterate through each schema branch
    for schema_branches in schemas:
        for schema_branch in schema_branches:
            # Retrieve and check the schema
            schema = schema_source.lookup(schema_branch, True)
            if not schema:
                continue

            if not schema.get_path():
                print(f"  Skipping relocatable schema: {schema_branch}")
                continue
            # Create a Gio.Settings object for each schema
            settings = Gio.Settings.new(schema_branch)
            # ^ Can cause crash if relocatable. See:
            #   - <https://stackoverflow.com/questions/78966924/how-do-i-check-if-a-listed-gio-schema-is-good-glib-gio-error-attempting-to-crea>
            #     - same as linux-preinstall/doc/issues-external/2024-09-09_gio_settings_crash.md

            # Retrieve and list all keys for the schema
            keys = schema.list_keys()
            if not keys:
                continue
            for key in keys:
                full_key = f"{schema_branch}.{key}"
                # print(full_key)
                value = settings.get_value(key)
                print(f"  Key: {full_key} = {value}")

if __name__ == '__main__':
    main()
