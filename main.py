# -*- coding: utf-8 -*-

# if you need more words https://www.sketchengine.eu/german-word-list/#tab-id-6
from functools import partial
from random import randrange
from translate import Translator

# global
translator = Translator(from_lang="de", to_lang="en")


def getWords(segment):
    if segment == "all":
        with open('words/1000words', encoding="utf-8") as fp:
            return list((x.split()[0], x.split()[1]) for x in fp.readlines())
    else:
        with open('words/german-word-list-' + segment + '.csv', encoding="utf-8") as fp:
            return list((x.split()[0], x.split()[1]) for x in fp.readlines())


def writeFile(words):
    # writes the list back to the file, to maintain the Spaced Repetition Time order!
    with open('words/1000words', 'w', encoding="utf-8") as filehandle:
        filehandle.writelines("%s %s\n" % (word[0], word[1]) for word in words)
    print("File updated")


def shuffleWord(final, words):
    word = words.pop(0)

    if final:
        words.append(word)
    else:
        # spaced repetition
        rand = randrange(15, 50) / 100
        size = words.__sizeof__()
        index = int(size * rand)
        words.insert(index, word)

    return 0


def menu():
    return """    1 - Eternal Guess
    2 - Spaced Repetition
    3 - Choose Languages (default GER -> EN)
    4 - Scoreboard
    0 - Close
    
Choose: """


def menuChooseGame():
    return """
    0 - all
    1 - nouns
    2 - adjectives
    3 - adverbs
    4 - verbs

Choose: """


def menuChooseScoreboard():
    return """
        1 - Longest Streak
        2 - Shortest Streak
        3 - Highest Win/Loss Ratio
        4 - Lowest Win/Loss Ratio
        0 - Back

Choose: """


def retireWord():
    return 0


# guess randomly
def eternalGuess(words):
    # initialize vars
    correct_guesses = 0
    wrong_guesses = 0
    streak = 0
    best_streak = 0

    # start loop
    while 1:
        # random word
        word = words[randrange(0, 1, len(words))]

        user_guess = input("\n" + word[0] + " | ")

        # exit
        if user_guess == "X":
            break

        # non-sensical
        if user_guess == "RETIRE":
            retireWord()
            continue

        result = checkGuess(user_guess, word)

        # update scores
        if result:
            streak += 1
            correct_guesses += 1
            print(f"{streak} Streak")
        else:
            print(f"Lost streak of {streak}")
            streak = 0
            wrong_guesses += 1

        # shuffle back word, based on the result of the guess
        shuffleWord(result, words)

        # if the new streak is better than the best, update it
        if streak > best_streak:
            best_streak = streak

    print(f"\nYou got {correct_guesses} correct guesses and {wrong_guesses} wrong guesses."
          f"\nBest streak: {best_streak}")
    # writes the list back into the file, maintaining the new order
    writeFile(words)


# guess with the spaced repetition learning concept, profile based
def spacedRepetition(words):
    # initialize vars
    correct_guesses = 0
    wrong_guesses = 0
    streak = 0
    best_streak = 0

    # iterate words
    for word in words:

        user_guess = input("\n" + word[0] + " | ")

        # exit
        if user_guess == "X":
            break

        # non-sensical
        if user_guess == "RETIRE":
            retireWord()
            continue

        result = checkGuess(user_guess, word)

        # update scores
        if result:
            streak += 1
            correct_guesses += 1
            print(f"{streak} Streak")
        else:
            print(f"Lost streak of {streak}")
            streak = 0
            wrong_guesses += 1

        # shuffle back word, based on the result of the guess
        shuffleWord(result, words)

        # if the new streak is better than the best, update it
        if streak > best_streak:
            best_streak = streak

    print(f"\nYou got {correct_guesses} correct guesses and {wrong_guesses} wrong guesses."
          f"\nBest streak: {best_streak}")
    # writes the list back into the file, maintaining the new order
    writeFile(words)


def checkGuess(user_guess, word):
    # Show answer
    if user_guess == "?":
        print(f"Answer was {word[1]}")
        return False
    else:
        if user_guess.lower() == word[1].lower():
            print("Correct, " + str(word))
            return True
        else:
            # TODO : translation is taking too long
            # translated = translator.translate(str(word[0]))
            # if user_guess.lower() == translated.lower():
            #       print("Correct, " + translated)
            #       return true
            # else:

            print("Wrong, the answer was " + str(word[1]))
            return False


def changeLang():
    valid_langs = ["en", "de", "pt", "es"]
    print(f"Available Languages:")
    print(*valid_langs)

    while from_lang := input("From? ") not in valid_langs:
        print("Language not available")

    while to_lang := input("To? ") not in valid_langs:
        print("Language not available")

    translator = Translator(from_lang=from_lang, to_lang=to_lang)


def showScoreboard(sort="descending", method="streak"):
    print(sort, method)
    print("*\t*\t*\t*\t*\tScoreboard\t*\t*\t*\t*\t*\n")
    print(f"| {'':>16}Name | Best Streak | Win/Loss |")

    # name, best streak, w/l
    ficticious = {
        0: ["Jon Michel", 15, 66.6],
        1: ["Vincent Aboubakar", 3, 33.3],
        2: ["Moussa Marega", 20, 80.0],
        3: ["Mista", 4, 44.6],
    }

    # TODO : make this a file
    # TODO : sort by biggest score or w/l
    for fake_key in ficticious.keys():
        fake = ficticious[fake_key]
        # im sure theres an easier way to do this...
        print(f"| {fake[0]:>{abs(20)}} | {'':<5}{fake[1]:02}{'':>4} | {'':<2}{fake[2]:.1f}{'':>2} |")

    print("")
    print("\n")


if __name__ == '__main__':
    print("Welcome to Spaced Repetition!")

    # := assigns
    while (choice := input(menu())) != "0":
        if choice == "1":
            while (choice_game := input(menuChooseGame())) not in ["0", "1", "2", "3", "4"]:
                print("Choose between 0 and 5")

            chosen_game = getWords({"0": "all",
                                    "1": "nouns",
                                    "2": "adjectives",
                                    "3": "adverbs",
                                    "4": "verbs", }[choice_game])
            eternalGuess(chosen_game)

        if choice == "2":
            print("Endless Random Play")
        if choice == "3":
            print("Choose Languages")
            changeLang()
        if choice == "4":
            while (choice_scoreboard := input(menuChooseScoreboard())) not in ["0", "1", "2", "3", "4"]:
                print("Choose between 0 and 4")

            if choice_scoreboard == "0":
                continue

            arguments = {"1": ("descending", "streak"),
                         "2": ("ascending", "streak"),
                         "3": ("descending", "wlratio"),
                         "4": ("ascending", "wlratio")}

            # partial object adds arguments when called
            chosen_scoreboard = partial(showScoreboard, arguments[choice_scoreboard])
            chosen_scoreboard()

            # this could simply be
            # showScoreboard(arguments[choice_scoreboard])
            # but it wouldn't be as fun :)
            pass

# TODO : Implement translation
# tr_de_to_en = Translator(from_lang="de", to_lang="en")
# tr_en_to_de = Translator(from_lang="en", to_lang="de")
# translation = tr_de_to_en.translate("das ist ein buch")
# print(translation)
#
# translation = tr_en_to_de.translate("That's a book")
# print(translation)

# TODO :
# scoreboard
# ~random word order
# translation
# words have multiple meanings
# sentences / expressions
