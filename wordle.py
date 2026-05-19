# wordle.py — CLI Wordle game
# Author: Priyanshu Pusola

import random
import os
import time
import urllib.request
from dictionary import ScrabbleDict

ANSWERS_URL  = 'https://raw.githubusercontent.com/cfreshman/wordle-nyt-answers-alphabetical/main/answers.txt'
WORDS_URL    = 'https://raw.githubusercontent.com/tabatkins/wordle-list/main/words'
ANSWERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'answers_cache.txt')
WORDS_FILE   = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'words_cache.txt')
CACHE_TTL    = 7 * 24 * 3600  # 7 days in seconds


def _fetch_if_stale(url, cache_path, label):
    '''Downloads url to cache_path if missing or older than CACHE_TTL.'''
    age = time.time() - os.path.getmtime(cache_path) if os.path.exists(cache_path) else float('inf')
    if age > CACHE_TTL:
        print(f'Updating {label}...', end=' ', flush=True)
        try:
            urllib.request.urlretrieve(url, cache_path)
            print('Done.')
        except Exception as e:
            if not os.path.exists(cache_path):
                raise RuntimeError(f'Could not fetch {label} and no cache exists: {e}')
            print(f'Could not reach server, using cached {label}. ({e})')


def ensure_word_lists():
    '''
    Ensures both word list caches are fresh.
    Returns (answers_path, valid_words_path).
    '''
    _fetch_if_stale(ANSWERS_URL, ANSWERS_FILE, 'answer list')
    _fetch_if_stale(WORDS_URL,   WORDS_FILE,   'valid words')
    return ANSWERS_FILE, WORDS_FILE


def check_input(user_input, prev_guess, dictionary):
    '''
    Validates user input against word length, duplicate guesses, and dictionary.
    Returns True if valid, False otherwise.
    '''
    word_limit = dictionary.getWordSize()
    if len(user_input) < word_limit:
        print(user_input.upper(), 'is too short')
        return False
    if len(user_input) > word_limit:
        print(user_input.upper(), 'is too long')
        return False
    if user_input in prev_guess:
        print(user_input.upper(), 'was already entered')
        return False
    if not dictionary.check(user_input):
        print(user_input.upper(), 'is not a recognized word')
        return False
    return True


def evaluate_guess(guess, word):
    '''
    Returns (green, orange, red) sets with correct duplicate-letter handling.

    Two-pass approach:
      Pass 1 — exact matches (green), consuming those target letters.
      Pass 2 — wrong-position matches (orange) from remaining letters.
    '''
    target     = list(word)
    guess_list = list(guess)
    result     = [None] * len(guess)

    # Build display labels for duplicate letters (e.g. 'e', 'e2', 'e3')
    letter_count = {}
    labels = []
    for letter in guess:
        count = letter_count.get(letter, 0) + 1
        letter_count[letter] = count
        labels.append(letter if count == 1 else letter + str(count))

    # Pass 1: exact matches
    for i in range(len(guess)):
        if guess_list[i] == target[i]:
            result[i]     = 'green'
            target[i]     = None
            guess_list[i] = None

    # Pass 2: wrong-position matches
    for i in range(len(guess)):
        if guess_list[i] is None:
            continue
        if guess_list[i] in target:
            result[i] = 'orange'
            target[target.index(guess_list[i])] = None
        else:
            result[i] = 'red'

    green  = {labels[i] for i, r in enumerate(result) if r == 'green'}
    orange = {labels[i] for i, r in enumerate(result) if r == 'orange'}
    red    = {labels[i] for i, r in enumerate(result) if r == 'red'}
    return green, orange, red


def main():
    '''
    Runs the Wordle game.
    - 6 attempts maximum
    - Random word selected from the cached word list
    - Colour-coded feedback: Green (correct), Orange (wrong position), Red (absent)
    '''
    answers_file, words_file = ensure_word_lists()
    dictionary   = ScrabbleDict(5, words_file)   # full list for validation
    answers_dict = ScrabbleDict(5, answers_file)  # common words for target
    word         = random.choice(list(answers_dict.dictionary.keys()))
    attempts   = 1
    prev_guess = []

    print('\nWelcome to Wordle! Guess the 5-letter word in 6 attempts.\n')

    while True:
        guess = input(f'ATTEMPT {attempts}: Enter a 5-letter word: ').lower()

        if not check_input(guess, prev_guess, dictionary):
            continue

        green, orange, red = evaluate_guess(guess, word)
        prev_guess.append(guess)

        if len(green) == 5:
            print(f'\nFound in {attempts} attempt{"s" if attempts != 1 else ""}! The word was {word.upper()} — well done!')
            return

        if attempts == 6:
            print(f'\nOut of attempts. The word was {word.upper()} — better luck next time!')
            return

        print(
            f'{guess.upper()}  '
            f'Green = {{{", ".join(sorted(green))}}}  '
            f'Orange = {{{", ".join(sorted(orange))}}}  '
            f'Red = {{{", ".join(sorted(red))}}}\n'
        )
        attempts += 1


main()
