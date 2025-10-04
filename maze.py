"""
Maze system for Pacman game.
Handles maze layout, tile system, and coordinate conversion.
"""

from constants import *

class Maze:
    """Manages the maze layout and provides collision detection."""
    
    def __init__(self):
        """Initialize the maze with the default layout."""
        self.layout = self._create_default_maze()
        self.width = len(self.layout[0])
        self.height = len(self.layout)
    
    def _create_default_maze(self):
        """Create a simple maze layout for testing."""
        # Simple 25x25 maze layout
        maze = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,3,1,1,1,2,1,1,1,1,1,2,1,2,1,1,1,1,1,2,1,1,1,3,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,1,2,1,2,1,1,1,1,1,1,1,1,1,2,1,2,1,1,1,2,1],
            [1,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,1],
            [1,1,1,1,1,2,1,1,1,1,1,0,1,0,1,1,1,1,1,2,1,1,1,1,1],
            [0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0],
            [1,1,1,1,1,2,1,0,1,1,4,4,4,4,4,1,1,0,1,2,1,1,1,1,1],
            [0,0,0,0,0,2,0,0,1,4,4,4,4,4,4,1,0,0,2,0,0,0,0,0,0],
            [1,1,1,1,1,2,1,0,1,4,4,4,4,4,4,1,0,1,2,1,1,1,1,1,1],
            [0,0,0,0,1,2,1,0,1,1,1,1,1,1,1,1,0,1,2,1,0,0,0,0,0],
            [1,1,1,1,1,2,1,0,0,0,0,0,5,0,0,0,0,0,1,2,1,1,1,1,1],
            [0,0,0,0,1,2,1,0,1,1,1,1,1,1,1,1,0,1,2,1,0,0,0,0,0],
            [1,1,1,1,1,2,1,0,1,4,4,4,4,4,4,1,0,1,2,1,1,1,1,1,1],
            [0,0,0,0,0,2,0,0,1,4,4,4,4,4,4,1,0,0,2,0,0,0,0,0,0],
            [1,1,1,1,1,2,1,0,1,1,1,1,1,1,1,1,0,1,2,1,1,1,1,1,1],
            [0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0],
            [1,1,1,1,1,2,1,1,1,1,1,0,1,0,1,1,1,1,1,2,1,1,1,1,1],
            [1,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,1],
            [1,2,1,1,1,2,1,2,1,1,1,1,1,1,1,1,1,2,1,2,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,3,1,1,1,2,1,1,1,1,1,2,1,2,1,1,1,1,1,2,1,1,1,3,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        return maze
    
    def load_maze(self, layout):
        """Load a custom maze layout."""
        self.layout = layout
        self.width = len(layout[0])
        self.height = len(layout)
    
    def is_wall(self, grid_x, grid_y):
        """Check if the given grid position contains a wall."""
        if not self._is_valid_position(grid_x, grid_y):
            return True  # Treat out-of-bounds as walls
        return self.layout[grid_y][grid_x] == WALL  
  
    def get_tile_at(self, grid_x, grid_y):
        """Get the tile type at the given grid position."""
        if not self._is_valid_position(grid_x, grid_y):
            return WALL  # Treat out-of-bounds as walls
        return self.layout[grid_y][grid_x]
    
    def _is_valid_position(self, grid_x, grid_y):
        """Check if the grid position is within maze bounds."""
        return 0 <= grid_x < self.width and 0 <= grid_y < self.height
    
    def world_to_grid(self, world_x, world_y):
        """Convert world coordinates to grid coordinates."""
        return (world_x // TILE_SIZE, world_y // TILE_SIZE)
    
    def grid_to_world(self, grid_x, grid_y):
        """Convert grid coordinates to world coordinates (center of tile)."""
        return (grid_x * TILE_SIZE + TILE_SIZE // 2, 
                grid_y * TILE_SIZE + TILE_SIZE // 2)
    
    def draw(self, screen):
        """Draw the maze using basic colored rectangles."""
        from pygame import Rect
        for y in range(self.height):
            for x in range(self.width):
                tile_type = self.layout[y][x]
                world_x, world_y = grid_to_world(x, y)
                
                # Draw tile based on type
                if tile_type == WALL:
                    screen.draw.filled_rect(
                        Rect(world_x, world_y, TILE_SIZE, TILE_SIZE),
                        WALL_COLOR
                    )
                # Note: Dots and power pellets are now drawn by CollectibleManager
    
    def get_spawn_positions(self):
        """Get spawn positions for Pacman and ghosts."""
        pacman_spawn = None
        ghost_spawns = []
        
        for y in range(self.height):
            for x in range(self.width):
                tile_type = self.layout[y][x]
                if tile_type == PACMAN_SPAWN:
                    pacman_spawn = (x, y)
                elif tile_type == GHOST_SPAWN:
                    ghost_spawns.append((x, y))
        
        return pacman_spawn, ghost_spawns
    
    def can_move_to(self, grid_x, grid_y):
        """Check if an entity can move to the given grid position."""
        # Check bounds
        if not self._is_valid_position(grid_x, grid_y):
            return False
        
        # Check if it's not a wall
        tile_type = self.layout[grid_y][grid_x]
        return tile_type != WALL
    
    def check_wall_collision(self, grid_x, grid_y, direction):
        """Check if moving in a direction would cause a wall collision."""
        new_x = grid_x + direction[0]
        new_y = grid_y + direction[1]
        return not self.can_move_to(new_x, new_y)
    
    def handle_screen_wrapping(self, grid_x, grid_y):
        """Handle screen wrapping for horizontal edges."""
        wrapped_x = grid_x
        wrapped_y = grid_y
        
        # Horizontal wrapping (left/right edges)
        if grid_x < 0:
            wrapped_x = self.width - 1
        elif grid_x >= self.width:
            wrapped_x = 0
        
        # Vertical boundaries are solid (no wrapping)
        if grid_y < 0 or grid_y >= self.height:
            return None  # Invalid position
        
        return (wrapped_x, wrapped_y)
    
    def get_valid_move_position(self, current_x, current_y, direction):
        """Get the valid position after attempting to move in a direction."""
        new_x = current_x + direction[0]
        new_y = current_y + direction[1]
        
        # Handle screen wrapping first
        wrapped_pos = self.handle_screen_wrapping(new_x, new_y)
        if wrapped_pos is None:
            return None  # Invalid move (out of vertical bounds)
        
        new_x, new_y = wrapped_pos
        
        # Check if the new position is valid (not a wall)
        if self.can_move_to(new_x, new_y):
            return (new_x, new_y)
        else:
            return None  # Wall collision
    
    def is_at_maze_edge(self, grid_x, grid_y, direction):
        """Check if position is at maze edge in given direction."""
        if direction == LEFT:
            return grid_x == 0
        elif direction == RIGHT:
            return grid_x == self.width - 1
        elif direction == UP:
            return grid_y == 0
        elif direction == DOWN:
            return grid_y == self.height - 1
        return False