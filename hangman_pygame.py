import pygame, os

pygame.init()

WIDTH, HEIGHT = 800, 600

pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman: the Pirates Island")

FPS = 60 
clock = pygame.time.Clock()

is_running = True 

while is_running: 
  clock.tick(FPS)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      is_running = False 
    
    if event.type == pygame.MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      print(pos)


pygame.quit()  

