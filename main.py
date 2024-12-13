import random
from enum import Enum

valid_answers = open("./guesses/valid_answers")
valid_guesses = open("./guesses/valid_guesses")

word_solve = ["-","-","-","-","-"]

wrong_guesses = []

class GuessStates(Enum):
    ERR_IN_INPUT_LENGTH = -1
    ERR_NOT_VALID_GUESS = -2

    INCORRECT = 0
    CORRECT = 1

def getWordle(_lines):
    length = len(_lines)

    random_choice = _lines[random.randint(1,length-1)]
    return random_choice.strip()

def verifyGuessIsValid(_guess, _lines):
    for i in range(len(_lines)):
        if _guess == _lines[i]:
            return True
    return False

def guess(_word, _answer, _lines):
    #checks
    print(_word)
    if len(_word) != 5:
        print("NOT CORRECT LENGTH")
        return GuessStates.ERR_IN_INPUT_LENGTH
    if not verifyGuessIsValid(_word, _lines):
        print("NOT VALID GUESS")
        return GuessStates.ERR_NOT_VALID_GUESS

    has_used_before = False

    for i in range(len(_word)):
        if _word[i] in wrong_guesses:
            print(f"You have already guessed '{_word[i]}' in a previous guess")
            has_used_before = True
    if has_used_before:
        return GuessStates.ERR_NOT_VALID_GUESS


    print("Guess: ", end="")
    for i in range(len(_word)):
        if _word[i] == _answer[i]:
            print(_word[i].upper(), end="")
            word_solve[i] = _answer[i].upper()
        elif _word[i] in _answer:
            print("#", end="")
            if word_solve[i] == "-":
                word_solve[i] = "#"
        else:
            print("-", end="")
            wrong_guesses.append(_word[i])
    print("")

    if _word == _answer:
        return GuessStates.CORRECT
    return GuessStates.INCORRECT

def main_loop(_answer, _guesses_left, _guesses, _answers):
    print(f"You have {_guesses_left} Guesses Left")
    if _guesses_left <= 0:
        print("You have run out of guesses...")
        print(f"The answer is {_answer}")
        exit()

    guess_in = ''.join(input().split(" "))
    print(guess_in)
    result = guess(guess_in, _answer, _guesses)
    print_word()

    match result:
        case GuessStates.ERR_NOT_VALID_GUESS:
            main_loop(_answer, _guesses_left, _guesses, _answers)
        case GuessStates.ERR_IN_INPUT_LENGTH:
            main_loop(_answer, _guesses_left, _guesses, _answers)
        case GuessStates.INCORRECT:
            main_loop(_answer, _guesses_left-1, _guesses, _answers)
        case GuessStates.CORRECT:
            print("You have guessed correctly!")
            print("Do you want to play again? (y/n)")
            play_again = input()
            while play_again.lower() != 'y' and play_again.lower() != 'n':
                print("Not valid. (y/n)")
                play_again = input()

            if play_again == "y":
                main_loop(getWordle(_answers), 6, _guesses, _answers)
            exit()

guesses = valid_guesses.readlines()
answers = valid_answers.readlines()

for index in range(len(guesses)):
    guesses[index] = guesses[index].strip()

answer = getWordle(answers)

def print_word():
    print(f"The word is: ", end='')
    for i in range(len(word_solve)):
        print(word_solve[i],end='')
    print("")

print_word()
main_loop(answer, 5, guesses, answers)

valid_answers.close()
valid_guesses.close()