# Problem Set 2, hangman.py
# Name: Dmytro Bubela
# Collaborators:-
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
import os
import platform
import re

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def load_file():
    inFile = open(WORDLIST_FILENAME, 'r')
    text = inFile.read()
    return text


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    return all(char in letters_guessed for char in secret_word)


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ''
    for char in secret_word:
        if char in letters_guessed:
            guessed_word += char
        else:
            guessed_word += '_ '
    return guessed_word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = ''
    alphabet = string.ascii_lowercase
    for letter in alphabet:
        if letter not in letters_guessed:
            available_letters += letter
    return available_letters


def print_ascii_hangman(guesses_remaining):
    print(" _________     ")
    print("|         |    ")
    if guesses_remaining < 6:
        print("|         0    ")
        if guesses_remaining == 4:
            print("|         |    ")
            print("|              ")
        elif guesses_remaining == 3:
            print("|        /|    ")
            print("|              ")
        elif guesses_remaining == 2:
            print("|        /|\\   ")
            print("|              ")
        elif guesses_remaining == 1:
            print("|        /|\\   ")
            print("|        /     ")
        elif guesses_remaining < 2:
            print("|        /|\\   ")
            print("|        / \\   ")
        else:
            print("|              \n" * 2, end='')
    else:
        print("|              \n"*3, end='')
    print("|              \n" * 2)


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = set()
    guesses_remaining = 6
    warnings_remaining = 3
    vowels = ['a', 'e', 'i', 'o', 'u']
    # Greeting
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print(f"You have {warnings_remaining} warnings left.")
    print('------------------------------------------------')

    while not is_word_guessed(secret_word, letters_guessed) and guesses_remaining > 0:
        print(f"You have {guesses_remaining} guesses left.")
        print_ascii_hangman(guesses_remaining)
        print("Available letters:", get_available_letters(letters_guessed))
        letter = input("Please guess a letter: ")
        if letter:
            letter = letter[0]
        if letter.isalpha():
            letter.lower()
            if letter in letters_guessed:
                print("Oops! You've already guessed that letter.", end=" ")
                if warnings_remaining > 0:
                    warnings_remaining -= 1
                    print(f"You have {warnings_remaining} warnings left.")
                else:
                    guesses_remaining -= 1
            else:
                letters_guessed.update(letter)
                if letter in secret_word:
                    print("Good guess!")
                else:
                    print("Oops! That letter is not in my word.")
                    if letter in vowels:
                        guesses_remaining -= 2
                    else:
                        guesses_remaining -= 1
        else:
            print("Oops! That is not a valid letter.", end=' ')
            if warnings_remaining > 0:
                warnings_remaining -= 1
                print(f"You have {warnings_remaining} warnings left.")
            else:
                guesses_remaining -= 1

        # is letter in a word
        print("Word:", get_guessed_word(secret_word, letters_guessed))
        print('------------------------------------------------')

    if guesses_remaining < 1:
        print(f"Sorry, you ran out of guesses. The word was '{secret_word}'")
        if platform.system() == 'Linux':
            print('\x1b[0;31;40m\n\n' + '                     YOU DIED\n')
            print_ascii_hangman(0)
            print('\x1b[0m')
        elif platform.system() == 'Windows':
            os.system("color 0c")
            print('\n\n' + '                     YOU DIED\n')
            print_ascii_hangman(0)
            os.system("pause")
            os.system("color 07")
        return
    print("Good guess:", get_guessed_word(secret_word, letters_guessed))
    print('------------------------------------------------')
    print("Your total score for this game is:",
          guesses_remaining*len(list(set(secret_word))))

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
     '''
     my_word: string with _ characters, current guess of secret word
     other_word: string, regular English word
     returns: boolean, True if all the actual letters of my_word match the
         corresponding letters of other_word, or the letter is the special symbol
         _ , and my_word and other_word are of the same length;
         False otherwise:
     '''
     my_word = my_word.replace(" ", "")
     # probably I should have done it better
     if len(my_word) == len(other_word):
         for i in range(len(my_word)):
             if my_word[i] != other_word[i]:
                 if my_word[i] == '_':
                     if other_word[i] in my_word[i+1:]:
                         return False
                 else:
                     return False
         return True
     return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # Let's imagine that we are in hackaton
    wordlist = re.findall(' ' + my_word.replace("_ ", ".")+ ' ', ' ' + load_file() + ' ')
    for word in wordlist:
        print(word.replace(" ", ""),end=' ')
    print()


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 

    Follows the other limitations detailed in the problem write-up.
    '''
    letters_guessed = set()
    guesses_remaining = 6
    warnings_remaining = 3
    vowels = ['a', 'e', 'i', 'o', 'u']
    # Greeting
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print(f"You have {warnings_remaining} warnings left.")
    print('------------------------------------------------')

    while not is_word_guessed(secret_word, letters_guessed) and guesses_remaining > 0:
        print(f"You have {guesses_remaining} guesses left.")
        print_ascii_hangman(guesses_remaining)
        print("Available letters:", get_available_letters(letters_guessed))
        letter = input("Please guess a letter: ")
        if letter:
            letter = letter[0]
        if letter == '*':
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            print('------------------------------------------------')
            continue
        elif letter.isalpha():
            letter.lower()
            if letter in letters_guessed:
                print("Oops! You've already guessed that letter.", end=" ")
                if warnings_remaining > 0:
                    warnings_remaining -= 1
                    print(f"You have {warnings_remaining} warnings left.")
                else:
                    guesses_remaining -= 1
            else:
                letters_guessed.update(letter)
                if letter in secret_word:
                    print("Good guess!")
                else:
                    print("Oops! That letter is not in my word.")
                    if letter in vowels:
                        guesses_remaining -= 2
                    else:
                        guesses_remaining -= 1
        else:
            print("Oops! That is not a valid letter.", end=' ')
            if warnings_remaining > 0:
                warnings_remaining -= 1
                print(f"You have {warnings_remaining} warnings left.")
            else:
                guesses_remaining -= 1

        # is letter in a word
        print("Word:", get_guessed_word(secret_word, letters_guessed))
        print('------------------------------------------------')

    if guesses_remaining < 1:
        print(f"Sorry, you ran out of guesses. The word was '{secret_word}'")
        if platform.system() == 'Linux':
            print('\x1b[0;31;40m\n\n' + '                     YOU DIED\n')
            print_ascii_hangman(0)
            print('\x1b[0m')
        elif platform.system() == 'Windows':
            os.system("color 0c")
            print('\n\n' + '                     YOU DIED\n')
            print_ascii_hangman(0)
            os.system("pause")
            os.system("color 07")
        return
    print("Good guess:", get_guessed_word(secret_word, letters_guessed))
    print('------------------------------------------------')
    print("Your total score for this game is:",
          guesses_remaining*len(list(set(secret_word))))

# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.

if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)

    # hangman(secret_word)


###############
    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
