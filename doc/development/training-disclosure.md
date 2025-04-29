# Training Disclosure for linux-preinstall
This Training Disclosure, which may be more specifically titled above here (and in this disclosure possibly referred to as "this disclosure"), is based on Training Disclosure version 1.0.0 at https://github.com/Hierosoft/training-disclosure by Jake Gustafson. Jake Gustafson is probably *not* an author of the project unless listed as a project author, nor necessarily the disclosure editor(s) of this copy of the disclosure unless this copy is the original which among other places I, Jake Gustafson, state IANAL. The original disclosure is released under the [CC0](https://creativecommons.org/public-domain/cc0/) license, but regarding any text that differs from the original:

This disclosure also functions as a claim of copyright to the scope described in the paragraph below since potentially in some jurisdictions output not of direct human origin, by certain means of generation at least, may not be copyrightable (again, IANAL):

Various author(s) may make claims of authorship to content in the project not mentioned in this disclosure, which this disclosure by way of omission implies unless stated elsewhere is of direct human origin to the best of the disclosure editor(s) ability. Additionally, the project author(s) hereby claim copyright and claim direct human origin to any and all content in the subsections of this disclosure itself, where scope is defined to the best of the ability of the disclosure editor(s), including the subsection names themselves, unless where stated, and unless implied such as by context, being copyrighted or trademarked elsewere, or other means of statement or implication according to law in applicable jurisdiction(s).

Disclosure editor(s): Hierosoft LLC

Project author: Hierosoft LLC

This document is a voluntary of how and where content in or used by this project was produced by LLM(s) or any tools that are "trained" in any way.

The main section of this document lists such tools. For each, the version, install location, and a scope of their training sources in a way that is specific as possible.

Subsections of this document contain prompts used to generate content, in a way that is complete to the best ability of the disclosure editor(s).

tool(s) used:
- GPT-4-Turbo (Version 4o, chatgpt.com)

Scope of use: Only code described in subsections below--typically modified by hand to improve logic, variable naming, integration, etc.


## linuxpreinstall
### moreapt
- 2024-10-06
how can I show the actual packages removed by the last apt command in bash, including ones removed as a side effect, including if purge was used?

ok, go back further and actually find the last time remove was used, instead of requiring purge or requiring the purge/remove to be the least command, so the script is more versatile

Ok, now at the start, set UNDO_COMMAND="apt install" then each time you encounter a package name, get it from the output and append a space and the package name to UNDO_COMMAND. for example, if the first package discovered was listed as 'gimp:amd64
(2.10.36-3ubuntu0.24.04.1)", set THIS_PKG to "gimp" and set UNDO_COMMAND="$UNDO_COMMAND $THIS_PKG" then at the end of the script echo $UNDO_COMMAND

We don't need to append the lines with parenthesis, and we don't need the commas. The UNDO_COMMAND should contain space-separated package names.

no no no you are removing the parenthesis but we need to remove everything between as wel

  - [sic]

the comma after the parenthesis is still in there, remove that too

Show the full remove command as well, so before Undo command also say Redo command

No, I don't want to construct REDO_COMMAND, I want to collect it from the apt history item we found.

This is getting out of hand. Convert it to python, make it a function, and allow an argument via argparse "-n" a.k.a. "--count" with a default of 1 for how many remove commands to show, and call the function for each one found.

for compatibility, add a python shebang and from __future__ import print_function

and use percent formatting instead of f interpolation


woh, youv'e really cripped it during the conversion. Rethink my instructions and think python. It only shows 'Last remove action found on 2024-10-06  21:47:27:
Packages removed:
libamd3

Packages removed as side effects:

Purge was not used in the last remove action.

Redo command:
apt remove libamd3

Undo command:
apt install libamd3" and the outputs I specified that were working are gone in the python version so please try again from scratch in Python taking into account all of the requirements I've specified.


You didn't fix it. You are only showing the first package removed as a byproduct, but instead I want to show all packages removed as a byproduct from the first matching entry. Try to get it right given that clarification.

