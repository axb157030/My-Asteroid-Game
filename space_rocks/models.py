from abc import abstractmethod
from pygame.math import Vector2
import pygame
from pygame.transform import rotozoom
from utils import load_sprite, get_random_velocity, remove_background
UP = pygame.math.Vector2(0, -1)

class GameObject:
    @abstractmethod
    def draw(self):
        pass
    @abstractmethod
    def move(self, damping=.98):
        pass
    @abstractmethod
    def collides_with(self, other_obj):
        pass
class AsteroidGameObject(GameObject):
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        self.direction = Vector2(UP)
        

    def draw(self, surface):
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        # Calculate 4% of screen dimensions
        target_width = int(screen_width * .04)
        target_height = int(screen_height * .04)

        # Scale the sprite
        self.sprite = pygame.transform.scale(self.sprite, (target_width, target_height))
        self.radius = self.sprite.get_width() / 2
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        self.position.x %= screen_width
        self.position.y %= screen_height
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def move(self, damping=.98):
                # Apply velocity to position
        self.position += self.velocity




# Example for AsteroidGameObject or Asteroid class

    def collides_with(self, other):
        # Use a reasonable collision radius for both objects
        collision_distance = self.radius/4 + other.radius
        return self.position.distance_to(other.position) < collision_distance

class Spaceship(AsteroidGameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    LASER_SPEED = 3
    def __init__(self, position, surface,  create_bullet_callback=None):
        self.create_bullet_callback = create_bullet_callback
        # Make a copy of the original UP vector
        #remove_background("spaceship")
        self.direction = Vector2(UP)

        super().__init__(position, load_sprite("spaceship"), Vector2(0))
        screen_width = surface.get_width()
        target_width = int(screen_width * .04)
        self.radius = target_width  / 2
        
    
    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)
        
    def accelerate(self, damping=.98):
        self.velocity += self.direction * self.ACCELERATION
        # Apply damping to velocity
        #damping = 0.98  # Adjust between 0.90 (strong drag) and 1.0 (no drag)
        self.velocity *= damping
    def shoot(self, surface):
        laser_velocity = self.direction * self.LASER_SPEED + self.velocity
        bullet = Laser(self.position, laser_velocity, surface)
        self.create_bullet_callback(bullet)
        # Add crash animation
    """def generate_crash_frames(self, num_frames=10):
        frames = []
        for i in range(num_frames):
            # Rotate more each frame
            angle = i * 36  # 360 degrees over 10 frames
            rotated = pygame.transform.rotate(self.sprite, angle)

            # Scale down gradually
            scale_factor = 1 - (i / num_frames)
            new_size = (int(rotated.get_width() * scale_factor), int(rotated.get_height() * scale_factor))
            scaled = pygame.transform.scale(rotated, new_size)

            # Optional: add fading effect
            faded = scaled.copy()
            faded.set_alpha(255 - int((i / num_frames) * 255))

            frames.append(faded)
        return frames """
        

class Asteroid(AsteroidGameObject):
    def __init__(self, position, surface):
            super().__init__(
            position, load_sprite("asteroid"), get_random_velocity(1, 2)
    )
            screen_width = surface.get_width()
            target_width = int(screen_width * .04)
            self.radius = target_width  / 2
            
class BigAsteroid(AsteroidGameObject):
    def __init__(self, position, surface):
            super().__init__(
            position, load_sprite("asteroid"), get_random_velocity(1, 1)
    )
            screen_width = surface.get_width()
            target_width = int(screen_width * .2)
            self.radius = target_width  / 2
            
    def draw(self, surface):
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        # Calculate 4% of screen dimensions
        target_width = int(screen_width * .2)
        target_height = int(screen_height * .2)

        # Scale the sprite
        self.sprite = pygame.transform.scale(self.sprite, (target_width, target_height))
        self.radius = target_width  / 2
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        self.position.x %= screen_width
        self.position.y %= screen_height
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)


class SpaceshipPiece(GameObject):
    def __init__(self, position, image, velocity):
        self.position = Vector2(position)
        self.sprite = image
        self.velocity = Vector2(velocity)
        self.alpha = 255

    def draw(self, surface):
        temp_sprite = self.sprite.copy()
        temp_sprite.set_alpha(self.alpha)
        surface.blit(temp_sprite, self.position)

    def move(self, damping=.98):
        self.position += self.velocity
        self.velocity *= damping
        self.alpha = max(0, self.alpha - 8)  # Fade out  
        #remove_background("asteroid")
   
class Laser(AsteroidGameObject):
    def __init__(self, position, velocity, surface):
        super().__init__(position, load_sprite("laser"), velocity)
        screen_width = surface.get_width()
        target_width = int(screen_width * .04)
        self.radius = target_width  / 2
        #remove_background("laser")

# big asteroid big size and when shot turns into smaller asteroids

class ExplosionPiece(GameObject):
    def __init__(self, position, image, velocity):
        self.position = Vector2(position)
        self.sprite = image
        self.velocity = Vector2(velocity)
        self.alpha = 255

    def draw(self, surface):
        temp_sprite = self.sprite.copy()
        temp_sprite.set_alpha(self.alpha)
        surface.blit(temp_sprite, self.position)

    def move(self, damping=.96):
        self.position += self.velocity
        self.velocity *= damping
        self.alpha = max(0, self.alpha - 12)

class AnimatedExplosionPiece(GameObject):
    def __init__(self, position):
        self.position = Vector2(position)
        self.frames = [
            pygame.image.load(f"../assets/sprites/explosion-sprites/{i}.png").convert_alpha()
            for i in range(1, 20)
        ]
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_duration = 3000 // len(self.frames)  # 3 seconds divided by 19 frames
        self.finished = False

    def draw(self, surface):
        if not self.finished:
            surface.blit(self.frames[self.current_frame], self.position)

    def move(self):
        if not self.finished:
            self.frame_timer += pygame.time.get_ticks() % self.frame_duration
            if self.frame_timer >= self.frame_duration:
                self.frame_timer = 0
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    self.finished = True