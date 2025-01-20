#from wordlist import words 
import random 


words = ('apple', 'orange', 'banana', 'coconut', 'pineapple')

# dict key: (tuple)
hangman_art = {
  0: ("   ",
      "   ", 
      "   "), 
  1: (" o ",
      "   ", 
      "   "), 
  2: (" o ",
      " | ", 
      "   "), 
  3: (" o ",
      "/| ", 
      "   "), 
  4: (" o ",
      "/|\\", 
      "   "), 
  5: (" o ",
      "/|\\", 
      "/   "), 
  6: (" o ",
      "/|\\", 
      "/ \\")
  }

def display_man(wrong_guesses):
  print('***************')
  for line in hangman_art[wrong_guesses]:
    print(line)
  print('***************')

def display_hint(hint): 
  print(" ".join(hint))

def display_answer(answer):
  print(" ".join(answer))

def load_words(file_path):
  try:
    with open(file_path, 'r') as file:
      return [word.strip() for word in file.readlines()]
  except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit()

def main():
  words = load_words('words.txt')
  answer = random.choice(words)
  hint = ['_'] * len(answer)
  wrong_guesses = 0
  guessed_letters = set()
  is_running = True

  while is_running:
    display_man(wrong_guesses)
    display_hint(hint)
    guess = input("\nEnter a letter: ").lower()

    if len(guess) != 1 or not guess.isalpha(): 
      print('Wrong input. Please provide an alphabet character')
      continue

    if guess in guessed_letters:
      print(f'{guess} has already been guessed')
      continue
    
    guessed_letters.add(guess)

    if guess in answer: 
      for i in range(len(answer)):
        if answer[i] == guess: 
          hint[i] = guess
    else:
      wrong_guesses += 1
    
    if '_' not in hint: 
      display_man(wrong_guesses)
      display_answer(answer)
      print('YOU WON!')
      is_running = False 
    elif wrong_guesses >= len(hangman_art) - 1:
      display_man(wrong_guesses)
      display_answer(answer)
      print('YOU HAVE BEEN HUNG!')
      is_running = False


if __name__ == '__main__': 
  main()