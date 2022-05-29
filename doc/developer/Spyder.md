# Spyder

`python3 -m pip install --user spyder_kernels==2.3.*`

## ModuleNotFoundError
If a module is installed via `pip`, Spyder may not recognize it. I thought the problem was that I installed the missing module using the "--user" option, but that was a misdiagnosis. The best way to handle the issue is to use the same python executable that was used to install the package. A secondary way (D below) is to add the directory that contains your development module that isn't installed. The reason Spyder forbids adding a directory named site-packages is to prevent version mismatches (According to a Spyder maintainer's answer on <https://stackoverflow.com/questions/63385123/issue-adding-site-packages-directory-to-pythonpath-in-spyder>).

You will have to do one of the following:

A. Create a virtualenv for every application (preferable since that is a reproducible set of requirements for your user).

B. Use your system's Python and install the Spyder debugging packages there.

C. Install the package(s) in the Spyder's environment (such as a ~/.virtualenvs/spyder or wherever you installed spyder).

D. Add the directory containing the Python modules that is not installed yet (useful for development).

If you do A or B:
- Go to "Tools", "Preferences" and set "Python interpreter" to the correct python (A. bin/python in the virtualenv)  B. your system's python such as /usr/bin/python or whichever one you used to install the missing pip or conda package(s))
- Install Spyder's debugging tools as instructed by the error that appears, such as via `python3 -m pip install --user spyder_kernels==2.3.*`, but the following changes to the instructions are necessary:
  - The correct package name is `spyder_kernels` (I changed `spyder-kernels` to `spyder_kernels`).
  - use the specific python you want in order to be sure (I added the `python3 -m` part).
  - remember to add --user if using method B (I added the `--user` part).

If you do A, B, or D, you must also restart Spyder since Spyder can't restart a kernel it didn't start.

### Didn't work

You may be able to adjust Spyder's PYTHONPATH as per
<https://medium.com/analytics-vidhya/python-on-spyder-modulenotfounderror-a-trick-51c058129e17>:

- Click "Tools", "PYTHONPATH manager"
  - Click "Add Path" and choose the path such as
    `~/.local/lib/python3.9` but change `python3.9` to
    your version folder (or
    `%LOCALAPPDATA%\Python\Python38-32\Lib` on Windows,
    but change `Python38-32` to your Python version folder.)
  - Spyder forbids adding "site-packages" which would have the actual
    desired effect, so the settings added above must be edited manually.
    If you are sure you are using the correct Python version, continue
    below (Otherwise, use a virtualenv and change the
    "Python interpreter" in "Tools", "Preferences" to that one).
    - Close Spyder.
    - Open your favorite text editor then open and find the
      spyder_pythonpath line. Add `/site-packages` (or `\site-packages`
      on Windows) to the end of the path you added above.

