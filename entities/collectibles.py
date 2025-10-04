"""
Collectible entities for Pacman game (dots and power pellets).
"""

from constants import *

class Collectible:
    """Base class for collectible items."""
    
    def __init__(self, grid_x, grid_y, points, collectible_type):
        """Initialize collectible at grid position."""
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.points = points
        self.type = collectible_type
        self.collected = False
        
        # Convert to world coordinates
        self.world_x, self.world_y = grid_to_world(grid_x, grid_y)
    
    def collect(self):
        """Mark this collectible as collected and return points."""
        if not self.collected:
            self.collected = True
            return self.points
        return 0
    
    def is_collected(self):
        """Check if this collectible has been collected."""
        return self.collected
    
    def get_position(self):
        """Get grid position of this collectible."""
        return (self.grid_x, self.grid_y)
    
    def get_world_position(self):
        """Get world position of this collectible."""
        return (self.world_x, self.world_y)

class Dot(Collectible):
    """Regular dot collectible."""
    
    def __init__(self, grid_x, grid_y):
        """Initialize dot at grid position."""
        super().__init__(grid_x, grid_y, DOT_POINTS, DOT)
    
    def draw(self, screen, shake_x=0, shake_y=0):
        """Draw the dot if not collected."""
        if not self.collected:
            dot_size = 4
            dot_x = self.world_x + TILE_SIZE // 2 + shake_x
            dot_y = self.world_y + TILE_SIZE // 2 + shake_y
            screen.draw.filled_circle(
                (dot_x, dot_y),
                dot_size // 2,
                DOT_COLOR
            )

class PowerPellet(Collectible):
    """Power pellet collectible that gives special abilities."""
    
    def __init__(self, grid_x, grid_y):
        """Initialize power pellet at grid position."""
        super().__init__(grid_x, grid_y, POWER_PELLET_POINTS, POWER_PELLET)
        self.animation_timer = 0
        self.animation_speed = 0.5  # Blinking speed
    
    def update(self):
        """Update power pellet animation."""
        self.animation_timer += 1/60.0  # Assuming 60 FPS
    
    def draw(self, screen, shake_x=0, shake_y=0):
        """Draw the power pellet with blinking animation if not collected."""
        if not self.collected:
            # Blinking effect
            blink_visible = (self.animation_timer % self.animation_speed) < (self.animation_speed / 2)
            
            if blink_visible:
                pellet_size = 12
                pellet_x = self.world_x + TILE_SIZE // 2 + shake_x
                pellet_y = self.world_y + TILE_SIZE // 2 + shake_y
                screen.draw.filled_circle(
                    (pellet_x, pellet_y),
                    pellet_size // 2,
                    POWER_PELLET_COLOR
                )

class CollectibleManager:
    """Manages all collectibles in the game."""
    
    def __init__(self, maze):
        """Initialize collectible manager with maze reference."""
        self.maze = maze
        self.dots = []
        self.power_pellets = []
        self.total_dots = 0
        self.collected_dots = 0
        
        self._generate_collectibles()
    
    def _generate_collectibles(self):
        """Generate dots and power pellets based on maze layout."""
        self.dots = []
        self.power_pellets = []
        self.total_dots = 0
        self.collected_dots = 0
        
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                tile_type = self.maze.get_tile_at(x, y)
                
                if tile_type == DOT:
                    dot = Dot(x, y)
                    self.dots.append(dot)
                    self.total_dots += 1
                elif tile_type == POWER_PELLET:
                    power_pellet = PowerPellet(x, y)
                    self.power_pellets.append(power_pellet)
    
    def update(self):
        """Update all collectibles."""
        for power_pellet in self.power_pellets:
            power_pellet.update()
    
    def check_collision(self, pacman_grid_x, pacman_grid_y):
        """Check for collisions between Pacman and collectibles."""
        collected_points = 0
        power_pellet_collected = False
        
        # Check dot collisions
        for dot in self.dots:
            if not dot.is_collected() and dot.grid_x == pacman_grid_x and dot.grid_y == pacman_grid_y:
                points = dot.collect()
                collected_points += points
                if points > 0:
                    self.collected_dots += 1
        
        # Check power pellet collisions
        for power_pellet in self.power_pellets:
            if not power_pellet.is_collected() and power_pellet.grid_x == pacman_grid_x and power_pellet.grid_y == pacman_grid_y:
                points = power_pellet.collect()
                collected_points += points
                if points > 0:
                    power_pellet_collected = True
        
        return collected_points, power_pellet_collected
    
    def draw(self, screen, shake_x=0, shake_y=0):
        """Draw all collectibles."""
        # Draw dots
        for dot in self.dots:
            dot.draw(screen, shake_x, shake_y)
        
        # Draw power pellets
        for power_pellet in self.power_pellets:
            power_pellet.draw(screen, shake_x, shake_y)
    
    def get_remaining_dots(self):
        """Get the number of dots remaining to be collected."""
        return self.total_dots - self.collected_dots
    
    def are_all_dots_collected(self):
        """Check if all dots have been collected."""
        return self.collected_dots >= self.total_dots
    
    def reset(self):
        """Reset all collectibles to uncollected state."""
        self.collected_dots = 0
        
        for dot in self.dots:
            dot.collected = False
        
        for power_pellet in self.power_pellets:
            power_pellet.collected = False
            power_pellet.animation_timer = 0