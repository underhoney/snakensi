import pygame, sys, time, random

vitesse = 10

# Taille écran jeux
frame_size_x = 720
frame_size_y = 480

# Check erreurs
check_errors = pygame.init()

if check_errors[1] > 0:
    print(f'[!] Il y a eu {check_errors[1]} erreurs quand le jeu a voulu démarrer ...')
    sys.exit(-1)
else:
    print('[+] Jeu lancer correctement')


# Initialisation taille fenetre
pygame.display.set_caption('Snake NSI')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Définition couleur
noir = pygame.Color(0, 0, 0)
blanc = pygame.Color(255, 255, 255)
rouge = pygame.Color(255, 0, 0)
vert = pygame.Color(0, 255, 0)
bleu = pygame.Color(0, 0, 255)


# Controle du nombre de fps pour qu'il soit ni trop élevé, ni trop bas
fps_controller = pygame.time.Clock()


# Variable jeu
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

# on génere aléatoirement la nouriture
food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# mort
def game_over():
    my_font = pygame.font.SysFont('times new roman', 80)
    game_over_surface = my_font.render('TU ES MORT', True, rouge)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(noir)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, rouge, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)


# Principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Quand une touche est pousser vers le bas
        elif event.type == pygame.KEYDOWN:
            # Z -> HAUT; S -> BAS; Q -> GAUCHE; D -> DROITE
            if event.key == pygame.K_UP or event.key == ord('z'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('q'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            # Pour echap le jeux (quitter)
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # On s'assure que deux directions opossés ne sont pas en meme tmeps
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Deplacement serpent
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Grandissement serpent
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawn nouritture
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    # Visuel
    game_window.fill(noir)
    for pos in snake_body:
        # Dessin serpent
        # jeu, couleur, xy-coordonées)
        pygame.draw.rect(game_window, vert, pygame.Rect(pos[0], pos[1], 10, 10))

    # Nouritture
    pygame.draw.rect(game_window, blanc, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Condition fin
    # Ecrasement contre le mur
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over()
    # Touche son propre corps
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, blanc, 'consolas', 20)
    #

    # Refresh l'ecran'
    pygame.display.update()
    # Refresh fps
    fps_controller.tick(vitesse)