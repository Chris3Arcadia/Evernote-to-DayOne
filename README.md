# Evernote-to-DayOne

A Python Script for migrating notes from Evernote to Day One.

Evernote notes (exported as HTML files) are converted to DayOne notes (as Markdown entries) using Day One's official command line interface. 

Most of the original note data is preserved, including media files, time stamps, and locations.

Written by Chris Arcadia on December 26, 2020.

## Prerequisites

Aside from the Python libraries loaded at the top of the script, the following applications must be installed on your Mac:

* [Evernote](https://evernote.com)
* [Day One](https://dayoneapp.com)
* [Day One Command Line Interface (CLI)](https://help.dayoneapp.com/en/articles/435871-command-line-interface-cli) : get by running the following command in Terminal (after installing Day One): `sudo bash /Applications/Day\ One.app/Contents/Resources/install_cli.sh`
* [Pandoc](https://pandoc.org/installing.html) : get by downloading the latest macOS package on [GitHub](https://github.com/jgm/pandoc/releases/).

## Usage
