import pygame, sys, time, random
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
fps_controller = pygame.time.Clock()
    my_font = pygame.font.SysFont('times new roman', 90)
    pygame.display.flip()
    pygame.quit()
    score_font = pygame.font.SysFont(font, size)
    # pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
            if event.key == pygame.K_DOWN or event.key == ord('s'):
            if event.key == pygame.K_LEFT or event.key == ord('a'):
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    pygame.display.update()
