import random
import os
import urllib.request
HANGMAN_STAGES = [
    "  _______\n  |     |\n  |\n  |\n  |\n  |\n  ||||||||||",  # 0 Mistakes:
    "  _______\n  |     |\n  |     O\n  |\n  |\n  |\n  ||||||||||",  # 1 Mistake: Head
    "  _______\n  |     |\n  |     O\n  |     |\n  |\n  |\n  ||||||||||",  # 2 Mistakes: Torso
    "  _______\n  |     |\n  |     O\n  |    /|\n  |\n  |\n  ||||||||||",  # 3 Mistakes: Left Arm
    "  _______\n  |     |\n  |     O\n  |    /|\\\n  |\n  |\n  ||||||||||",  # 4 Mistakes: Right Arm
    "  _______\n  |     |\n  |     O\n  |    /|\\\n  |    /\n  |\n  ||||||||||",  # 5 Mistakes: Left Leg
    "  _______\n  |     |\n  |     O\n  |    /|\\\n  |    / \\\n  |\n  ||||||||||"   # 6 Mistakes: Right Leg
]


class ScreenDisplay: 
    def show_words_blanks(self,secret_word,correct_letters): #allows method "show_words_blanks" to perform functions with self, secret_word, correct_letters (self automatically used)
        display = [letter if letter in correct_letters else "_" for letter in secret_word] #display letter (not defined as a real letter yet) if its in correct_letters, otherwise display "_" in the secret_word string
        print("\033[1mWord: \033[0m " + " ".join(display)) #puts an empty line, then prints "Word" + "[characters of the secret_word with space between each, joining the characters]"
        return "_" not in display #checks if no "_"s are being displayed

class MistakeCounter: #creates a classs called MistakeCounter
    def __init__(self): # initializes (not constructs) a new instance of the object "self"
        self.wrong_guesses = 0 #wrong_guesses is an instance variable for the object "self", exclusively belonging to the istance that creates it (see line above). This line sets the counter for wrong_guesses to 0.
        self.max_allowed = 6
    def add_wrong_guess(self):
        self.wrong_guesses +=1
        return self.wrong_guesses >= self.max_allowed #checks if the number of wrong guesses is more than the number allowed.

class GameSystem(ScreenDisplay, MistakeCounter): #extending 2 superclasses - distinctive feature of Python
    def __init__(self): #initializes a new instance of object "self"
        MistakeCounter.__init__(self) #inherits functions performed in MistakeCounter and ScreenDisplay
        url = "https://gist.githubusercontent.com/scholtes/94f3c0303ba6a7768b47583aff36654d/raw/73f890e1680f3fa21577fef3d1f06b8d6c6ae318/wordle-La.txt"
        extract_everything = urllib.request.urlopen(url).read().decode('utf-8')
        word_list = [word.upper() for word in extract_everything.splitlines()]
        self.secret_word = random.choice(word_list)


def play_game():
    game = GameSystem() #game is an instance of GameSystem
    guessed_letters = set() #creates a set to keep track of guesses
    hints_used_counter = 0
    
    alert_message = ""
    wrong_guess_alert = ""


    os.system('cls' if os.name =='nt' else 'clear')

    while True:
        os.system('cls' if os.name =='nt' else 'clear')
        print("\033[1mWelcome to \033[1;31mH\033[38;5;208mA\033[1;33mN\033[1;32mG\033[1;34mM\033[1;35mA\033[1;95mN\033[0m!")
        
        game.show_words_blanks(game.secret_word, guessed_letters) 
           
        if wrong_guess_alert != "":
            print(wrong_guess_alert)
            wrong_guess_alert = ""

        print(HANGMAN_STAGES[game.wrong_guesses])
        
        eliminated = [letter for letter in (guessed_letters) if letter not in game.secret_word]
        print(f"Eliminated letters: {','.join(eliminated)}")
        print(f"Hints used: {hints_used_counter}/3")

        if alert_message != "":
            print(alert_message)
            alert_message = ""    
        guess = input("\033[90mGuess a letter (or type 'HINT' for a hint): \033[0m").upper().strip()  
        if guess == "HINT":
            if hints_used_counter >= 3:
                alert_message = "\033[33mNo hints remaining!\033[0m"
            else:
                unguessed_char = [char for char in game.secret_word if char not in guessed_letters]
                if unguessed_char:
                    hints_used_counter +=1
                    alert_message = f"\033[36mHint: the word contains {random.choice(unguessed_char)}.\033[0m"
            continue

        if len(guess) != 1 or not guess.isalpha():
            alert_message = "Please type a single letter."
            continue
        if guess in guessed_letters:
            alert_message = f"You already guessed '{guess}'!"
            continue

        guessed_letters.add(guess)

        if "_" not in [letter if letter in guessed_letters else "_" for letter in game.secret_word]:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\033[1mWelcome to \033[1;31mH\033[38;5;208mA\033[1;33mN\033[1;32mG\033[1;34mM\033[1;35mA\033[1;95mN\033[0m!\n")
            game.show_words_blanks(game.secret_word, guessed_letters)
            print(HANGMAN_STAGES[game.wrong_guesses])
            print("\nYou won!")
            break
        if guess not in game.secret_word:
            is_game_over = game.add_wrong_guess()
            wrong_guess_alert = f"Wrong! Mistakes: {game.wrong_guesses}/{game.max_allowed}"
            
            if is_game_over: #if wrong guesses >=6
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\033[1mWelcome to \033[1;31mH\033[38;5;208mA\033[1;33mN\033[1;32mG\033[1;34mM\033[1;35mA\033[1;95mN\033[0m!\n")

                print(f"Word: {' '.join(list(game.secret_word))}")
                print(f"Eliminated letters: {', '.join(eliminated)}")
                print(f"Hints used: {hints_used_counter}/3")
                print(f"Wrong! Mistakes: {game.wrong_guesses}/{game.max_allowed}")
                print(HANGMAN_STAGES[game.wrong_guesses]) # Uses safe indexing
                print("\nGame Over! The word was " + str(game.secret_word))
                break
  
while True:
    play_game()
    play_again = input("\nWould you like to play again? (Y/N): ").strip().upper()
    if play_again != 'Y':
        print("Thanks for playing!")
        break
#   _______
#   |   |
#   |   O
#   |  /|\
#   |   /\
#   |
#   |||||||||| 