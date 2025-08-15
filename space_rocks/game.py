import pygame
from models import AsteroidGameObject, BigAsteroid, SpaceshipPiece
#from sounds import make_crash_sound
from utils import get_random_position, load_sprite
from models import Asteroid, Spaceship
from pygame.math import Vector2
import random
from models import AnimatedExplosionPiece

class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 260
#https://github.com/clear-code-projects/5games/tree/main/space%20shooter
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((900, 700))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.asteroids = []
        self.lasers = []
        self.spaceship = Spaceship((450, 350), self.screen, self.lasers.append)
        self.spaceship_pieces = []
        self.last_shot_time = 0
        self.crash_sound = pygame.mixer.Sound("../assets/sounds/crash.wav")  # Use your actual path
        self.laser_sound = pygame.mixer.Sound("../assets/sounds/laser.wav")  # Use your actual path
        self.explosion_sound = pygame.mixer.Sound("../assets/sounds/explosion.wav")  # Use your actual path


        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE
                    and all(position.distance_to(a.position) > self.MIN_ASTEROID_DISTANCE for a in self.asteroids)
                ):
                    break
            self.asteroids.append(Asteroid(position, self.screen))
        
        for _ in range(2):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position) > (self.MIN_ASTEROID_DISTANCE + 40)
                    and all(position.distance_to(a.position) > self.MIN_ASTEROID_DISTANCE for a in self.asteroids)
                ):
                    break
            self.asteroids.append(BigAsteroid(position, self.screen))



    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
            if is_key_pressed[pygame.K_DOWN]:
                self.spaceship.accelerate(.6)
            if is_key_pressed[pygame.K_d]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_a]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_w]:
                self.spaceship.accelerate(.99)
            if is_key_pressed[pygame.K_s]:
                self.spaceship.accelerate(.5)
            if is_key_pressed[pygame.K_SPACE]:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_shot_time > 1000:  # 1000 ms = 1 second
                    self.laser_sound.play()
                    self.spaceship.shoot(self.screen)
                    self.last_shot_time = current_time
            

    def _process_game_logic(self):
        # Move all game objects
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
        # Move and fade spaceship pieces and explosion animations
        for piece in self.spaceship_pieces[:]:
            piece.move()
            if hasattr(piece, "finished") and piece.finished:
                self.spaceship_pieces.remove(piece)

        # Spaceship-Asteroid collision
        if self.spaceship:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(self.spaceship):
                    self.crash_sound.play()
                    self._explode_spaceship()
                    self.spaceship = None
                    break

        # Laser-Asteroid collision detection
        for laser in self.lasers[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(laser):
                    self.explosion_sound.play()
                    if isinstance(asteroid, BigAsteroid):
                        # Split into 3 normal asteroids with random directions/speeds
                        for _ in range(3):
                            angle = random.uniform(0, 360)
                            speed = random.uniform(2, 5)
                            velocity = Vector2(speed, 0).rotate(angle)
                            new_asteroid = Asteroid(asteroid.position, self.screen)
                            new_asteroid.velocity = velocity
                            self.asteroids.append(new_asteroid)
                    else:
                        # Spawn animated explosion for small asteroid
                        self.spaceship_pieces.append(
                            AnimatedExplosionPiece(asteroid.position)
                        )
                    self.asteroids.remove(asteroid)
                    if laser in self.lasers:
                        self.lasers.remove(laser)
                    break  # Remove only one asteroid per laser

        # Remove lasers that leave the screen
        for laser in self.lasers[:]:
            if not self.screen.get_rect().collidepoint(laser.position):
                self.lasers.remove(laser)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        for piece in self.spaceship_pieces:
            piece.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = []

        if self.spaceship:
            game_objects.append(self.spaceship)

        game_objects.extend(self.asteroids)
        game_objects.extend(self.lasers)

        return game_objects
    
    def _explode_spaceship(self):
        if not self.spaceship:
            return
        original_sprite = self.spaceship.sprite
        piece_size = original_sprite.get_width() // 4
        center = self.spaceship.position
        for i in range(8):
            angle = i * (360 / 8)
            # Randomize speed and add a downward bias
            speed = 4 + (i % 3) + (pygame.time.get_ticks() % 2)
            velocity = Vector2(speed, 0).rotate(angle) + Vector2(0, 2)
            # Offset initial position for each piece
            offset = Vector2(piece_size // 2, piece_size // 2).rotate(angle)
            start_pos = center + offset
            col = i % 4
            row = i // 4
            rect = pygame.Rect(col * piece_size, row * piece_size, piece_size, piece_size)
            piece_image = original_sprite.subsurface(rect).copy()
            self.spaceship_pieces.append(
                SpaceshipPiece(start_pos, piece_image, velocity)
            )