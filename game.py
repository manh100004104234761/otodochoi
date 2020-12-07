import os
import random
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2

CAPTION = "Hello world"
SCREEN_SIZE = (1084, 720)
destination = (-100, -100)


class Car(object):
    def __init__(self, CAR_IMAGE, ROAD_IMAGE, x, y, angle=-90.0, length=2):
        self.image = CAR_IMAGE
        self.road = ROAD_IMAGE
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(0, 0))
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.steering = 0.0

    def update(self, dt):
        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0
        self.rect.center = self.position
        next_position = self.position + self.velocity.rotate(-self.angle) * dt
        if self.road.get_at((int(next_position[0]), int(next_position[1]))) == (0, 0, 0, 255):
            self.position = next_position
            self.angle += degrees(angular_velocity) * dt
        else:
            return


class Map(object):
    def __init__(self, map_image, car):
        self.image = map_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.car = car
        self.car.rect.center = self.rect.center
        self.finished_flag = pygame.image.load("flag.png").convert_alpha()

    def update(self, dt):
        self.car.update(dt)

    def draw(self, surface):
        new_image = self.image.copy()
        surface.blit(new_image, (0, 0))
        rotated = pygame.transform.rotate(self.car.image, self.car.angle)
        rect = rotated.get_rect()
        self.car.rect = rect
        surface.blit(rotated, self.car.position -
                     (rect.width / 2, rect.height/2))
        surface.blit(self.finished_flag,
                     (destination[0] - 32, destination[1] - 27))
        pygame.display.flip()


class Control(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.keys = pygame.key.get_pressed()
        self.done = False
        self.car = Car(CAR_IMAGE, ROAD_IMAGE, 0, 0)
        self.map = Map(MAP_IMAGE, self.car)
        self.count_clicked = 0
        self.ready = False

    def event_loop(self):
        global destination
        for event in pygame.event.get():
            if (self.ready):
                self.keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                    self.done = True
                if self.keys[pygame.K_r]:
                    self.count_clicked = 0
                    self.ready = False
                if self.keys[pygame.K_w]:
                    self.car.velocity.x = 60
                elif self.keys[pygame.K_s]:
                    self.car.velocity.x = -60
                else:
                    self.car.velocity.x = 0

                if self.keys[pygame.K_d]:
                    self.car.steering = -4
                elif self.keys[pygame.K_a]:
                    self.car.steering = 4
                else:
                    self.car.steering = 0
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    self.count_clicked += 1
                    if (self.count_clicked == 1):
                        if (ROAD_IMAGE.get_at((int(pos[0]), int(pos[1]))) == (0, 0, 0, 255)):
                            self.car = Car(
                                CAR_IMAGE, ROAD_IMAGE, pos[0], pos[1])
                            self.map = Map(MAP_IMAGE, self.car)
                        else:
                            print("not in road, pls click again")
                            self.count_clicked -= 1
                    if (self.count_clicked == 2):
                        if (ROAD_IMAGE.get_at((int(pos[0]), int(pos[1]))) == (0, 0, 0, 255)):
                            destination = pos
                            self.ready = True
                        else:
                            print("not in road, pls click again")
                            self.count_clicked -= 1

    def display_fps(self):
        caption = "{} - FPS: {:.2f}".format(CAPTION, self.clock.get_fps())
        pygame.display.set_caption(caption)

    def update(self, dt):
        """
        Update the level. In this implementation player updating is taken
        care of by the level update function.
        """
        self.screen.fill(pygame.Color("black"))
        self.map.update(dt)
        self.map.draw(self.screen)

    def main_loop(self):
        while not self.done:
            dt = self.clock.get_time() / 1000
            self.event_loop()
            self.update(dt)
            pygame.display.update()
            self.clock.tick(self.fps)
            self.display_fps()


def main():
    global MAP_IMAGE, CAR_IMAGE, ROAD_IMAGE
    pygame.init()
    pygame.display.set_caption("car")
    pygame.display.set_mode(SCREEN_SIZE)
    CAR_IMAGE = pygame.image.load("car32x16.png").convert_alpha()
    MAP_IMAGE = pygame.image.load("map1084x720.png").convert_alpha()
    ROAD_IMAGE = pygame.image.load("road1084x720.png").convert_alpha()
    Control().main_loop()
    pygame.quit()


if __name__ == "__main__":
    main()