you are still not correcting the error I've described. Let me help you. The value of actions is something like  ['Remove: libamd3:amd64 (1:7.6.1+dfsg-1build1), gimp-data:amd64 (2.10.36-3ubuntu0.24.04.1), libcamd3:amd64 (1:7.6.1+dfsg-1build1), libgegl-common:amd64 (1:0.4.48-2.4build2), qt5ct:amd64 (1.5-1build11), libcholmod5:amd64 (1:7.6.1+dfsg-1build1), gutenprint-locales:amd64 (5.3.4.20220624T01008808d602-1build4), libtiff-tools:amd64 (4.5.1+git230720-4ubuntu2.2), libumfpack6:amd64 (1:7.6.1+dfsg-1build1), libgraphicsmagick++-q16-12t64:amd64 (1.4+really1.3.42-1.1build3), libgmic1:amd64 (2.9.4-4build11), libgutenprint9:amd64 (5.3.4.20220624T01008808d602-1build4), libgimp2.0t64:amd64 (2.10.36-3ubuntu0.24.04.1), libgutenprintui2-2:amd64 (5.3.4.20220624T01008808d602-1build4), libgegl-0.4-0t64:amd64 (1:0.4.48-2.4build2), libgutenprint-common:amd64 (5.3.4.20220624T01008808d602-1build4), sqlite3:amd64 (3.45.1-1ubuntu2), libccolamd3:amd64 (1:7.6.1+dfsg-1build1)\n', 'End-Date: 2024-10-06  10:37:53\n', '\n', 'Start-Date: 2024-10-06  21:47:27\n', 'Commandline: apt install smplayer\n', 'Requested-By: owner (1000)\n', 'Install: smplayer-themes:amd64 (1:20.11.0-1, automatic), smplayer:amd64 (23.12.0+ds0-1build2), smplayer-l10n:amd64 (23.12.0+ds0-1build2, automatic)\n', 'End-Date: 2024-10-06  21:47:36\n'] and I want to keep all of the package names in there, such as libamd3, gimp, and so on, including each package from each line. However, somehow you've also got extra commands in there that are not remove commands, such as apt install smplayer. Try to parse the input better considering that.

packages = line.split(":")[1].strip().split(",") is not the right way to split "Remove: libamd3:amd64 (1:7.6.1+dfsg-1build1), gimp-data:amd64 (2.10.36-3ubuntu0.24.04.1), libcamd3:amd64 (1:7.6.1+dfsg-1build1), libgegl-common:amd64 (1:0.4.48-2.4build2), qt5ct:amd64 (1.5-1build11), libcholmod5:amd64 (1:7.6.1+dfsg-1build1), gutenprint-locales:amd64 (5.3.4.20220624T01008808d602-1build4), libtiff-tools:amd64 (4.5.1+git230720-4ubuntu2.2), libumfpack6:amd64 (1:7.6.1+dfsg-1build1), libgraphicsmagick++-q16-12t64:amd64 (1.4+really1.3.42-1.1build3), libgmic1:amd64 (2.9.4-4build11), libgutenprint9:amd64 (5.3.4.20220624T01008808d602-1build4), libgimp2.0t64:amd64 (2.10.36-3ubuntu0.24.04.1), libgutenprintui2-2:amd64 (5.3.4.20220624T01008808d602-1build4), libgegl-0.4-0t64:amd64 (1:0.4.48-2.4build2), libgutenprint-common:amd64 (5.3.4.20220624T01008808d602-1build4), sqlite3:amd64 (3.45.1-1ubuntu2), libccolamd3:amd64 (1:7.6.1+dfsg-1build1)". first split it by commas, then strip out the parenthetical parts, then spaces and make a list of packages, then for each package, remove the colon and part after the colon to get the package name which is all that is left.

You keep biting off more than you can chew. Instead of packages = line.split(":")[1].strip().split(",") do packages = line.split(",") then process each one in the way I described.

I said stop doing packages = line.split(":")[1].strip().split(",") and do packages = line.split(",") then process each result individually

