# tscripts
Python scripts for LCR lookup, LCR database import, and caller ID name lookup.
The intended use is to call these scripts from Asterisk or a simmilar platform
in your dialplan to look up LCR information and Caller ID names.

## Usage
Read the comments in all of the scripts.

* `lcr_lookup.py` is the LCR lookup script.
* `lcr_import.py` is a script to help you make your LCR databases.
* `cnam_lookup.py` is a very simple script to look up Caller ID name.

## Requirements

* Python 3
* PyYAML - install by `sudo pip install pyyaml`
* requests - install by `sudo pip install requests`
* requests_cache (optional, for caching requests) - `sudo pip install requests_cache`

Keep in mind if you are using a system that defaults to Python 2 rather than 3,
you will need to use `python3` and `pip3`.
