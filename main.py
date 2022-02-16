# -*- coding: utf-8 -*-

# if you need more words https://www.sketchengine.eu/german-word-list/#tab-id-6
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


def menu_1():
    return """
    0 - all
    1 - nouns
    2 - adjectives
    3 - adverbs
    4 - verbs

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
            print(f"Correct! {streak} Streak")
        else:
            streak = 0
            wrong_guesses += 1
            print(f"Incorrect... Lost streak of {streak}")

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
            print(f"Correct! {streak} Streak")
        else:
            streak = 0
            wrong_guesses += 1
            print(f"Incorrect... Lost streak of {streak}")

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


if __name__ == '__main__':
    print("Welcome to Spaced Repetition!")

    # := assigns
    while (choice := input(menu())) != "0":
        if choice == "1":
            while (choice_1 := input(menu_1())) not in ["0", "1", "2", "3", "4"]:
                print("Choose between 0 and 5")

            data = getWords({"0": "all",
                             "1": "nouns",
                             "2": "adjectives",
                             "3": "adverbs",
                             "4": "verbs", }[choice_1])
            eternalGuess(data)

        if choice == "2":
            print("Endless Random Play")
        if choice == "3":
            print("Choose Languages")
            changeLang()
        if choice == "4":
            # showScoreboard()
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
