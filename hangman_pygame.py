import pygame
import math

# setup display
pygame.init()
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman: the Pirates Island")

# load images
images = []
for i in range(7):
  image = pygame.image.load("hangman"+str(i)+".png")
  images.append(image)

# game variables 
wrong_guesses = 0
word = 'HANGMAN'
guessed = []

# colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# fonts
LETTER_FONT = pygame.font.SysFont('arial', 35)
WORD_FONT = pygame.font.SysFont('comicsans', 60)

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

# game loop setup
FPS = 60 
clock = pygame.time.Clock()
is_running = True 

def draw():
  window.fill(WHITE)

  # draw word
  display_word = ""
  for letter in word: 
    if letter in guessed: 
      display_word += letter + " "
    else:
      display_word += "_ "
  text = WORD_FONT.render(display_word, 1, BLACK)
  window.blit(text, (350, 200)) # we later need to check that the word does not go off the screen if it is too long

  # draw buttons 
  for letter in letters: 
    x,y,ltr, visible = letter
    if visible:
      pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)
      text = LETTER_FONT.render(ltr, 1, BLACK)
      window.blit(text, (x - text.get_width()/2, y - text.get_height()/2))


  window.blit(images[wrong_guesses], (150, 100))
  pygame.display.update()

while is_running: 
  clock.tick(FPS)
  draw()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      is_running = False 
    
    if event.type == pygame.MOUSEBUTTONDOWN:
      m_x, m_y = pygame.mouse.get_pos()
      for letter in letters: 
        x, y, ltr, visible = letter
        if visible: 
          distance = math.sqrt((x - m_x)**2 + (y - m_y)**2) # determine the distance between two points (mouse cursor and button)
          if distance < RADIUS: 
            letter[3] = False
            guessed.append(ltr)
      
pygame.quit()  

