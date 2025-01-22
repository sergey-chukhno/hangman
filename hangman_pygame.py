import pygame
import math
import random

# setup display
pygame.init()
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman game")

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

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# fonts
LETTER_FONT = pygame.font.SysFont('arial', 35)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('arial', 70)

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

def draw():
    window.fill(WHITE)

    # draw title
    text = TITLE_FONT.render('HANGMAN', 1, BLACK)
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    window.blit(text, (350, 200))  # we later need to check that the word does not go off the screen if it is too long

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            window.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    window.blit(images[wrong_guesses], (150, 100))
    pygame.display.update()

def display_message(message):
    pygame.time.delay(1500)
    window.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global wrong_guesses
    # game loop setup
    FPS = 60
    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

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
        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        if won:
            display_message('You WON!')
            break

        if wrong_guesses == 6:
            display_message('You LOST!')
            break

main()
pygame.quit()


