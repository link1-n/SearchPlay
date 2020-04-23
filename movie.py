from subprocess import call
import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format

cprint(figlet_format('SearchPlay', font='standard'),
       'yellow', 'on_red', attrs=['bold'])
ask = str(input('\n\nEnter 1 if you want to stream.\nEnter 2 if you torrent.\n'))
if ask == '2':
    call(["python", "torrent.py"])
    print('\n\nScript made by u/link1-n and u/sp1nalcord.')
else:
    call(["python", "watch.py"])
    print('\n\nScript made by u/link1-n and u/sp1nalcord.')
