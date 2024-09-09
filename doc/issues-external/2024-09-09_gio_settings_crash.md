# 2024-09-09 Gio settings crash

## Posted to stackoverflow
(2024-09-09 <https://stackoverflow.com/questions/78966924/how-do-i-check-if-a-listed-gio-schema-is-good-glib-gio-error-attempting-to-crea>)

I would like to list the schemas for the purpose of making a setting search tool.

However, some schemas make `Gio.Settings.new` cause a core dump.

This script requires linux and the "python3-gi" package (such as via `sudo apt install python3-gi`; recent pip versions won't let you install via pip it if it is a system managed package, so the distro's package is recommended).

I am using Linux Mint 22 (based on Ubuntu 24.04 Noble Numbat, which is based on Debian trixie/sid), using the Cinnamon desktop environment. In Python, `import gi; gi.__version__` says '3.48.2'.

```python
#!/usr/bin/env python3

import sys

import gi
gi.require_version('Gio', '2.0')
from gi.repository import Gio

def main():
    # Get the default schema source
    schema_dir = Gio.SettingsSchemaSource.get_default()
    print(f"Default schema source: {schema_dir}")

    schemas = schema_dir.list_schemas(False)
    value = None
    for schema_branches in schemas:
        for schema_branch in schema_branches:
            print(f"\nSchema: {schema_branch}")
            schema = schema_dir.lookup(schema_branch, True)
            if not schema:
                continue
            keys = schema.list_keys()
            if not keys:
                continue
            settings = Gio.Settings.new(schema_branch)
            for key in keys:
                value = settings.get_value(key)
                print(f"  Key: {schema_branch}.{key} = {value}")
                # print(f"  Key: {schema_branch}.{key}")
    return 0


if __name__ == '__main__':
    sys.exit(main())

```

Running the program causes:
```
(process:1117725): GLib-GIO-ERROR **: 13:24:27.172: attempting to create schema 'org.gnome.settings-daemon.peripherals.wacom.stylus.deprecated' without a path
Trace/breakpoint trap (core dumped)
```

If I skip the "new" operation when the `schema_name` contains "deprecated", that isn't enough. Various other names also cause the error.


If I list the names and not the values, then I am able to comment out `settings = Gio.Settings.new(schema_branch)` and prevent the crash, but I want to be able to get the values and understand how to avoid the crash. Normally if I want values I wouldn't get them all at once, so this program is designed to reproduce the crash. However, this could happen even with a smaller program that only lists certain settings.

How do I detect which names are invalid and shouldn't be used for Gio.Settings.new?
