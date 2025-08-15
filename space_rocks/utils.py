import os
import pygame
import os
from rembg import remove
from PIL import Image
import random
from pygame.math import Vector2

def remove_background(name):
    path = os.path.join(PROJECT_ROOT, "assets", "sprites", f"{name}.png")
    try:
        input_image = Image.open(path).convert("RGBA")
        output_image = remove(input_image).convert("RGBA")
        output_image.save(path)
        print(f"Background removed successfully. Image saved to: {path}")
    except FileNotFoundError:
        print(f"Error: Input image '{path}' not found. Please check the path.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Define the project root based on the current file's location
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def load_sprite(name, with_alpha=True):
    # Build path from project root
    path = os.path.join(PROJECT_ROOT, "assets", "sprites", f"{name}.png")

    try:
        image = pygame.image.load(path)
        if with_alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
        return image
    except pygame.error as e:
        print(f"Failed to load sprite '{name}': {e}")
        raise
    
""""def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h) """
    
def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )
    
def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)