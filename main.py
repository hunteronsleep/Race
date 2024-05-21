import pygame as pg
from random import random


class Enemy:
    def __init__(self, _coord_x, _coord_y):
        self.coord_x = _coord_x
        self.coord_y = _coord_y
        self.speed = 0.05
        self.speed_step = round(random() / 10000, 6)
        self.isFinished = False
        self.isAheadOfThePlayer = False

    def Move(self, speed):
        self.coord_x += speed


class Wall:
    def __init__(self, _coord_x, _coord_y, _texture):
        self.coord_x = _coord_x
        self.coord_y = _coord_y
        self.texture = _texture

    def Move(self, speed):
        self.coord_x -= speed


class Finish_line:
    def __init__(self, _width, _height, _start_coords):
        self.width = round(_width, 3)
        self.height = round(_height, 3)
        self.coord_x, self.coord_y = _start_coords

    def Move(self, speed):
        self.coord_x -= speed


screen_width = 700.0
screen_height = 500.0
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Race")
car_width = 35
car_height = 20
finish_line_width = 30.0
finish_line_height = screen_height
wall_color = (0, 0, 200)
wall_width = screen_width
wall_height = 15.0
wall_speed = 0.01
enemy_texture = pg.image.load("Resources/red_car.png")
player_texture = pg.image.load("Resources/green_car.png")
finish_line_texture = pg.image.load("Resources/finish_line.png")
wall_texture = pg.image.load("Resources/wall.png")
enemy_texture = pg.transform.scale(enemy_texture, (car_width, car_height))
player_texture = pg.transform.scale(player_texture, (car_width, car_height))
finish_line_texture = pg.transform.scale(finish_line_texture,
                                         (finish_line_width, screen_height - 2 * wall_height))
wall_texture = pg.transform.scale(wall_texture,
                                  (wall_width, wall_height))
pg.init()
background_color = (96, 96, 96)
coord_x = 30.0
coord_y = float((screen_height - car_height) / 2)
step_x = 0.02
step_y = 0.2
speed_x = 0.1
speed_y = 0.0
max_speed = 0.5
start_interval = 90
race_length_multiplier = 2


walls = [Wall(screen_width, 0, wall_texture),
         Wall(screen_width, screen_height - wall_height, wall_texture)]
for i in range(race_length_multiplier):
    walls.append(Wall(screen_width * (i + 1), 0, wall_texture))
    walls.append(Wall(screen_width * (i + 1),
                 screen_height - wall_height, wall_texture))

enemies = [Enemy(coord_x, coord_y-start_interval),
           Enemy(coord_x, coord_y-start_interval*2),
           Enemy(coord_x, coord_y+start_interval),
           Enemy(coord_x, coord_y+start_interval*2)]


finish_line = Finish_line(finish_line_width, finish_line_height,
                          (len(walls) / 2 * screen_width - finish_line_width,
                           wall_height))


clock = pg.time.Clock()
clock.tick(30)


place = 1


raceIsEnded = False


writings_color = (0, 0, 255)
font = pg.font.SysFont("comicsansms", 20)

