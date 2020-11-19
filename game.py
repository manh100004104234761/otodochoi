import os
import random
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2

CAPTION = "Hello word"
SCREEN_SIZE = (1280, 720)


class Car(object):
    def __init__(self, CAR_IMAGE, x, y, angle=-90.0, length=4):
        self.image = CAR_IMAGE
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
        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

    def draw(self, surface):
        rotated = pygame.transform.rotate(CAR_IMAGE, self.angle)
        rect = rotated.get_rect()
        self.rect = rect
        surface.blit(rotated, self.position - (rect.width / 2, rect.height/2))
        pygame.display.flip()


class Map(object):
    def __init__(self, map_image, viewport, car):
        self.image = map_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.car = car
        self.car.rect.center = self.rect.center
        self.viewport = viewport

    def update(self, dt):
        self.car.update(dt)
        self.update_viewport()

    def update_viewport(self):
        self.viewport.center = self.car.rect.center
        self.viewport.clamp_ip(self.rect)

    def draw(self, surface):
        new_image = self.image.copy()
        self.car.draw(new_image)
        surface.blit(new_image, (0, 0), self.viewport)


class Control(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 20.0
        self.keys = pygame.key.get_pressed()
        self.done = False
        self.car = Car(CAR_IMAGE, 0, 0)
        self.map = Map(MAP_IMAGE, self.screen_rect.copy(), self.car)

    def event_loop(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                self.done = True
            if self.keys[pygame.K_w]:
                self.car.velocity.x = 100
            elif self.keys[pygame.K_s]:
                self.car.velocity.x = -100
            else:
                self.car.velocity.x = 0

            if self.keys[pygame.K_d]:
                self.car.steering = -10
            elif self.keys[pygame.K_a]:
                self.car.steering = 10
            else:
                self.car.steering = 0

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
    global MAP_IMAGE, CAR_IMAGE
    pygame.init()
    pygame.display.set_caption("car")
    pygame.display.set_mode(SCREEN_SIZE)
    CAR_IMAGE = pygame.image.load("car2.png").convert_alpha()
    MAP_IMAGE = pygame.image.load("map.png").convert_alpha()
    Control().main_loop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
