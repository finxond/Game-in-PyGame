import pygame

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((910, 512))
pygame.display.set_caption("Путешествие героя")
icon = pygame.image.load('image/icon.png')
pygame.display.set_icon(icon)

bg = pygame.image.load('image/background_forest.jpg')
Emma = pygame.image.load('Hero/Emma/Left/Emma_Left1.png')

Emma_walk_left = [
    pygame.image.load('Hero/Emma/Left/Emma_Left1.png'),
    pygame.image.load('Hero/Emma/Left/Emma_Left2.png'),
    pygame.image.load('Hero/Emma/Left/Emma_Left3.png'),
]

Emma_walk_right = [
    pygame.image.load('Hero/Emma/Right/Emma_right1.png'),
    pygame.image.load('Hero/Emma/Right/Emma_right1.png'),
    pygame.image.load('Hero/Emma/Right/Emma_right1.png'),
]

Emma_anim_count = 0

running = True
while running:

    screen.blit(bg, (0,0))
    screen.blit(Emma_walk_right[Emma_anim_count], (300, 360))

if Emma_anim_count == 2:
    Emma_anim_count = 0
else:
    Emma_anim_count += 1



    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

clock.tick(10)