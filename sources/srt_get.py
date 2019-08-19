# Module for getting SRT files.

import sys
import tkinter
from tkinter import filedialog
import pysrt
import subliminal
import babelfish
from sources import srt_proc
from sources import srt_defines


def get_dict_from_file():
    # We need this object to close Tkinter window after choosing a file;
    # It will remain on the screen by default, if not to destroy it
    # manually after choosing a file.
    root_tkinter_window = tkinter.Tk()

    try:
        print("Press Enter to choose a file...")
        input()
        filepath = filedialog.askopenfilename(title="Choose a file", filetypes=(
            ("Subtitles", "*.srt"), ("All files", "*.*")))
        subtitles = pysrt.open(filepath, encoding='utf-8')
    except Exception as exception:
        print("Something went wrong:", exception)
        sys.exit()

    root_tkinter_window.destroy()

    return srt_proc.get_dict(subtitles)


def get_dict_from_remote_provider():
    res_dict = {}

    print("Choose the type of content:",
          "1. Feature film.",
          "2. TV series.",
          "Enter the number:", sep="\n")

    content_type = int(input())

    if content_type == 1:
        print("Enter the number of films:")
        number_of_films = int(input())
        films = []
        print("Enter film titles (you can also specify the release year,",
              "for example, 'Guardians of the galaxy 2014').")
        print("Divide them by new line:")
        for i in range(number_of_films):
            film_title = input()
            films.append(film_title)

        for i in range(number_of_films):
            append_sub_list_to_dict(download_subtitles(films[i]), res_dict)

        return res_dict

    else:
        print("Type YES if you wish to use predefined options (for task 1):")
        builtin_options_string = input()
        if builtin_options_string.lower() == "yes":
            series = srt_defines.predefined_series
            seasons = srt_defines.predefined_seasons
            episodes = srt_defines.predefined_episodes
        else:
            print("Enter the number of TV series:")
            number_of_series = int(input())

            # List of the series names.
            series = []
            print("Enter TV series titles (just titles, without season",
                  "or episode number, for example, 'Game of thrones').")
            print("Divide them by new line:")
            for i in range(number_of_series):
                series_title = input()
                series.append(series_title)

            # List of the pairs (first season and last season), corresponding to
            # the series from the 'series' list.
            seasons = []
            print("Enter the range of seasons inclusive for the series",
                  "(two numbers, divided by new line).")
            for i in range(number_of_series):
                print(series[i], ":", sep='')
                first_season = int(input())
                last_season = int(input())
                seasons.append([first_season, last_season])

            # List of the pairs (first episode and last episode), corresponding
            # to the series and season.
            episodes = []
            print("Enter the range of episodes inclusive for the seasons",
                  "of the series (two numbers, divided by new line).")
            for i in range(number_of_series):
                episodes.append([])
                for j in range(seasons[i][0], seasons[i][1] + 1):
                    print(series[i], ", season ", j, ":", sep='')
                    first_episode = int(input())
                    last_episode = int(input())
                    episodes[i].append([first_episode, last_episode])

        # Iterating through lists and appending strings from different episodes
        # and different seasons to main dictionary (res_dict).
        for i in range(len(series)):
            for j in range(seasons[i][1] - seasons[i][0] + 1):
                for k in range(episodes[i][j][0], episodes[i][j][1] + 1):
                    movie_title = series[i]
                    movie_title += " S" + str(j + seasons[i][0]) + "E" + str(k)
                    append_sub_list_to_dict(download_subtitles(movie_title),
                                            res_dict)

        return res_dict


def download_subtitles(movie_title):
    # Creating subliminal.video object using movie title.
    video = subliminal.Video.fromname(movie_title)

    print("Downloading subtitles for '", movie_title, "'...", sep='')
    # Downloading subtitles for created video object. If several are
    # available, subtitles with higher rating will be chosen. All available
    # providers are used for searching.
    best_subtitles = \
        subliminal.download_best_subtitles({video}, {babelfish.Language('eng')})

    if not best_subtitles[video]:
        print("No subtitles found for '", movie_title, "'...", sep='')
        return []

    # This line can enable saving downloaded files for further use. Default
    # directory is the directory, where running script is located.
    # Note: when the script is running in non-sudo mode on Linux,
    # downloaded files will be saved in user Home directory.

    # subliminal.save_subtitles(video, [best_subtitles[video][0]])

    # Converting list of subtitles to string, so pysrt module can then convert
    # it to its own format.
    subtitles_string = ''
    for item in [best_subtitles[video][0]]:
        subtitles_string += item.text

    # Converting string to list of strings without any SRT-special content
    # (text only) and returning it.
    return pysrt.from_string(subtitles_string)


def append_sub_list_to_dict(list, main_dict):
    # The function is important for optimizing memory usage. We create a new
    # dictionary for every movie right after getting the list of subtitles.
    # After that we "append" this dictionary to main one. So we do not need to
    # store a lot of lists of strings (heavy memory usage), because we convert
    # and append them to main dictionary right away.

    dict_from_list = srt_proc.get_dict(list)
    for word, number in dict_from_list.items():
        if word in main_dict:
            main_dict[word] += number
        else:
            main_dict[word] = number
