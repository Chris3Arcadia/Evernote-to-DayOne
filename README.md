# Evernote-to-DayOne

A Python Script for migrating notes from Evernote to Day One.

Evernote notes (exported as HTML files) are converted to DayOne notes (as Markdown entries) using Day One's official command line interface. 

Most of the original note data is preserved, including media files, time stamps, and locations.

Written by Chris Arcadia on December 26, 2020.

## Prerequisites

Aside from the Python libraries loaded at the top of the script, the following applications must be installed on your Mac device:

* macOS (since Day One and its Command Line Interface is only available on mac)
* Evernote
* Day One
* [Pandoc](https://pandoc.org/installing.html)
    * get by downloading the latest macOS pkg on [GitHub](https://github.com/jgm/pandoc/releases/).
* [Day One Command Line Interface (CLI)](https://help.dayoneapp.com/en/articles/435871-command-line-interface-cli):
    * get by running the following in terminal: `sudo bash /Applications/Day\ One.app/Contents/Resources/install_cli.sh`)

## Usage
