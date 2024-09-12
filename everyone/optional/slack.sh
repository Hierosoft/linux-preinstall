#!/bin/bash
echo "Slack 4.39.95 from the latest/stable channel works fine on Linux Mint 22 (based on Ubuntu 24.04, based on Debian trixie/sid) and is the same version as the one on the website as of that version."
snap_code=
slack_code=1
if [ ! -f "`command -v snap`" ]; then
    snap_code=1
    echo "snap command was not found. If the snapd package is installed, restart your terminal."
    blocked_path=/etc/apt/preferences.d/nosnap.pref
    unblocked_dir=/etc/apt/preferences.disabled/nosnap.pref
    unblocked_path=$unblocked_dir/nosnap.pref
    echo "* Recommendation: install snapd then run sudo snap install slack."
    if [ -f "$blocked_path" ]; then
        echo "  * You will have to remove $block path to do that on your distro, such as via:"
        echo "    sudo mkdir -p $unblocked_dir && sudo mv $blocked_path $unblocked_path"
    fi
else
    echo "Slack version:"
    snap info slack | grep 'installed:' | awk '{print $2}'
    snap_code=$?
    if [ $snap_code -ne 0 ]; then
        echo "* Slack does not appear to be installed by snap."
        echo "Recommendation: install it from snap."
    else
        slack_code=0
        echo "Your installed Slack is from channel:"
        snap info slack | grep 'tracking' | awk '{print $2}'
    fi
fi
if [ ! -f "`command -v slack`" ]; then
    if [ -f /snap/bin/slack ]; then
        echo "snap isn't in the path but /snap/bin/slack exists. Try restarting your terminal."
        slack_code=0
    elif [ -f /usr/bin/slack ]; then
        echo "snap isn't in the path but /usr/bin/slack exists. Try restarting your terminal."
        slack_code=0
    else
        echo "snap isn't installed (not in path. Also tried /snap/bin/slack, /usr/bin/slack"
#         if [ $snap_code -ne 0 ]; then
#             echo "Snap didn't find it either, so exiting."
#             exit 1
#         fi
        slack_code=1
    fi
fi
echo "If slack does not open, the only known way to get Slack to start is to restart the computer. Terminating Slack processes has no effect on the problem (tested on Linux Mint 22 on September 12, 2024)."
exit $slack_code
cat > /dev/null <<END
# Get all the PIDs and their commands of Slack processes, excluding this script
processes=$(ps -eo pid,cmd | grep slack | grep -v grep | grep -v "slack.sh")

if [ -z "$processes" ]; then
  echo "No Slack processes found."
  exit 0
fi

# Debugging: Print the value of $processes and the number of lines it contains
echo "Found Slack processes:"
echo "$processes"
echo "Process count: $(echo "$processes" | wc -l)"

echo "Terminating Slack processes..."

# Loop through the processes and kill them with SIGKILL
while IFS= read -r process; do
  # Ensure the line isn't empty before proceeding
  if [ -n "$process" ]; then
    pid=$(echo "$process" | awk '{print $1}')
    command=$(echo "$process" | cut -d' ' -f2-)

    echo "* Terminating process with PID: $pid, Command: $command... "
    printf "  "  # try to put space before the error if any
    # >&2 printf "  "  # try to put space before the error if any
    kill -9 "$pid"

    if [ $? -eq 0 ]; then
      echo "  OK"
    # else an error should already have been shown.
    fi
  fi
done <<< "$processes"

echo "All Slack processes terminated."
exit 0
END
