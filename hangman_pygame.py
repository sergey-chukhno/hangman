import pygame
import math
import random
import json
import time

# setup display
pygame.init()
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# load images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# game variables
wrong_guesses = 0
words = ['PYTHON', 'MATCH', 'MAGIC']
word = random.choice(words)
guessed = []

# timer variables
TIME_LIMIT = 120
start_time = time.time()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)

# fonts
LETTER_FONT = pygame.font.SysFont('arial', 35)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('arial', 70)
MENU_FONT = pygame.font.SysFont('comicsans', 25)

# buttons
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# score data
score_file = "score.json"

# Initialize score
try:
    with open(score_file, "r") as file:
        score_data = json.load(file)
except FileNotFoundError:
    score_data = {}

game_id = len(score_data) + 1
wins = sum(1 for result in score_data.values() if result == "win")
losses = sum(1 for result in score_data.values() if result == "loss")


def save_score(outcome):
    global game_id, score_data, wins, losses
    score_data[game_id] = outcome
    with open(score_file, "w") as file:
        json.dump(score_data, file)
    game_id += 1
    if outcome == "win":
        wins += 1
    elif outcome == "loss":
        losses += 1


def draw():
    window.fill(WHITE)

    # draw title
    text = TITLE_FONT.render('HANGMAN', 1, BLACK)
    window.blit(text, (200 - text.get_width() // 2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    window.blit(text, (350, 200))  # ensure word fits on the screen

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            window.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # draw score
    score_text = f"Score: W: {wins} L: {losses}"
    score_display = LETTER_FONT.render(score_text, 1, BLACK)
    window.blit(score_display, (WIDTH - score_display.get_width() - 10, 10))

    # draw hangman image
    window.blit(images[wrong_guesses], (150, 100))

    # draw timer
    elapsed_time = int(time.time() - start_time)
    remaining_time = max(0, TIME_LIMIT - elapsed_time)
    timer_text = f"Time Left: {remaining_time}s"
    timer_display = LETTER_FONT.render(timer_text, 1, BLACK)
    window.blit(timer_display, (500 - timer_display.get_width(), HEIGHT - 50))

    pygame.display.update()


def display_message(message):
    pygame.time.delay(1500)
    window.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def draw_menu(selected_option):
    # Tint the background (transparent overlay)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 255, 255))  # Semi-transparent black tint
    window.blit(overlay, (0, 0))

    # Draw the menu window with rounded corners
    menu_width, menu_height = WIDTH // 1.5, HEIGHT // 4
    menu_x, menu_y = (WIDTH - menu_width) // 2, (HEIGHT - menu_height) // 2
    pygame.draw.rect(window, BLACK, (menu_x, menu_y, menu_width, menu_height), border_radius=15)
    pygame.draw.rect(window, BLACK, (menu_x, menu_y, menu_width, menu_height), 3, border_radius=15)

    # Draw buttons with rounded corners
    options = ["New Game", "Exit"]
    button_width = 150
    button_height = 50
    button_gap = 40
    buttons = []

    start_x = menu_x + (menu_width - (len(options) * (button_width + button_gap) - button_gap)) // 2
    y = menu_y + menu_height // 2 - button_height // 2

    for i, option in enumerate(options):
        x = start_x + i * (button_width + button_gap)
        color = LIGHT_GRAY if i == selected_option else WHITE
        pygame.draw.rect(window, color, (x, y, button_width, button_height), border_radius=10)
        pygame.draw.rect(window, BLACK, (x, y, button_width, button_height), 3, border_radius=10)

        text = MENU_FONT.render(option, 1, BLACK)
        window.blit(text, (x + (button_width - text.get_width()) // 2, y + (button_height - text.get_height()) // 2))
        buttons.append((x, y, button_width, button_height))

    pygame.display.update()
    return buttons


def menu():
    selected_option = 0
    is_menu_open = True
    while is_menu_open:
        buttons = draw_menu(selected_option)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_option = (selected_option - 1) % 2
                if event.key == pygame.K_RIGHT:
                    selected_option = (selected_option + 1) % 2
                if event.key == pygame.K_RETURN:
                    if selected_option == 0:  # New Game
                        return True
                    elif selected_option == 1:  # Exit
                        pygame.quit()
                        quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for i, (x, y, w, h) in enumerate(buttons):
                    if x <= m_x <= x + w and y <= m_y <= y + h:
                        if i == 0:  # New Game
                            return True
                        elif i == 1:  # Exit
                            pygame.quit()
                            quit()


def main():
    global wrong_guesses, guessed, word, start_time, letters

    while True:
        if not menu():
            break  # Exit game if "Exit" is selected

        # Reset game state
        wrong_guesses = 0
        guessed = []
        word = random.choice(words)
        start_time = time.time()

        # Reinitialize the letters
        letters = []
        startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
        starty = 400
        for i in range(26):
            x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
            y = starty + ((i // 13) * (GAP + RADIUS * 2))
            letters.append([x, y, chr(A + i), True])

        # Game loop
        FPS = 60
        clock = pygame.time.Clock()
        is_running = True

        while is_running:
            clock.tick(FPS)

            elapsed_time = int(time.time() - start_time)
            remaining_time = max(0, TIME_LIMIT - elapsed_time)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_x, m_y = pygame.mouse.get_pos()
                    for letter in letters:
                        x, y, ltr, visible = letter
                        if visible:
                            distance = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                            if distance < RADIUS:
                                letter[3] = False
                                guessed.append(ltr)
                                if ltr not in word:
                                    wrong_guesses += 1

                if event.type == pygame.KEYDOWN:
                    key = event.unicode.upper()
                    if key.isalpha() and len(key) == 1:
                        for letter in letters:
                            x, y, ltr, visible = letter
                            if ltr == key and visible:
                                letter[3] = False
                                guessed.append(ltr)
                                if ltr not in word:
                                    wrong_guesses += 1

            draw()

            won = all(letter in guessed for letter in word)
            if won:
                save_score("win")
                display_message("You WON!")
                break

            if wrong_guesses == 6 or remaining_time == 0:
                save_score("loss")
                display_message("You LOST!")
                break

        # After game ends, return to menu
        is_running = False

main()





