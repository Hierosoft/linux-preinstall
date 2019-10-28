#!/usr/bin/env python

# Run this file on the CLIENT! It will use scp.

import os
import sys
import subprocess
import platform
import json

print("============================= SCAN REMOTE ======================================")


if platform.system() == "Windows":
    print("Windows is not implemented")
    exit(1)

cwd = os.getcwd()
hostname = os.environ["HOSTNAME"]
client_remote_path = "{}:{}".format(hostname, cwd)
configs_path = os.path.join(os.environ["HOME"], ".config")
config_path = os.path.join(configs_path, "scanremote")
temps_path = os.path.join("/tmp", "scanremote")
settings_path = os.path.join(config_path, "settings.json")


def usage():
    print("")
    print("USAGE:")
    print("  {} <filename> [<remote_host>] [--<option>]".format(sys.argv[0]))
    print("where [<remote_host>] is the server that has the scanner.")
    print("(You don't have to specify [] options, but remote_host is\n"
          " only optional if you specified it before--or if it\n"
          " is in {} for some other reason.)".format(settings_path))
    print("")
    print("--<option>      changes ANY option in {}".format(settings_path))
    print("                Therefore, remote_host is the same as having filename\n"
          "                followed by another unnamed parameter.")
    print("--scanner_name  specifies the remote scanner name\n"
          "                (otherwise, the first scanner available from \n"
          "                \"ssh <remote_host> 'scanimage -L'\" will be used.")
    print("--rotate        specifies rotation: 90, 180, or 270")
    print("                (only works if remote CLIENT has jpegtran \n"
          "                such as from the libjpeg-turbo-utils package)")
    print("")
    print("Each option must be followed by a space then a value.")
    print("")
    print("")

if len(sys.argv) < 2:
    usage()
    print("")
    print("ERROR: You must specify a filename.")
    print("")
    exit(1)

if not os.path.isdir(config_path):
    os.makedirs(config_path)

if not os.path.isdir(temps_path):
    os.makedirs(temps_path)

rotate = 0

config = {}
good_settings = ["rotate", "scanner_name", "remote_host", "remote_user"]
not_saved_settings = ["rotate", "scanned_name"]

if os.path.isfile(settings_path):
    json_str = ""
    with open(settings_path) as f:
        print("* using settings from '{}'".format(settings_path))
        lines = f.readlines()  # includes newlines!
        for line_original in lines:
            line = line_original.rstrip()
            json_str += line
    config = json.loads(json_str)

for n,v in config.items():
    print("* using {} for *default* {}".format(n, v))

# if len(sys.argv) >= 3:
    # if sys.argv[2][0:2] != "--":
        # config["remote_host"] = sys.argv[2]
o_name = None
unnamed_count = 0
for i in range(1, len(sys.argv)):
    o = sys.argv[i]
    if o_name is not None:
        config[o_name] = o
        print("* You specified {} for {}.".format(o_name, o))
        o_name = None
    elif o[0:2] == "--":
        n = o[2:]
        if n in good_settings:
            o_name = n
        else:
            usage()
            print("ERROR: {} is not a known option.".format(n))
            exit(1)
    else:
        # unnamed params are out name and remote_host
        if unnamed_count == 0:
            print("* You specified {} for scanned_name.".format(o))
            config["scanned_name"] = o
            unnamed_count += 1
        elif unnamed_count == 1:
            print("* You specified {} for remote_host.".format(o))
            config["remote_host"] = o
            unnamed_count += 1
        else:
            print("You can only specify two unnamed params.")
            usage()
            exit(1)

if config.get("remote_host") is None:
    usage()
    print("ERROR: you must specify remote host")
    exit(1)

if config.get("remote_user") is None:
    config["remote_user"] = os.environ["USER"]
    print("* using {} for remote_user")

scanned_path = config["scanned_name"]
out_path = scanned_path
list_scanners_cmd = "scanimage -L"
if config.get("scanner_name") is None:
    print("Listing scanners...")
    remote_cmd_parts = ["'{}'".format(list_scanners_cmd)]
    scanner_list = subprocess.check_output(list_scanners_cmd.split(" "))
    scanner_lines = scanner_list.split("\n")
    count = 0
    for scanner_line in scanner_lines:
        line = scanner_line.strip()
        parts1 = line.split("`")
        if len(parts1) < 2:
            print("* ('{}' was not understood.)")
            continue
        parts2 = parts1[1].split("'")
        if len(parts2) < 2:
            print("* ('{}' was not understood.)")
            continue
        if config.get("scanner_name") is None:
            config["scanner_name"] = parts2[0]
            print("* using {} for scanner.".format(config["scanner_name"]))
        else:
            print("* additional scanner (ignored unless specified with --scanner_name ): {}".format(parts2[0]))

