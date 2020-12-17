import pygame
import sys
import random


def draw(x, y, tube1_x, tube2_x, tube2_y, screen, tube1_size_y, a_tube1_x, a_tube1_size_y, a_tube2_y, a_tube2_x):
    """
    the function draws images onto the player , the tubes and the background.

    :param x: player x
    :param y: player y
    :param tube1_x: upper tube x
    :param tube2_x: down tube x
    :param tube2_y: down tube y
    :param screen: screen of the game
    :param tube1_size_y: the y size of the upper tube
    :param a_tube1_x: another upper tube x
    :param a_tube1_size_y: another upper tube y size
    :param a_tube2_y: another down tube y
    :param a_tube2_x: another down tube x
    :return: None
    """
    pepe = pygame.image.load("pepe.png")
    screen.blit(pepe, (x, y))
    tube = pygame.image.load("flappy_tube.png")
    tube2 = pygame.image.load("flappy_tube_2.png")
    screen.blit(tube2, (tube2_x, tube2_y))
    screen.blit(tube, (tube1_x, tube1_size_y - 1000))
    screen.blit(tube2, (a_tube2_x, a_tube2_y))
    screen.blit(tube, (a_tube1_x, a_tube1_size_y - 1000))


def tubes(first_tubes, summon_tube, width, height,  background, tube1_y, tube1_x, tube1_size_x, tube1_size_y, screen, tube2_size_y, tube2_size_x, tube2_x, tube2_y, speed, a_tube1_size_x, a_tube1_size_y, a_tube1_x, a_tube1_y, a_tube2_size_y, a_tube2_size_x, a_tube2_x,  a_tube2_y):

    if first_tubes:
        tube1_x -= speed
        tube2_x = tube1_x
        pygame.draw.rect(screen, background, (tube1_x, tube1_y, tube1_size_x, tube1_size_y))
        pygame.draw.rect(screen, background, (tube2_x, tube2_y, tube2_size_x, tube2_size_y))
    if not summon_tube:
        if tube1_x == width // 2 - tube2_size_x:
            a_tube1_size_y = random.randint(100, height - 400)
            a_tube1_x = width
            a_tube2_y = a_tube1_size_y + 220
            summon_tube = True
    if summon_tube:
        a_tube1_x -= speed
        a_tube2_x = a_tube1_x
        pygame.draw.rect(screen, background, (a_tube1_x, a_tube1_y, a_tube1_size_x, a_tube1_size_y))
        pygame.draw.rect(screen, background, (a_tube2_x, a_tube2_y, a_tube2_size_x, a_tube2_size_y))

    if a_tube1_x == width // 2 - a_tube2_size_x:
        first_tubes = False
        tube1_size_y = random.randint(100, height - 400)
        tube1_x = width
        tube2_y = tube1_size_y + 220
    if not first_tubes:
        tube1_x -= speed
        tube2_x = tube1_x
        pygame.draw.rect(screen, background, (tube1_x, tube1_y, tube1_size_x, tube1_size_y))
        pygame.draw.rect(screen, background, (tube2_x, tube2_y, tube2_size_x, tube2_size_y))
        if a_tube1_x == 0 - 110:
            summon_tube = False
    return tube1_x, tube2_x, a_tube1_x, a_tube2_x, summon_tube, first_tubes, tube1_size_y, tube2_y, a_tube1_size_y, a_tube2_y


def score_function(y, x, tube1_x, a_tube1_x, tube1_size_y, a_tube1_size_y, tube2_y, a_tube2_y, player_size, score):
    if x == tube1_x:
        if y > tube1_size_y and y + player_size[1] < tube2_y:
            score += 1
            point = pygame.mixer.Sound("point.wav")
            point.play()
            point.set_volume(0.2)
    if x == a_tube1_x:
        if y > a_tube1_size_y and y + player_size[1] < a_tube2_y:
            score += 1
            point = pygame.mixer.Sound("point.wav")
            point.play()
            point.set_volume(0.2)
    return score


