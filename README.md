# Evernote-to-DayOne

A Python Script for migrating notes from Evernote to Day One.

Evernote notes (exported as HTML files) are converted to DayOne notes (as Markdown entries) using Pandoc and Day One's official command line interface. 

Most of the original note data is preserved, including media files, time stamps, and locations.

Written by Chris Arcadia on December 26, 2020.

## Prerequisites

Aside from the Python libraries loaded at the top of the script, the following applications must be installed on your Mac:

* [Evernote](https://evernote.com) App : "Accomplish more with better notes."
* [Day One](https://dayoneapp.com) App : "Your journal for life."
* [Day One Command Line Interface (CLI)](https://help.dayoneapp.com/en/articles/435871-command-line-interface-cli) : get by running the following command in Terminal (after installing Day One) : `sudo bash /Applications/Day\ One.app/Contents/Resources/install_cli.sh`
* [Pandoc](https://pandoc.org/installing.html) Document Converter : get by downloading the latest macOS package on [GitHub](https://github.com/jgm/pandoc/releases/).

## Usage

1. export your notes from Evernote as HTML (not ENEX, see the [official tutorial](https://help.evernote.com/hc/en-us/articles/360053159414))
2. update the script paths with your desired paths (input folder, output folder, and Day One CLI path)
3. configure the script options as needed (set "write" to convert Evernote HTML notes into Markdown, set "command" to import those Markdown notes into the Day One journal specified by "journal")
4. run the script and watch your entries be added to your Day One library.

