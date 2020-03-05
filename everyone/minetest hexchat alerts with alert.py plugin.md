
1. Run the following:
```
addons=~/.config/hexchat/addons
if [ ! -d "$addons" ]; then mkdir -p "$addons"; fi
wget -O $addons/alerts.py https://github.com/dewiniaid/hexchat-scripts/raw/master/alerts/alerts.py
```
2. Type the following into Hexchat (after joining any channel) to make
leave and join silent, but other messages the system beep (or silent
when away, which alerts plugin cannot handle). Basically, just use
alerts to override the default beep with silence using regex.
- NOTE: you must NOT put quotes or anything else around the regular
  expression, even if it has a space at the end (or the plugin will
  count the quotes as part of the regex).
- In hexchat preferences:
  - Check the following boxes for Alerts (if desired):
    - Channel Message
    - Private Message
  - Sounds (if desired)
    - Private Message: set it to a more urgent sound, for example:
      /home/owner/ownCloud/Sound/system/chat-message-received.wav
- NOTE: For regex tests, you can use <https://www.regextester.com/1939>.
- /alerts add not_game_action
- /alerts add minetest_action_joined
- /alerts add minetest_action_left
- See https://stackoverflow.com/questions/164414/how-to-inverse-match-with-regex
- /alerts set not_game_action regex ^((?!(\w joined the game|\w left the game)).)*$
  - This is an inverse match that only occurs when there is text that is outside of the (lookahead) match above.
  - # \w* is word then anything/nothing, so "*** poikilos left the game" is a match.
  - #fails: /alerts set not_game_action regex ^(((\*\*\*) \w* left |^(\*\*\*) \w* joined )).*$
  - #fails: /alerts set not_game_action regex (?! (((\*\*\*) \w* left |^(\*\*\*) \w* joined )))
  - #fails: /alerts set not_game_action regex (?!^((\*\*\*) \w* joined ).*$)
  - #fails: ^((?!(\*\*\* \w joined the game)).)*$
  - #fails: ^((?!(\*\*\* \w joined the game|\*\*\* \w left the game)).)*$
  - #- even though the following works:
  - #  /alerts set not_game_action regex ^((?!(\*\*\* poikilos joined the game|\*\*\* poikilos left the game)).)*$
  - #- and even though the following works:
  - #  /alerts set not_game_action regex ^((?!(\w joined the game|\w left the game)).)*$
  - #  - no match (as expected) `*** poikilos joined the game`
  - #  - no match (as expected) `*** poikilos left the game`
  - #  - match (as expected) `*** poikilos says hello`
- #/alerts set not_game_action color OFF
- /alerts set minetest_action_joined regex ^(\*\*\*) \w* joined
- /alerts set minetest_action_left regex ^(\*\*\*) \w* left
- #/alerts set not_game_action sound 220189__gameaudio__blip-squeak-CC0-soft-poikilos.wav
  - Skip this since doesn't respect "Away" status like the builtin beep
    does.
- /alerts set not_game_action sound OFF
- /alerts set minetest_action_joined sound silence.wav
- /alerts set minetest_action_left sound silence.wav
  - The sound file must be in ~/.config/hexchat/sounds

## Alerts
```
#/alerts colors:
#"Colors 0-15 correspond to the 'mIRC colors' in your Hexchat preferences."
#00 LighterGray
#01 DarkGray
#02 Blue
#03 Green
#04 Red
#05 Brown
#06 Purple
#07 Orange
#08 DarkYellow
#09 LightGreen
#10 Aqua
#11 DarkCyan
#12 SlateBlue
#13 DarkMagenta
#14 Gray
#16 LightGray
#35 white
```

### Additional examples (not recommended)
- /alerts set minetest_action_joined sound OFF
- /alerts set minetest_action_left sound OFF
- /alerts set not_game_action sound OFF
- /alerts set minetest_action_joined color off
- /alerts set minetest_action_left color off
- /alerts set minetest_action_joined linecolor 35,15
- /alerts set minetest_action_left linecolor 35,13
- In hexchat preferences:
  - Turn off alert and message recieved sounds manually.
  - Change "beep" to a silent wav file (or turn off beep in notification
    settings; It will play the system beep when no beep is
    specified and if the beep notification is turned on).


