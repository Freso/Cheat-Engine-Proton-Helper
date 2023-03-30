#!/usr/bin/env python3

# Cheat Engine for Proton Script:
# Based on a script from Luetti from the Cheat Engine forums, modified for Steam Proton games by KingKrouch.
# Ported to Python by Freso.
#
# Requires Cheat Engine to be installed via Wine in it's default install directory.
# Feel free to tweak the stuff in the "Config" section based on the game that you are playing.
# Keep in mind that you need to have fully launched the game in the currently used Proton version once.
# Prior to running it for the first time, you need to run "chmod +x ./CE.py" to mark this shell script as executable.
# Then, when you want to play the game with Cheat Engine, you just run "./CE.py".

from os import environ as env
from pathlib import Path
from subprocess import run
from time import sleep

## Config: ##
##
# Here's where you should enter the Cheat Engine version that is installed.
# For this example, Cheat Engine 7.4, the experimental branch of Proton are being used as examples.
# Another example you can use instead of "Proton - Experimental" for the Proton Version name is "Proton 3.7", however, instead of using "files" for the Proton Subdirectory name, you would use "dist" instead.
CEVersion="7.4"
PROTONVERSIONNAME="Proton - Experimental"
PROTONSUBDIRECTORYNAME="files"

# This is where you should put the Steam library that you are running the game from, as the compatdata directory with the required Proton prefix will be there.
# For the local Steam install folder, this would be "/home/$USER/.steam/steam".
prefixInstall=f"/home/{env['USER']}/.steam/steam"

# These shouldn't change unless you installed Cheat Engine in a Wine prefix somewhere else.
# By default, you will either need WINE installed separately with Cheat Engine installed in it, or you will need to copy the CE program files needed to your Proton Prefix.
steamInstall=f"/home/{env['USER']}/.steam/"
CEPrefix=f"/home/{env['USER']}/.wine"

# Here's some flags you can tweak, although IIRC, ESync and FSync are required for Cheat Engine to function.
env['WINEESYNC']='1'
env['WINEFSYNC']='1'
env['PROTON_FORCE_LARGE_ADDRESS_AWARE']='1'
env['WINE_LARGE_ADDRESS_AWARE']='1'
TIMER_WAITTIME=5


## Script Functionality begins here: ##

STEAMAPPID=str(input('Enter a Steam AppID: '))

# Don't mess with these variables, as they are necessary for this script to function.
TIMES_TRIED=0

# Sets the WinePrefix to the Proton prefix for said game.
env['WINEPREFIX']=f"{prefixInstall}/steamapps/compatdata/{STEAMAPPID}/pfx"

def checkProcess():
    global TIMES_TRIED
    sleep(TIMER_WAITTIME)
    print(f"Searching for Steam AppID {STEAMAPPID}'s window class...")
    xdotool=run(['xdotool', 'search', '--class', f'steam_app_{STEAMAPPID}']) # Checks if the SteamApp is running inside of Proton
    if not xdotool.returncode: # If so, launches Cheat Engine.
        print("Starting Cheat Engine...")
        sleep(10) # Sleeps the rest for ten seconds to let the game have some time to launch.
        # Starts Cheat Engine using the currently used Proton prefix.
        run([f"{steamInstall}/steam/steamapps/common/{PROTONVERSIONNAME}/{PROTONSUBDIRECTORYNAME}/bin/wine", f"{CEPrefix}/drive_c/Program Files/Cheat Engine {CEVersion}/cheatengine-x86_64.exe"])
    else:
        TIMES_TRIED=TIMES_TRIED+1 # Adds a try to the amount of tries that have been done.
        if TIMES_TRIED==1:
            print(f"Tried {TIMES_TRIED} times.")
        else:
            print(f"Tried {TIMES_TRIED} time.")

if Path(env['WINEPREFIX']).is_dir():
    if Path(f"{steamInstall}/steam/steamapps/common/{PROTONVERSIONNAME}/{PROTONSUBDIRECTORYNAME}/").is_dir():
        run(["xdg-open", f"steam://run/{STEAMAPPID}"]) # Tells Steam to launch the game
        checkProcess() # Starts the process checking function.
    else:
        print("ERROR # 2: Incorrect Proton Directory. Did you set your Steam Install folder, Proton Version Name, or Subdirectory name correctly?")
else:
    print("ERROR # 1: Steam Compatdata folder for game being launched doesn't exist. Make sure to run the game in Proton once before running, check if the Proton version is correct, and check if Proton is enabled for the SteamApp in question.")
