# SRT setup module.
# Two main third-party modules used in the script are:
# - pysrt: https://github.com/byroot/pysrt
#   (for parsing .srt files)
# - subliminal: https://github.com/Diaoul/subliminal
#   (for downloading subtitles from remote services)

import importlib
import site
import subprocess
import sys


def check_srt_modules():
    try:
        import pysrt
        import subliminal
        print("SRT modules found. You can launch main.py to start the program.")
        return
    except ImportError and ModuleNotFoundError:
        print("SRT modules not found. Type YES if you wish to install them:")
        install_modules_string = input()
        if install_modules_string.lower() == "yes":
            install_srt_modules()
        else:
            exit_program()


def install_srt_modules():
    print("Installing SRT modules...")
    try:
        # Running pip with necessary arguments (user mode).
        subprocess.call(
            [sys.executable, "-m", "pip", "install", "pysrt", "--user"])
        subprocess.call(
            [sys.executable, "-m", "pip", "install", "subliminal", "--user"])

        # Reloading list of installed packages.
        importlib.reload(site)

        # Trying to import SRT modules.
        import pysrt
        import subliminal

        # If everything is OK, print corresponding message and exit.
        print("Installation complete. Launch main.py to start the program.")
    except Exception as exception:
        # For example, pip hasn't been found or some module hasn't been
        # installed successfully.
        print("Something went wrong:", exception)
        print("Please, try again")
        exit_program()


def exit_program():
    print("Exiting...")
    sys.exit()


check_srt_modules()
