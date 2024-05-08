import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((910,512))
pygame.display.set_caption("Путешествие героя")
icon = pygame.image.load('image/icon.png').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load('image/background_forest.jpg').convert_alpha()
walk_right = [
    pygame.image.load('Hero/Emma/Right/Emma_right1.png').convert_alpha(),
    pygame.image.load('Hero/Emma/Right/Emma_right2.png').convert_alpha(),
    pygame.image.load('Hero/Emma/Right/Emma_right3.png').convert_alpha()
]
walk_left = [
    pygame.image.load('Hero/Emma/Left/Emma_Left1.png').convert_alpha(),
    pygame.image.load('Hero/Emma/Left/Emma_Left2.png').convert_alpha(),
    pygame.image.load('Hero/Emma/Left/Emma_left3.png').convert_alpha()
]

player_anim_count = 0
bg_x = 0

enemy_image_1 = pygame.image.load('Enemy/Enemy_Left/Enemy_Left1.png').convert_alpha()
enemy_image_2 = pygame.image.load('Enemy/Enemy_Left/Enemy_Left1.png').convert_alpha()
enemy_image_3 = pygame.image.load('Enemy/Enemy_Left/Enemy_Left1.png').convert_alpha()

enemy = [enemy_image_1, enemy_image_2, enemy_image_3]


enemy_anim_count = 0

enemy_x = 880
enemy_y = 400
ghost_list_in_game = []

player_speed = 5
player_x = 100
player_y = 400

is_jump = False
jump_count = 10

bg_sound = pygame.mixer.Sound('Songs/night.mp3')
bg_sound.play()

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 3200)

label = pygame.font.Font('Fonts/Blackadder.ttf', 40)
lose_label = label.render('You loser!', False, (193, 196, 199))
restart_label = label.render('Restart!', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(180, 200))
gameplay = True

bullet = pygame.image.load('Weapon/Bullet_Right.png').convert_alpha()
bullets = []
running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 910, 0))

    if gameplay:
        if ghost_list_in_game:
            for (i, enemy_rect) in enumerate(ghost_list_in_game):
                screen.blit(enemy[enemy_anim_count], (enemy_rect.x, enemy_rect.y))
                enemy_rect.x -= 10

            if enemy_rect.x < -10:
                ghost_list_in_game.pop(i)

            if player_rect.colliderect(enemy_rect):
                gameplay = False

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
        enemy_rect = enemy[0].get_rect(topleft=(enemy_x,enemy_y))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 5:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 850:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -10:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 10

        if player_anim_count == 2:
            player_anim_count = 0
        else:
            player_anim_count += 1

        if enemy_anim_count == 2:
            enemy_anim_count = 0
        else:
            enemy_anim_count = 0

        bg_x-= 2
        if bg_x == -910:
            bg_x = 0


        if keys[pygame.K_z]:
             bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 10

                if el.x > 910:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, ghost) in enumerate (ghost_list_in_game):
                        if el.colliderect(ghost):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)



    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label, (180, 200))

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 100
            ghost_list_in_game.clear()
            bullets.clear()
            bullets.pop(i)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer:
            ghost_list_in_game.append(enemy[enemy_anim_count].get_rect(topleft=(880,400)))


    clock.tick(8)