def collisions(y, height, x, tube1_x, a_tube1_x, tube1_size_y, a_tube1_size_y, tube2_y, a_tube2_y, tube1_size_x, a_tube1_size_x, player_size):
    if y + player_size[1] >= height or y <= 0:
        hit = pygame.mixer.Sound("hit.wav")
        hit.play()
        hit.set_volume(0.4)
        game_over = True
        return game_over
    if (tube1_x < x + player_size[0] < tube1_x + tube1_size_x) or (tube1_x < x < tube1_x + tube1_size_x):
        if not (y > tube1_size_y and y + player_size[1] < tube2_y):
            hit = pygame.mixer.Sound("hit.wav")
            hit.play()
            hit.set_volume(0.4)
            game_over = True
            return game_over
    if (a_tube1_x < x + player_size[0] < a_tube1_x + a_tube1_size_x) or (a_tube1_x < x < a_tube1_x + a_tube1_size_x):
        if not (y > a_tube1_size_y and y + player_size[1] < a_tube2_y):
            hit = pygame.mixer.Sound("hit.wav")
            hit.play()
            hit.set_volume(0.4)
            game_over = True
            return game_over


def jump(y, velocity_up, jump_pressed):
    if jump_pressed:
        velocity_up -= 1
        y -= velocity_up
        if velocity_up <= 0:
            jump_pressed = False

    return y, jump_pressed, velocity_up


def gravitation(y, velocity, jump_pressed):
    if not jump_pressed:
        y += velocity
        velocity += 0.5
        jump_pressed = False
    elif jump_pressed:
        velocity = 0
    return y, velocity, jump_pressed


