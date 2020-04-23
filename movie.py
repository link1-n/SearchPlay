from subprocess import call
import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format

cprint(figlet_format('SearchPlay', font='standard'), 'cyan', attrs=['bold', 'underline', 'dark','concealed'])
def run():
    ask = str(input("\nEnter 'Stream' if you want to stream.\nEnter 'Torrent' if you torrent.\n"))
    if ask == 'Torrent':
        call(["python", "torrent.py"])
        print('\n\nScript made by u/link1-n and u/sp1nalcord.')
    else:
        call(["python", "watch.py"])
        print('\n\nScript made by u/link1-n and u/sp1nalcord.')

    ask_again = str(input('Do you want to run again?'))
    if ask_again=='yes' or 'YES' or 'Yes':
        run()
    else:
        print('')
run()
