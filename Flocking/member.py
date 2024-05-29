from setting import *
import pygame
import random
import math
class Member(pygame.sprite.Sprite):
    def __init__(self, game_controller):
        super().__init__()
        self.game_controller = game_controller
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(random.uniform(-SPAWN_RADIUS, SPAWN_RADIUS), random.uniform(-SPAWN_RADIUS, SPAWN_RADIUS))
        self.velocity = pygame.Vector2(random.uniform(-velocity, velocity), random.uniform(-velocity, velocity))
        self.acceleration = pygame.Vector2(0, 0)
        self.wander_target = pygame.Vector2(0, 0)

    def update(self):
        self.acceleration = WANDER_PRIORITY * self.wander() * VALUE[2] + COHESION_PRIORITY * self.cohesion() * VALUE[3] + ALIGNMENT_PRIORITY * self.alignment() * VALUE[4]
        self.acceleration = self.acceleration.normalize() * MAX_ACCELERATION
        self.velocity += self.acceleration * 0.1
        self.velocity = self.velocity.normalize() * MAX_VELOCITY
        self.position += self.velocity
        
        self.position.x = self.wrap_around_float(self.position.x, -BOUNDS, BOUNDS)
        self.position.y = self.wrap_around_float(self.position.y, -BOUNDS, BOUNDS)
        self.rect.center = self.position

    def wander(self):
        deltaTime = 0.01
        self.wander_target += pygame.Vector2(random.uniform(-5, 5) * WANDER_JITTER * deltaTime, random.uniform(-5, 5) * WANDER_JITTER * deltaTime)
        self.wander_target = self.wander_target.normalize() * WANDER_RADIUS

        target_in_local_space = self.wander_target + pygame.Vector2(0, WANDER_DISTANCE)
        target_in_world_space = self.position + target_in_local_space.rotate(self.velocity.angle_to(pygame.Vector2(1, 0)))
        return target_in_world_space.normalize()

    def cohesion(self):
        cohesion_vector = pygame.Vector2(0, 0)
        count_members = 0
        for member in self.game_controller.members:
            if member != self and self.position.distance_to(member.position) <= COHESION_RADIUS:
                if self.is_in_fov(member.position, MAX_FOV):
                    cohesion_vector += member.position
                    count_members += 1

        if count_members != 0:
            cohesion_vector /= count_members
            cohesion_vector -= self.position

        return cohesion_vector

    def alignment(self):
        alignment_vector = pygame.Vector2(0, 0)
        count_members = 0
        for member in self.game_controller.members:
            if member != self and self.position.distance_to(member.position) <= ALIGNMENT_RADIUS:
                if self.is_in_fov(member.position, MAX_FOV):
                    alignment_vector += member.velocity
                    count_members += 1

        if count_members == 0:
            return alignment_vector
        alignment_vector /= count_members
        return alignment_vector.normalize()

    def wrap_around_float(self, value, minimum, maximum):
        if value > maximum:
            return minimum
        elif value < minimum:
            return maximum
        else:
            return value

    def is_in_fov(self, position, angle):
        angle = self.velocity.angle_to(position - self.position)
        return abs(angle) <= angle