I said delete line  packages = line.split(":")[1].strip().split(",") and add packages = line.split(",") in its place, then change code following that to strip the characters inside of the for loop instead

now before the first if statement, make a case that checks for "Commandline:" and put the rest of the line after that in a variable called command_line. Then whenever you process a Remove: line you can use that variable to get the actual redo command.

command_line is not being associated with all of the lines associated with the action. Create an AptAction class to make the code more reliable and clear.

rename current_action to action for brevity. Also, the lines aren't being grouped into the correct action, so create a new "Start-Date:" case and only create an action instance on such a line.

Make a new attribute of AptAction called subcommand that defaults to None. In the "Remove:" case, set subcommand to  "remove". In the End-Date: case, only append to remove actions if the subcommand is "remove".


## morepdf
make a python script that accepts a "path", an "old" string and a "new" string, and replaces the old string with the new string assuming the path is a pdf

For backward compatibility, start with a python shebang and from __future__ import print_function, and use percent substitution instead of string interpolation throughout the code. Save the output file as os.path.splitext(path)[0] + "%s-.pdf" % new. Make replace_text_in_pdf a method of a new MorePDF class which has a "load" function to initialize doc which should become self.doc. Count the number of instances as in each block as block_replaced, then add that to a total "replaced" count, which should be shown in the print statement as "%s replacement(s) complete" instead of "Replacements complete". In save, rename "new" to "suffix" and only add "-%s" % suffix if suffix is not None. Call save like pdf_editor.save(path, suffix=new). use argparse. Instead of old, use args.find, and instead of new use args.replace. For find, allow -f or --find, for replace allow -r or --replace. If find is set and replace is not set, call replace_text_in_pdf(args.find, None). Change replace_text_in_pdf so that if new is None, the block's text is displayed with print but not modified. Display the page number before each matching block's text if new is None.

- 2025-04-29: Grok 3

Make a Python script with pykeepass that asks for a password, then loads plist.kdbx, and iterates all items in the "Bills" directory. Make a dictionary called spans = {"6mo": "bi-annually", "per yr": "annually", "yr": "annually", "year": "year", "mo": "monthly", "month": "monthly", "bi-annually": "bi-annually", "quarterly": "quarterly", "3mo": "quarterly", "3months": "quarterly", "wk": "weekly"}. Set d0 = Decimal(0). Create empty totals = OrderedDictionary([("weekly", d0), ("monthly", d0), ("bi-annually": d0), ("annually", d0), "every 2 years": d0, "every 3 years", "every 4 years", "every 5 years"]). Set well_defined_keys = {"per yr": "annually"} Fill in additional 1-1 mappings into spans as follows: iterate key, _ in totals.items(): spans[key] = key. Display a single row for each entry in the Bills folder of the keypass database file as follows. Set span = None. Set amount = None. Set lines = notes.split("\n"). Convert the last modified date to a datetime object and display and format, then after that on the same line display lines[0] only. Do line_parts = lines[0].split(), then iterate for chunk in line_parts. If not chunk.startswith("$"): continue (short circuit the inner note_parts loop) and if that short circuit does not occur do the following in the chunk scope: set amount_parts = note_part.split("/") do amount_parts[0] = amount_parts[0].lstrip("$"), and set amount = Decimal(amount_parts[0]). If the length of amount_parts is != 2, show logger.warning showing the length and full note_part, and continue (short circuit the chunk loop only). if that short circuit does not occur, do the following in the chunk scope: span = spans.get(amount_parts[1]). if span is None, continue (short circuit the chunk loop). After the chunk loop has ended, do the following in the main entry iteration scope: Iterate for try_key, try_span in well_defined_keys.items(): If lines[0] contains try_key: span = try_key. After that inner loop, do the following in the main entry loop: if span is not None and amount is not None: totals[span] += Decimal(amount) else: show a logger warning saying "span={span}, amount={amount}". After the entry loop is over, iterate for span, amount in totals.items(): print("{span}: {amount}")