def main():
    running = True
    while running:
        pygame.init()
        width = 500
        height = 700
        green = [0, 255, 0]
        background = [59, 134, 255]
        black = [0, 0, 0]
        white = [255, 255, 255]
        red = [255, 0, 0]
        screen = pygame.display.set_mode((width, height))
        screen.fill(background)
        game_over = False
        clock = pygame.time.Clock()
        velocity = 0
        velocity_up = 15
        player_size = [60, 51]
        x = 100
        y = height // 2
        tube1_size_y = random.randint(50, height - 400)
        tube1_size_x = 100
        tube1_y = 0
        tube1_x = width
        tube2_size_y = height
        tube2_size_x = tube1_size_x
        tube2_x = tube1_x
        tube2_y = tube1_size_y + 220
        speed = 5
        a_tube1_size_x = 100
        a_tube1_size_y = random.randint(50, height - 400)
        a_tube1_x = width
        a_tube1_y = 0
        a_tube2_size_y = height
        a_tube2_size_x = a_tube1_size_x
        a_tube2_x = a_tube1_x
        a_tube2_y = a_tube1_size_y + 220
        jump_pressed = False
        first_tubes = True
        summon_tube = False
        game_beginning = True
        moving = False
        score = 0
        FPS = 80

        while game_beginning:

            if not moving:
                y -= 1
            if y == 335:
                moving = True
            if y < 375 and moving:
                y += 1
            if y == 375:
                moving = False
            screen.fill(background)
            pygame.draw.rect(screen, background, (x, y, player_size[0], player_size[1]))
            background_image_load = pygame.image.load("background.jpg")
            background_image = screen.blit(background_image_load, (0, 0))
            draw(x, y, tube1_x, tube2_x, tube2_y, screen, tube1_size_y, a_tube1_x, a_tube1_size_y, a_tube2_y, a_tube2_x)
            clock.tick(30)
            game_name = "Flappy Pepe!"
            developer = "Game made by David Plepler"
            game_name_text = pygame.font.Font("pixel_text.ttf", 50)
            name = pygame.font.Font("pixel_text.ttf", 20)
            name_label = name.render(developer, 3, black)
            game_label = game_name_text.render(game_name, 3, black)
            screen.blit(game_label, (10, 0))
            screen.blit(name_label, (30, 60))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        wing = pygame.mixer.Sound("wing.wav")
                        wing.play()
                        wing.set_volume(0.4)
                        jump_pressed = True
                        y, jump_pressed, velocity_up = jump(y, velocity_up, jump_pressed)
                        game_beginning = False
        while not game_over:
            game_over = collisions(y, height, x, tube1_x, a_tube1_x, tube1_size_y, a_tube1_size_y, tube2_y, a_tube2_y, tube1_size_x, a_tube1_size_x, player_size)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        wing = pygame.mixer.Sound("wing.wav")
                        wing.play()
                        wing.set_volume(0.4)
                        velocity_up = 15
                        jump_pressed = True

            y, velocity, jump_pressed = gravitation(y, velocity, jump_pressed)
            y, jump_pressed, velocity_up = jump(y, velocity_up, jump_pressed)

            screen.fill(background)
            score_text = str(score)

            tube1_x, tube2_x, a_tube1_x, a_tube2_x, summon_tube, first_tubes, tube1_size_y, tube2_y, a_tube1_size_y, a_tube2_y = tubes(first_tubes, summon_tube, width, height, background, tube1_y, tube1_x, tube1_size_x, tube1_size_y, screen, tube2_size_y, tube2_size_x, tube2_x, tube2_y, speed, a_tube1_size_x, a_tube1_size_y, a_tube1_x, a_tube1_y, a_tube2_size_y, a_tube2_size_x, a_tube2_x,  a_tube2_y)
            pygame.draw.rect(screen, background, (x, y, player_size[0], player_size[1]))
            score = score_function(y, x, tube1_x, a_tube1_x, tube1_size_y, a_tube1_size_y, tube2_y, a_tube2_y, player_size, score)
            background_image_load = pygame.image.load("background.jpg")
            background_image = screen.blit(background_image_load, (0, 0))
            draw(x, y, tube1_x, tube2_x, tube2_y, screen, tube1_size_y, a_tube1_x, a_tube1_size_y, a_tube2_y, a_tube2_x)
            score_font = pygame.font.Font("score_font.ttf", 50)
            score_label = score_font.render(score_text, 1, black)
            screen.blit(score_label, (width // 2 - 25, 50))
            clock.tick(FPS)
            pygame.display.update()

        if game_over:
            high_score = open("high_score.txt", "r")
            high_score_read = high_score.read()
            if high_score_read == " ":
                high_score_read = "0"
            if int(high_score_read) <= score:
                high_score.close()
                high_score = open("high_score.txt", "w")
                high_score.write(str(score))
                high_score.close()

        while game_over:
            screen.fill(background)
            background_image_load = pygame.image.load("background.jpg")
            background_image = screen.blit(background_image_load, (0, 0))
            high_score = open("high_score.txt", "r")
            high_score_read = high_score.read()
            game_over_text = "PEPE DIED"
            game_over_text_2 = "score: " + str(score)
            game_over_text_3 = "High score: " + str(high_score_read)
            font = pygame.font.Font("pixel_text.ttf", 60)
            font_2 = pygame.font.Font("pixel_text.ttf", 40)
            font_3 = pygame.font.Font("pixel_text.ttf", 30)
            lost_label = font.render(game_over_text, 3, black)
            lost_label2 = font_2.render(game_over_text_2, 3, black)
            lost_label3 = font_3.render(game_over_text_3, 3, black)
            screen.blit(lost_label, (15, 0))
            screen.blit(lost_label2, (width // 2 - 95, 65))
            screen.blit(lost_label3, (0, 110))
            sad_pepe = pygame.image.load("sad_pepe.png")
            screen.blit(sad_pepe, (0, height - 277))
            clock.tick(5)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_beginning = True
                        game_over = False


if __name__ == '__main__':
    main()
