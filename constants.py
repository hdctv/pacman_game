# Game constants and configuration

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Tile system
TILE_SIZE = 20
MAZE_WIDTH = 25
MAZE_HEIGHT = 25

# Game settings
INITIAL_LIVES = 3
DOT_POINTS = 10
POWER_PELLET_POINTS = 50
GHOST_POINTS = 200
POWER_PELLET_DURATION = 10.0  # seconds

# Entity states
PACMAN_NORMAL = "normal"
PACMAN_POWERED = "powered"

GHOST_CHASE = "chase"
GHOST_SCATTER = "scatter"
GHOST_VULNERABLE = "vulnerable"
GHOST_RETURNING = "returning"

# Game states
PLAYING = "playing"
GAME_OVER = "game_over"
VICTORY = "victory"
PAUSED = "paused"

# Maze tile types
EMPTY = 0
WALL = 1
DOT = 2
POWER_PELLET = 3
GHOST_SPAWN = 4
PACMAN_SPAWN = 5

# Movement directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Colors (fallback if sprites fail to load)
WALL_COLOR = (0, 0, 255)      # Blue
DOT_COLOR = (255, 255, 0)     # Yellow
POWER_PELLET_COLOR = (255, 255, 255)  # White
PACMAN_COLOR = (255, 255, 0)  # Yellow
GHOST_COLORS = [
    (255, 0, 0),    # Red
    (255, 184, 255), # Pink
    (0, 255, 255),   # Cyan
    (255, 184, 82)   # Orange
]
VULNERABLE_GHOST_COLOR = (0, 0, 255)  # Blue

def grid_to_world(grid_x, grid_y):
    """Convert grid coordinates to world coordinates."""
    return (grid_x * TILE_SIZE, grid_y * TILE_SIZE)

def world_to_grid(world_x, world_y):
    """Convert world coordinates to grid coordinates."""
    return (world_x // TILE_SIZE, world_y // TILE_SIZE)