if config.get("scanner_name") is None:
    print("ERROR: A scanner name could not be obtained by running '{}'"
          " on '{}'".format(list_scanners_cmd,
                            config.get("remote_host")))
    exit(1)

remote_scanned_path = os.path.join("/tmp", config["scanned_name"])
try:
    remote_rm = "rm {}".format(remote_scanned_path)
    rm_output_bytes = subprocess.check_output(['ssh', "{}@{}".format(config["remote_user"], config["remote_host"]), "'{}'".format(remote_rm)])
    rm_output = output_bytes.decode('utf-8').strip()
    # print(rm_output)
    print("* removed temp file (unexpected)")
except subprocess.CalledProcessError as e:
    print("* There is probably no temp file (as expected): " + str(e))

def save_config():
    less_config = {}
    for k,v in config.items():
        if k not in not_saved_settings:
            less_config[k] = v
    # for s in not_saved_settings:
        # if s in config:
            # del config[s]

    with open(settings_path, 'w') as outs:
        outs.write(json.dumps(less_config))

save_config()
print("* scanning...")
# remote_scan_cmd = "scanimage -d \"{}\" --format=tiff | convert tiff:- {}.jpg".format(config["scanner_name"], remote_scanned_path)
remote_scan_cmd = "scanimage -d \"{}\" --format=jpeg > {}.jpg".format(config["scanner_name"], remote_scanned_path)
print("  " + remote_scan_cmd)
# such as: scanimage -d "brother4:bus8;dev1" --format=jpeg --source FlatBed
# such as: scanimage -d "brother4:bus8;dev1" --format=tiff | convert tiff:- FlowChart-1a-handmade.jpg
  # Geometry:
    # -l 0..215.9mm (in steps of 0.0999908) [0]
        # Top-left x position of scan area.
    # -t 0..355.6mm (in steps of 0.0999908) [0]
        # Top-left y position of scan area.
    # -x 0..215.9mm (in steps of 0.0999908) [215.88]
        # Width of scan-area.
    # -y 0..355.6mm (in steps of 0.0999908) [355.567]
        # Height of scan-area.
scan_output_bytes = subprocess.check_output(['ssh', '{}@{}'.format(config["remote_user"], config["remote_host"]), "'{}'".format(remote_scan_cmd)])
scan_output = scan_output_bytes.decode('utf-8').strip()
print(scan_output)
print("* transferring file from {} to {}...".format(config["remote_host"], client_remote_path))
remote_transfer_cmd = "rsync -tv {} {}".format(remote_scanned_path, client_remote_path)
print("  " + remote_transfer_cmd)
# such as: rsync -t FlowChart-1a-handmade.jpg   pgs:/home/owner
transfer_output_bytes = subprocess.check_output(['ssh', '{}@{}'.format(config["remote_user"], config["remote_host"]), "'{}'".format(remote_transfer_cmd)])
transfer_output = transfer_output_bytes.decode('utf-8').strip()
print(transfer_output)

if rotate != 0:
    # in_file = os.path.split(scanned_path)[-1]
    out_path = os.path.splitext(scanned_path)[0] + "-rotated.jpg"
    remote_src = None
    output_bytes = subprocess.check_output(['command', '-v', 'jpegtran'])
    output = output_bytes.decode('utf-8').strip()
    if os.path.isfile(output): # /usr/bin/jpegtran
        print("* using '{}'".format(output))
        rotate_cmd = 'jpegtran -rotate {} -outfile {} {}'.format(rotate, out_path, scanned_path)
        rotate_output = subprocess.check_output(rotate_cmd.split(" "))
        # such as: jpegtran -rotate 270 FlowChart-1a-handmade.jpg -outfile MyJpegRotated.jpg
        # or: jpegtran -rotate 270 FlowChart-1a-handmade.jpg > MyJpegRotated.jpg
        print(rotate_output.decode('utf-8'))
        if os.path.isfile(out_path):
            os.remove(scanned_path)
            shutil.move(out_path, scanned_path)
            out_path = scanned_path
        else:
            print(rotate_cmd)
            print("ERROR: rotate command above did not result in '{}'".format(out_path))
            save_config()
            exit(1)
    else:
        print("To use jpegtran for lossless rotation, you must first install libjpeg-turbo-utils.")

save_config()

