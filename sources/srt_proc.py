# Module for processing SRT files.

import string


def get_dict(subtitles):
    res_dict = {}
    for line in subtitles:
        line_words = line.text.split()
        for word in line_words:
            # Remove punctuation from words. Note: "isn't", "won't" and etc.
            # will become "isnt", "wont".
            word = word.translate(str.maketrans('', '', string.punctuation))

            # If all the letters are capital, that's just additional info
            # about what's happening on the screen, not a part of dialog.
            # One exception: word "I".
            if word.isupper() and word != "I":
                continue

            # Empty symbol shouldn't be counted.
            if len(word) == 0:
                continue

            # Make all letters lower-case to ensure that words, which begin
            # the sentence, will be counted properly.
            word = word.lower()

            # Add word to dictionary.
            if word in res_dict:
                res_dict[word] += 1
            else:
                res_dict[word] = 1

    return res_dict
