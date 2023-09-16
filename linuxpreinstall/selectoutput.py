#!/usr/bin/env python3
'''
selectoutput
------------
Set the preferred audio device as specified in the 1st parameter as a
search term.

Requires:
- pulseaudio-utils (provides the commands: pactl, pacmd)

Examples:
selectoutput analog  # default behavior
selectoutput hdmi
'''
from __future__ import print_function
import sys
import subprocess


def main():
    preferred_string = "analog"
    # ^ built-in analog stereo
    #   such as alsa_output.pci-0000_00_1b.0.analog-stereo
    if len(sys.argv) > 1:
        preferred_string = sys.argv[1]

    # See <https://askubuntu.com/a/14083>:
    cmd_parts = ['pacmd', 'list-sinks']
    # limited_cmd = "pacmd list-sinks | grep 'name: <'"

    # See <https://stackoverflow.com/a/4760517>:
    # result = subprocess.run(cmd_parts, stdout=subprocess.PIPE)
    # s = result.stdout.decode('utf-8')
    # Python 2 compatible:
    p = subprocess.Popen(cmd_parts, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    # ^ pass input as the param with "\n" characters if necessary
    # print("type(out): {}".format(type(out).__name__))
    # ^ bytes
    e = err.decode("utf-8")
    if len(e) > 0:
        print("ERROR: {}".format(e))
    s = out.decode('utf-8')
    indent = ""
    prev_indent = ""
    depth = 0
    indent_stack = []
    sinks = []
    default_sink = None
    is_default = False
    for rawL in s.split("\n"):
        line = rawL.rstrip()
        lineS = line.strip()
        rawIndent = line[:len(line)-len(lineS)]
        indent = rawIndent.replace("\t", "        ")
        # ^ sadly pactl output has a mixture of tabs and spaces :(
        if len(indent) > len(prev_indent):
            depth += 1
            indent_stack.append(indent)
        elif len(indent) < len(prev_indent):
            # depth -= 1
            # Match a previous indent in case went back more than one
            # level.
            if len(indent_stack) > 0:
                while ((len(indent_stack) > 0)
                        and (len(indent) < len(indent_stack[-1]))):
                    depth -= 1
                    indent_stack.pop()
        if (len(indent_stack) == 0) and (len(indent) > 0):
            # Warning: unmatched indent (normal for pactl due to
            # every "index:" being aligned but "* " being to the left of
            # the default one :(
            indent_stack.append(indent)
            depth = 1
        # if True:  # depth == 1:
        #     print("{} {}".format(depth, line))
        # depth 1: index
        # depth 2: "name" of sink, and other properties.
        name = None
        value = None
        signI = lineS.find(":")
        if signI > -1:
            name = lineS[:signI].strip()
            if name.startswith("* "):
                # "*" means default index
                name = name[2:]
                if name == "index":
                    is_default = True
            elif name == "index":
                is_default = False
            value = lineS[signI+1:].strip()
            if value.startswith("<") and value.endswith(">"):
                value = value[1:-1]
            if depth == 2:
                if name == "name":
                    sinks.append(value)
                    if is_default:
                        default_sink = value
        prev_indent = indent
    print("sinks: {}".format(sinks))
    print("default_sink: {}".format(default_sink))
    preferred_sink = None
    for sink in sinks:
        if preferred_string.lower() in sink.lower():
            preferred_sink = sink
    if preferred_sink is not None:
        print("* detected preferred sink: {}".format(preferred_sink))
        set_cmd_parts = ['pacmd', 'set-default-sink']
        set_cmd_parts.append(preferred_sink)
        result = subprocess.run(set_cmd_parts, stdout=subprocess.PIPE)
        data = result.stdout.decode('utf-8')
        print(data)
    else:
        print("* A preferred sink matching \"{}\" was not detected."
              "".format(preferred_string.lower()))
        print("Found ({}):".format(len(sinks)))
        for sink in sinks:
            print("* {}".format(sink))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