while True:
    screen.fill(background_color) #Заполнение экрана цветом асфальта

    #Считывание всех нажатий и выполнение соответствующих действий (выход, ускорение поворот)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                print("Keydown D/right", end="\t")
                if speed_x + step_x <= max_speed:
                    speed_x += step_x
                    speed_x = round(speed_x, 3)
                print("Current speed:", speed_x)
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                print("Keydown A/left", end="\t")
                if speed_x - step_x >= 0:
                    speed_x -= step_x
                    speed_x = round(speed_x, 3)
                print("Current speed:", speed_x)

            if event.key == pg.K_w or event.key == pg.K_UP:
                print("Keydown W/up", end="\t")
                if speed_y >= 0:
                    speed_y = round(speed_y - step_y, 3)
                print("Current speed:", speed_y)
            if event.key == pg.K_s or event.key == pg.K_DOWN:
                print("Keydown W/up", end="\t")
                if speed_y <= 0:
                    speed_y = round(speed_y + step_y, 3)
                print("Current speed:", speed_y)
        if event.type == pg.KEYUP:
            if (event.key == pg.K_w or event.key == pg.K_UP) and speed_y < 0:
                speed_y = 0
            if (event.key == pg.K_s or event.key == pg.K_DOWN) and speed_y > 0:
                speed_y = 0

    #Финиширование и выполнение соответствующих действий
    if round(finish_line.coord_x, 3) <= round(coord_x + car_width, 3) and round(finish_line.coord_x + finish_line_width, 3) >= round(coord_x, 3):
        won_writing = font.render("Your place: " + str(place), 0, writings_color)
        tip_writing = font.render("For race again press any key", 0, writings_color)

        screen.blit(won_writing, (finish_line.coord_x + finish_line_width + 50, wall_height))
        screen.blit(tip_writing, (finish_line.coord_x + finish_line_width + 50, wall_height + 22))

        raceIsEnded = True
        
        speed_x = 0.0
        speed_y = 0.0
        enemies_speed = 0.0
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                raceIsEnded = False
                coord_x = 30.0
                coord_y = float((screen_height - car_height) / 2)
                            
                enemies = [Enemy(coord_x, coord_y-start_interval), Enemy(coord_x, coord_y-start_interval*2), Enemy(coord_x, coord_y+start_interval), Enemy(coord_x, coord_y+start_interval*2)]

                walls = []
                for i in range(race_length_multiplier):
                    walls.append(Wall(screen_width * (i + 1), 0, wall_texture))
                    walls.append(Wall(screen_width * (i + 1), screen_height - wall_height, wall_texture))

                finish_line.coord_x = screen_width * 2 - finish_line_width

                speed_x = 0.1
                speed_y = 0.0
                enemies_speed = 0.1

                place = 1                
        
    screen.blit(finish_line_texture, (finish_line.coord_x, finish_line.coord_y)) #Отрисовка финишной черты

    #Отрисовка всех бортиков и проверка на поражение
    for wall in walls:
        screen.blit(wall.texture, (wall.coord_x, wall.coord_y, wall_width, wall_height))
        wall.Move(speed_x)

        #Притормаживает игру после поражения
        if ((round(wall.coord_y, 3) <= round(coord_y + car_height, 3) and round(wall.coord_y + wall_height, 3) >= round(coord_y, 3)) and (round(wall.coord_x) <= round(coord_x + car_width))) or ((round(wall.coord_y + wall_height, 3) >= round(coord_y, 3) and round(wall.coord_y, 3) <= round(coord_y + car_height, 3)) and (round(wall.coord_x) <= round(coord_x + car_width))) or (round(coord_y) < 0 or round(coord_y) + car_height > screen_height):
            lose_writing = font.render("Game over", 0, writings_color)
            tip_writing = font.render("For race again press any key", 0, writings_color)

            screen.blit(lose_writing, (80, wall_height))
            screen.blit(tip_writing, (80, wall_height + 22))

            speed_x = 0.0
            speed_y = 0.0
            for enemy in enemies:
                enemy.speed = 0.0

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    isGameOver = False
                    coord_x = 30.0
                    coord_y = float((screen_height - car_height) / 2)
                            
                    enemies = [Enemy(coord_x, coord_y-start_interval), Enemy(coord_x, coord_y-start_interval*2), Enemy(coord_x, coord_y+start_interval), Enemy(coord_x, coord_y+start_interval*2)]

                    walls = []
                    for i in range(race_length_multiplier):
                        walls.append(Wall(screen_width * (i + 1), 0, wall_texture))
                        walls.append(Wall(screen_width * (i + 1), screen_height - wall_height, wall_texture))

                    finish_line.coord_x = screen_width * 2 - finish_line_width

                    speed_x = 0.1
                    speed_y = 0.0
                    enemies_speed = 0.1

                    place = 1  

    #отрисовывает игрока
    screen.blit(player_texture, (coord_x, coord_y))

    for enemy in enemies: #В этом цикле все противники отрисовываются, перемещаются и останавливаются если гонщик врезался/финишировал, увеличивает скорость противников (имитирует нажатие на газ), проверяет, обогнал ли игрока кто-нибудь
        screen.blit(enemy_texture, (enemy.coord_x, enemy.coord_y)) #Отрисовка машин противников

        if raceIsEnded: #Не даёт двигаться противникам если гонка окончена
            continue

        enemy.Move(enemy.speed - speed_x) #Выполняет передвижение противников

        if enemy.speed + enemy.speed_step <= max_speed: #Изменение скорости машин противников
            enemy.speed += enemy.speed_step
        else: #Ограничение скорости противников
            enemy.speed = max_speed - 0.05
        
        #проверка на то, впереди игрока конкретный враг или нет
        if not enemy.isAheadOfThePlayer and enemy.coord_x > coord_x:
            enemy.isAheadOfThePlayer = True
            place += 1
        if enemy.isAheadOfThePlayer and enemy.coord_x < coord_x:
            enemy.isAheadOfThePlayer = False
            place -= 1

        #Ниже подобие хитбоксов нужных для поражения, код дублируется в другом месте, мне жаль, но чинить это слишком сложно - появляется куча багов и ошибок
        if (round(enemy.coord_y + car_height, 3) >= round(coord_y, 3) and round(enemy.coord_y, 3) <= round(coord_y + car_height, 3)) and ((round(enemy.coord_x + car_width, 3) >= round(coord_x, 3)) and (round(enemy.coord_x, 3) <= round(coord_x + car_width, 3))) or (coord_x < 0 or coord_y < 0): #В этой суперстрашной строчке реализовано жалкое подобие касаний хитбоксов машин, нужных для того, чтобы игрок проигрывал, сталкиваясь с противником
            lose_writing = font.render("Game over", 0, writings_color)
            tip_writing = font.render("For race again press any key", 0, writings_color)

            screen.blit(lose_writing, (80, wall_height))
            screen.blit(tip_writing, (80, wall_height + 22))

            speed_x = 0.0
            speed_y = 0.0
            for enemy in enemies:
                enemy.speed = 0.0

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    isGameOver = False
                    coord_x = 30.0
                    coord_y = float((screen_height - car_height) / 2)
                            
                    enemies = [Enemy(coord_x, coord_y-start_interval), Enemy(coord_x, coord_y-start_interval*2), Enemy(coord_x, coord_y+start_interval), Enemy(coord_x, coord_y+start_interval*2)]

                    walls = []
                    for i in range(race_length_multiplier):
                        walls.append(Wall(screen_width * (i + 1), 0, wall_texture))
                        walls.append(Wall(screen_width * (i + 1), screen_height - wall_height, wall_texture))

                    finish_line.coord_x = screen_width * 2 - finish_line_width

                    speed_x = 0.1
                    speed_y = 0.0
                    enemies_speed = 0.1

                    place = 1  

    finish_line.Move(speed_x) #Перемещение финишной черты

    coord_y += speed_y #Изменение координат игрока по оси у

    place_writing = font.render("Current place: " + str(place), 0, writings_color) #Объявление и отрисовка надписи о текущем месте игрока
    screen.blit(place_writing, (screen_width - 170, screen_height - 25))

    pg.display.flip()
    