# Install macOS

"Install failed with update not found" for:
- `softwareupdate --fetch-full-installer --full-installer-version 10.15.7`
  - Still works: a box appears that says "Are you sure you want to download"
    - Click yes.
    - (may first have had to click "Get" in the store though; I did that as well but it didn't seem to do anything--See <https://support.apple.com/en-us/HT201372> for links to each version.
- `softwareupdate --fetch-full-installer --full-installer-version 10.15.1`

As per [How to create a bootable installer for macOS](https://support.apple.com/en-us/HT201372)
- Format the drive (Catalina says it requires 25.21 G though 14 G or more according to URL) as Mac OS Extended (Applications, Disk Utilities)
  - Case-insensitive according to [Tony T1 Oct 16, 2017](https://discussions.apple.com/thread/8118481?answerId=32403271022#32403271022).
  - GUID is probably best based on information from [The Different Partition Format Types on Mac](https://mac-optimization.bestreviews.net/the-different-partition-format-types-on-mac/#:~:text=As%20part%20of%20the%20Unified,Apple%20Partition%20Map%20(APM).).

When it is finished, click the drive, then click File, Eject.

Boot from the drive:
- Plug it into the computer to erase.
- When you hear the startup sound, immediately hold the "option" key until the startup menu appears.
- Choose "Install macOS Catalina"



# Create a bootable installer for macOS
[from [Create a bootable installer for macOS](https://gist.github.com/windyinsc/7ff5f3b37fe3b388d8f15f4d042f3eae)]

The following instructions were predominantly sourced via this [Apple Support Document](https://support.apple.com/en-qa/HT201372).


With macOS, you can use a USB flash drive or other removable media as a startup disk from which to install macOS. These advanced steps are intended primarly for system administrators and others who are familiar with the command line.

The final executable command(s) are found within ***Section III. Final macOS Executable Commands*** labled as **Full Example or Full Example w/Options**. I personally use the w/Options command which include both the `--nointeraction` and `&&say Installation` commands.

## I. Overview

### Use the createinstallmedia command in Terminal

1. There are two options for downloading the macOS installer
  - **Option 1:** Download the macOS installer from the Mac App Store. Quit the installer if it opens automatically after downloading.  The installer will be in your Applications folder.
  - **Option 2:** Download the macOS installer via terminal... as per this macOS Big Sur example below.

    softwareupdate --fetch-full-installer --full-installer-version 11.0.1

2. Mount your USB flash drive or other volume. You could also use a secondary internal partition.
3. Open the Terminal app, which is in the Utilities folder of your Applications folder.
4. Use the `createinstallmedia` command in Terminal to create the bootable installer. Examples of this command are in the next section. For detailed usage instructions, make sure that the appropriate Install macOS app is in your Applications folder, then enter one of the following paths in Terminal:

Path for El Capitan:

    /Applications/Install OS X El Capitan.app/Contents/Resources/createinstallmedia

Path for Yosemite:

    /Applications/Install OS X Yosemite.app/Contents/Resources/createinstallmedia

Path for Mavericks:

    /Applications/Install OS X Mavericks.app/Contents/Resources/createinstallmedia

Path for Seirra

	/Applications/Install\ macOS\ Sierra.app/Contents/Resources/createinstallmedia

Path for High Seirra

	/Applications/Install\ macOS\ High\ Sierra.app/Contents/Resources/createinstallmedia

Path for Mojave

	/Applications/Install\ macOS\ Mojave.app/Contents/Resources/createinstallmedia

Path for Catalina

	/Applications/Install\ macOS\ Catalina.app/Contents/Resources/createinstallmedia

Path for Big Sur

	/Applications/Install\ macOS\ Big\ Sur.app/Contents/Resources/createinstallmedia

Path for Monterey

	/Applications/Install\ macOS\ Monterey.app/Contents/Resources/createinstallmedia

## II. Examples

### Using basic syntax `volumepath` & `installerpath`

- **Note: `--applicationpath` is deprecated in macOS 10.14 and greater.**

This is the basic syntax of the command. Replace `volumepath` with the path to your USB flash drive or other volume, and replace `installerpath` with the path to the Install OS X/macOS app.

    createinstallmedia --volume volumepath --applicationpath installerpath

The following examples assume that the OS X installer is in your Applications folder and the name of your USB flash drive or other volume is MyVolume:

Example for El Capitan:

    sudo /Applications/Install OS X El Capitan.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume --applicationpath /Applications/Install OS X El Capitan.app

Example for Yosemite:

    sudo /Applications/Install OS X Yosemite.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume --applicationpath /Applications/Install OS X Yosemite.app

Example for Mavericks:

    sudo /Applications/Install OS X Mavericks.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume --applicationpath /Applications/Install OS X Mavericks.app

Example for Sierra:

	sudo /Applications/Install\ macOS\ Sierra.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume --applicationpath /Applications/Install\ macOS\ Sierra.app

Example for High Sierra:

	sudo /Applications/Install\ macOS\ High\ Sierra.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume --applicationpath /Applications/Install\ macOS\ High\ Sierra.app

Example for Mojave:

	sudo /Applications/Install\ macOS\ Mojave.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume

Example for Catalina:

	sudo /Applications/Install\ macOS\ Catalina.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume

Example for Big Sur

	sudo /Applications/Install\ macOS\ Big\ Sur.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume

Example for Monterey

	sudo /Applications/Install\ macOS\ Monterey.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume

## III. Final macOS Executable Commands

### _macOS (12.0.1) Monterey_

Path for macOS Monterey: `/Applications/Install\ macOS\ Monterey.app`

- ***`createinstallmedia`*** | `/Applications/Install\ macOS\ Monterey.app/Contents/Resources/createinstallmedia`
- ***`--volume`*** | `/Volumes/untitled`

Optional:

- `--nointeraction` | Erase the disk pointed to by volume without prompting for confirmation.
- `&&say Installation\ Done` | Upon completion terminal will speak (audio) the word "Done"

Full Example:

	sudo /Applications/Install\ macOS\ Monterey.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume

Full Example w/Options:

	sudo /Applications/Install\ macOS\ Monterey.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --nointeraction &&say Installation\ macOS Monterey Done

Successfull Full Example w/Options Script Output:

```bash
$ sudo /Applications/Install\ macOS\ Monterey.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --nointeraction &&say Installation\ macOS Monterey Done
Password:
Erasing disk: 0%... 10%... 20%... 30%... 100%
Making disk bootable...
Copying to disk: 0%... 10%... 20%... 30%... 40%... 50%... 60%... 70%... 80%... 90%... 100%
Install media now available at "/Volumes/Install macOS Monterey"
```

### _macOS (11.0.1) Big Sur_

Path for macOS Big Sur: `/Applications/Install\ macOS\ Big\ Sur.app`

- ***`createinstallmedia`*** | `/Applications/Install\ macOS\ Big\ Sur.app/Contents/Resources/createinstallmedia`
- ***`--volume`*** | `/Volumes/untitled`

Optional:

- `--nointeraction` | Erase the disk pointed to by volume without prompting for confirmation.
- `&&say Installation\ Done` | Upon completion terminal will speak (audio) the word "Done"

Full Example:

	sudo /Applications/Install\ macOS\ Big\ Sur.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume

Full Example w/Options:

	sudo /Applications/Install\ macOS\ Big\ Sur.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --nointeraction &&say Installation\ macOS Big Sur Done

Successfull Full Example w/Options Script Output:

```bash
$ sudo /Applications/Install\ macOS\ Big\ Sur.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --nointeraction &&say Installation\ macOS Big Sur Done
Password:
Erasing disk: 0%... 10%... 20%... 30%... 100%
Copying to disk: 0%... 10%... 20%... 30%... 40%... 50%... 60%... 70%... 80%... 90%... 100%
Making disk bootable...
Install media now available at "/Volumes/Install macOS Big Sur"
```

### _macOS (10.15) Catalina_

Path for macOS Catalina: `/Applications/Install\ macOS\ Catalina.app`

- ***`createinstallmedia`*** | `/Applications/Install\ macOS\ Catalina.app/Contents/Resources/createinstallmedia`
- ***`--volume`*** | `/Volumes/untitled`

Optional:

- `--nointeraction` | Erase the disk pointed to by volume without prompting for confirmation.
- `&&say Installation\ Done` | Upon completion terminal will speak (audio) the word "Done"

Full Example:

	sudo /Applications/Install\ macOS\ Catalina.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume

Full Example w/Options:

	sudo /Applications/Install\ macOS\ Catalina.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --nointeraction &&say Installation\ macOS Catalina Done

### _macOS (10.14) Mojave_

Path for macOS Mojave: `/Applications/Install\ macOS\ Mojave.app`

- ***`createinstallmedia`*** | `/Applications/Install\ macOS\ Mojave.app/Contents/Resources/createinstallmedia`
- ***`--volume`*** | `/Volumes/untitled`

Optional:

- `--nointeraction` | Erase the disk pointed to by volume without prompting for confirmation.
- `&&say Installation\ Done` | Upon completion terminal will speak (audio) the word "Done"

Full Example:

	sudo /Applications/Install\ macOS\ Mojave.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled

Full Example w/Options:

	sudo /Applications/Install\ macOS\ Mojave.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --nointeraction &&say Installation\ macOS Mojave Done

### _macOS (10.13) High Sierra_

Path for macOS High Sierra: `/Applications/Install\ macOS\ High\ Sierra.app`

- ***`createinstallmedia`*** | `/Applications/Install\ macOS\ High\ Sierra.app/Contents/Resources/createinstallmedia`
- ***`--volume`*** | `/Volumes/untitled`
- ***`--applicationpath`*** |	`/Applications/Install\ macOS\ High\ Sierra.app`

Optional:

- `--nointeraction` | Erase the disk pointed to by volume without prompting for confirmation.
- `&&say Installation\ Done` | Upon completion terminal will speak (audio) the word "Done"

Full Example:

	sudo /Applications/Install\ macOS\ High\ Sierra.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --applicationpath /Applications/Install\ macOS\ High\ Sierra.app

Full Example w/Options:

	sudo /Applications/Install\ macOS\ High\ Sierra.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --applicationpath /Applications/Install\ macOS\ High\ Sierra.app --nointeraction &&say Installation\ macOS High Sierra Done


### _macOS (10.12) Sierra_

Path for macOS Sierra:

- ***`createinstallmedia`*** | `/Applications/Install\ macOS\ Sierra.app/Contents/Resources/createinstallmedia`
- ***`--volume`*** | `/Volumes/Untitled`
- ***`--applicationpath`*** |	`/Applications/Install\ macOS\ Sierra.app`

Optional:

- `--nointeraction` | Erase the disk pointed to by volume without prompting for confirmation.
- `&&say Installation\ Done` | Upon completion terminal will speak (audio) the word "Done"

Full Example:

	sudo /Applications/Install\ macOS\ Sierra.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --applicationpath /Applications/Install\ macOS\ Sierra.app

Full Example w/Options:

	sudo /Applications/Install\ macOS\ Sierra.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --applicationpath /Applications/Install\ macOS\ Sierra.app --nointeraction &&say Installation\ Sierra Done

### _OS X (10.11) El Capitan_

Path for OS X El Capitan:

- ***`createinstallmedia`*** | `/Applications/Install\ OS\ X\ El\ Capitan.app/Contents/Resources/createinstallmedia`
- ***`--volume`*** | `/Volumes/Untitled`
- ***`--applicationpath`*** |	`/Applications/Install\ OS\ X\ El\ Capitan.app`

Full Example:

	sudo /Applications/Install\ OS\ X\ El\ Capitan.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --applicationpath /Applications/Install\ OS\ X\ El\ Capitan.app

Full Example w/Options:

	sudo /Applications/Install\ OS\ X\ El\ Capitan.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --applicationpath /Applications/Install\ OS\ X\ El\ Capitan.app --nointeraction &&say Installation\ El Capitan Done

### _OS X (10.10) Yosemite_

Path for OS X Yosemite:

- ***`createinstallmedia`*** | `/Applications/Install\ OS\ X\ Yosemite.app/Contents/Resources/createinstallmedia`
- ***`--volume`*** | `/Volumes/Untitled`
- ***`--applicationpath`*** |	`/Applications/Install\ OS\ X\ Yosemite.app`

Full Example:

	sudo /Applications/Install\ OS\ X\ Yosemite.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --applicationpath /Applications/Install\ OS\ X\ Yosemite.app

Full Example w/Options:

	sudo /Applications/Install\ OS\ X\ Yosemite.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --applicationpath /Applications/Install\ OS\ X\ Yosemite.app --nointeraction &&say Installation\ Yosemite Done

### _OS X (10.9) Mavericks_

Path for OS X Mavericks:

- ***`createinstallmedia`*** | `/Applications/Install\ OS\ X\ Mavericks.app/Contents/Resources/createinstallmedia`
- ***`--volume`*** | `/Volumes/untitled`
- ***`--applicationpath`*** |	`/Applications/Install\ OS\ X\ Mavericks.app`

Full Example:

	sudo /Applications/Install\ OS\ X\ Mavericks.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --applicationpath /Applications/Install\ OS\ X\ Mavericks.app

Full Example w/Options:

	sudo /Applications/Install\ OS\ X\ Mavericks.app/Contents/Resources/createinstallmedia --volume /Volumes/untitled --applicationpath /Applications/Install\ OS\ X\ Mavericks.app --nointeraction &&say Installation\ Mavericks Done


### V. Alternitive Methods & Help

1. ==**NEW OCTOBER 2021 ADDITION**== | Alt method for downloading macOS 12 full Installer pkg files via the awesome [Mr. Macintosh](https://mrmacintosh.com) website.
  - [macOS 12 Monterey Full Installer Database. Download Directly from Apple! – Mr. Macintosh](https://mrmacintosh.com/macos-12-monterey-full-installer-database-download-directly-from-apple/)

2. Download specific macOS version and create USB installer from the CLI - via GitHub user [andrewodri/README.md](https://gist.github.com/andrewodri/15dc6c9d6c7a14a686ef772516df2293)
  - andrewodri states, "I always seem to forget how to download the macOS version I need by the time I need it again, so here is a quick and nasty guide on how to download a properly signed *.dmg file to build a USB installer."

3. Having trouble with old installers that have expired certificates?
  - Thanks to the always reliable [TidBITS](https://tidbits.com/) website you can address this issue by visiting his Oct 28, 2019 article found below:
     - **[Redownload Archived macOS Installers to Address Expired Certificates - TidBITS](https://tidbits.com/2019/10/28/redownload-archived-macos-installers-to-address-expired-certificates/)**
