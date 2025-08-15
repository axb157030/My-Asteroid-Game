# Asteroid Game

Welcome to **Asteroid Game**!  
This is a Python/Pygame project inspired by classic arcade asteroid shooters, with some custom touches.

## How to Run

1. Open a terminal and navigate to the `space_rocks` directory:
    ```
    cd space_rocks
    ```
2. Run the game:
    ```
    python __main__.py
    ```

## Resources & Inspiration

- Game mechanics and some assets are inspired or taken by:
  - [Real Python Asteroids Game Tutorial](https://realpython.com/asteroids-game-python/)
  - [Clear Code Projects - Space Shooter](https://github.com/clear-code-projects/5games/tree/main/space%20shooter)
- Pictures and some code were adapted from these sources, but **I added my own touches to the gameplay and features**.

## Project Structure & Utilities

- **`utils.py`**: Contains helper functions, including `remove_background`, which removes the background from image files directly under the `sprites` folder (located in the `assets` directory).
- **`sounds.py`**: Most sound files were created using this Python file, though not all sounds in the game were made this way.

## Notes

- Make sure you have all dependencies installed (`pygame`, `rembg`, `Pillow`).
- Place your sprites in `assets/sprites/` and sounds in `assets/sounds/`.
- Enjoy blasting asteroids and watch out for custom explosions and effects!
