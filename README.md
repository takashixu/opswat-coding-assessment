# OPSWAT Coding Assessment

## Description
This project uses the Metadefender Cloud API v4 to scan a file against metadefender.opswat.com


## Requirements
Python 3.9.7+

## Setup/Installation
Type and run the command ```pip install requests``` in the terminal

## Running the Program
In the terminal, run ```python3 ops.py```\
In the case that ```python3 ops.py``` does not work, try running ```py ops.py``` or ```python ops.py```
### Entering a Command
It will first ask you to enter a command\
Type ```upload_file {file_name}``` where ```{file_name}``` is the name of the file you are scanning\
Example: ```upload_file test.txt```

### Entering your apikey
Next, it will ask you to enter your apikey\
Type in or paste your apikey into the terminal

If you have typed a valid file_name (in the same directory), and a valid apikey, the program will run accordingly.

## Author
Takashi Xu