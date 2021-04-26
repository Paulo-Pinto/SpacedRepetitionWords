# if you need more words https://www.sketchengine.eu/german-word-list/#tab-id-6
from random import randrange


def readFile():
    # creates list of words
    with open('words/1000words') as fp:
        return list((x.split()[0], x.split()[1]) for x in fp.readlines())


def writeFile(words):
    # writes the list back to the file, to maintain the Spaced Repetition Time order!
    with open('words/1000words', 'w') as filehandle:
        filehandle.writelines("%s %s\n" % (word[0], word[1]) for word in words)
    print("File updated")


def shuffleWord(final, words):
    word = words.pop(0)

    if final:
        words.append(word)
        print("Correct, " + str(word))
    else:
        rand = randrange(15, 50) / 100
        size = words.__sizeof__()
        index = int(size * rand)
        words.insert(index, word)

        print("Wrong, the answer was " + str(word[1]))

    return 0


def retireWord():
    return 0


if __name__ == '__main__':
    print("Welcome to Spaced Repetition!\nGuess 'X' to leave")

    # stores file content in list
    words = readFile()

    # initialize vars
    correctGuesses = 0
    wrongGuesses = 0
    streak = 0
    bestStreak = 0

    # start loop
    while 1:
        # get first word from list
        word = words[0]

        # get user input
        guess = input("\n" + word[0] + " | ")

        # check guess
        # X -> leave loop
        if guess == "X":
            break
        # ? -> retires word (removed from original file and stored in retired file)
        if guess == "?":
            retireWord()
        else:
            # correct guess
            if guess.lower() == word[1].lower():
                shuffleWord(True, words)
                # increment correct guesses and streak
                correctGuesses = correctGuesses + 1
                streak = streak + 1
                # if the new streak is better than the best, update it
                if streak > bestStreak:
                    bestStreak = streak
                print("Streak: " + str(streak))
            else:
                shuffleWord(False, words)
                # increment wrong guesses and resets streak
                wrongGuesses = wrongGuesses + 1
                streak = 0

    print("\nYou got " + str(correctGuesses) + " correct guesses and " + str(wrongGuesses) + " wrong guesses.\n"
                                                                                             "Best streak: " + str(
        bestStreak))
    # writes the list back into the file, maintaining the new order
    writeFile(words)
