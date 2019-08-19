# Main module.

import sys
from sources import srt_get

try:
    import pysrt
    import subliminal
    import babelfish
except ImportError and ModuleNotFoundError:
    print("SRT modules not found. Launch srt_setup.py to install them.")
    sys.exit()

print("Choose the source of subtitles:",
      "1. File (if you have already downloaded subtitles).",
      "2. Remote provider (if you want this program to download subtitles).",
      "Enter the number:", sep="\n")

subtitles_source = int(input())

if subtitles_source == 1:
    movie_dict = srt_get.get_dict_from_file()
else:
    movie_dict = srt_get.get_dict_from_remote_provider()

print("")
print("Number of unique words:", len(movie_dict))
print("Number of words:", sum(movie_dict.values()))

print("Type YES if you wish to output the words by the frequency:")
output_dict_string = input()
if output_dict_string.lower() == "yes":
    print("How much words do you want to output (enter the number)?")
    number_of_words = int(input())
    for key in sorted(movie_dict.items(), key=lambda x: x[1], reverse=True):
        if number_of_words == 0:
            break
        number_of_words -= 1
        print(" ", key[0], ": ", key[1], sep='')
