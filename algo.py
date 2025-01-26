import random

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

def save_words_to_file(words, file_path='words.txt'):
  """Save a list of words to a file."""
  with open(file_path, 'w') as file:
    for word in words:
      file.write(word + '\n')

def generate_dynamic_topics():
  """Generate a dynamic list of 5 topics."""
  base_topics = ["sports", "animals", "cities", "fruits", "famous songs titles", "movies", "countries", "languages", "plants", "professions"]
  return random.sample(base_topics, 5)

def generate_words_for_topic(topic):
  """Generate a list of 15 random words based on the selected topic."""
  word_bank = {
    "sports": ["soccer", "tennis", "hockey", "rugby", "golf", "swimming", "skiing", "karate", "cycling", "boxing", "running", "surfing", "archery", "baseball", "basketball"],
    "animals": ["elephant", "giraffe", "tiger", "zebra", "dolphin", "penguin", "kangaroo", "panda", "koala", "rhinoceros", "chimpanzee", "octopus", "eagle", "crocodile", "peacock"],
    "cities": ["paris", "london", "tokyo", "berlin", "rome", "dubai", "sydney", "madrid", "moscow", "newyork", "seoul", "cairo", "mumbai", "singapore", "bangkok"],
    "fruits": ["apple", "banana", "orange", "mango", "kiwi", "grape", "peach", "plum", "cherry", "apricot", "papaya", "blueberry", "pineapple", "pomegranate", "watermelon"],
    "famous songs titles": ["yesterday", "imagine", "hallelujah", "thriller", "wonderwall", "bohemian", "roxanne", "superstition", "badguy", "shallow", "despacito", "dancingqueen", "purplehaze", "hotelcalifornia", "heyjude"],
    "movies": ["inception", "avatar", "titanic", "matrix", "gladiator", "jaws", "rocky", "alien", "psycho", "joker", "godfather", "frozen", "batman", "avengers", "casablanca"],
    "countries": ["usa", "canada", "france", "germany", "italy", "japan", "brazil", "india", "china", "australia", "mexico", "russia", "spain", "egypt", "argentina"],
    "languages": ["english", "spanish", "french", "german", "italian", "japanese", "chinese", "russian", "portuguese", "korean", "arabic", "swedish", "dutch", "hindi", "greek"],
    "plants": ["rose", "tulip", "orchid", "lily", "sunflower", "bamboo", "cactus", "fern", "ivy", "oak", "maple", "pine", "willow", "dandelion", "moss"],
    "professions": ["doctor", "engineer", "teacher", "artist", "lawyer", "nurse", "pilot", "scientist", "chef", "actor", "writer", "firefighter", "policeman", "architect", "musician"]
  }
  return random.sample(word_bank[topic], 15)

def prompt_user_for_topic(topics):
  """Prompt the user to select a topic."""
  print("Select a topic for the game:")
  for i, topic in enumerate(topics, start=1):
    print(f"{i}. {topic}")

  while True:
    try:
      choice = int(input("Enter the number corresponding to your choice: "))
      if 1 <= choice <= len(topics):
        return topics[choice - 1]
      else:
        print("Invalid choice. Please enter a number between 1 and 5.")
    except ValueError:
      print("Invalid input. Please enter a valid number.")

def main():
  # AI-enhanced part: Generate dynamic topics and prompt user for selection
  topics = generate_dynamic_topics()
  selected_topic = prompt_user_for_topic(topics)
  words = generate_words_for_topic(selected_topic)
  save_words_to_file(words)  # Save the words to 'words.txt'
  print(f"\nWords on the topic '{selected_topic}' have been saved to 'words.txt'!")

  # Load words from the file for the game
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
