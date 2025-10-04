"""
Ghost entities with AI behavior for Pacman game.
"""

import random
import math
from constants import *

# Import Actor from pygame zero when available
try:
    from pgzero.actor import Actor
except ImportError:
    # Fallback if pgzero is not available
    Actor = None

class Ghost:
    """Ghost entity with AI behavior and state management."""
    
    def __init__(self, maze, ghost_id=0, spawn_position=None):
        """Initialize Ghost with maze reference and AI state."""
        self.maze = maze
        self.ghost_id = ghost_id  # Used for different colors and behaviors
        
        # Get spawn position
        if spawn_position:
            self.grid_x, self.grid_y = spawn_position
        else:
            # Use default spawn position if none provided
            _, ghost_spawns = maze.get_spawn_positions()
            if ghost_spawns and ghost_id < len(ghost_spawns):
                self.grid_x, self.grid_y = ghost_spawns[ghost_id]
            else:
                # Fallback position in ghost house area
                self.grid_x, self.grid_y = 12, 10
        
        # Store original spawn position for respawning
        self.spawn_x, self.spawn_y = self.grid_x, self.grid_y
        
        # Convert to world coordinates for smooth movement
        self.world_x, self.world_y = self.maze.grid_to_world(self.grid_x, self.grid_y)
        
        # Movement state
        self.current_direction = self._get_random_direction()
        self.moving = False
        self.move_speed = 1.5  # Slightly slower than Pacman
        
        # Target position for smooth movement
        self.target_x = self.world_x
        self.target_y = self.world_y
        
        # AI state
        self.state = GHOST_SCATTER  # Start in scatter mode
        self.state_timer = 0.0
        self.scatter_duration = 7.0  # seconds
        self.chase_duration = 20.0   # seconds
        self.vulnerable_duration = 10.0  # seconds
        
        # AI targets and behavior
        self.target_grid_x = 0
        self.target_grid_y = 0
        self._set_scatter_target()
        
        # Direction change timer to prevent rapid direction switching
        self.direction_change_timer = 0.0
        self.min_direction_change_interval = 0.5  # seconds
        
        # Animation state for enhanced visuals
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.15  # Animation frame duration
        self.body_bob_offset = 0.0  # For floating animation
        self.eye_direction = RIGHT  # Direction eyes are looking
        
        # Create Actor for sprite rendering
        try:
            if Actor:
                ghost_sprite = f'ghost_{ghost_id}' if ghost_id < 4 else 'ghost_0'
                self.actor = Actor(ghost_sprite, center=(self.world_x, self.world_y))
            else:
                self.actor = None
        except:
            # If sprite loading fails, we'll use fallback rendering
            self.actor = None
    
    def update(self, pacman_position=None):
        """Update ghost AI, movement, and state."""
        self._update_state_timer()
        self._update_ai_target(pacman_position)
        self._handle_movement()
        self._update_animation(pacman_position)
        self._update_actor_position()
    
    def _update_state_timer(self):
        """Update AI state timers and switch states when needed."""
        self.state_timer += 1/60.0  # Assuming 60 FPS
        self.direction_change_timer += 1/60.0
        
        # State transitions
        if self.state == GHOST_SCATTER:
            if self.state_timer >= self.scatter_duration:
                self.set_state(GHOST_CHASE)
        elif self.state == GHOST_CHASE:
            if self.state_timer >= self.chase_duration:
                self.set_state(GHOST_SCATTER)
        elif self.state == GHOST_VULNERABLE:
            if self.state_timer >= self.vulnerable_duration:
                self.set_state(GHOST_SCATTER)
    
    def set_state(self, new_state):
        """Change ghost state and reset timer."""
        if new_state != self.state:
            self.state = new_state
            self.state_timer = 0.0
            
            # Set appropriate target based on new state
            if new_state == GHOST_SCATTER:
                self._set_scatter_target()
            elif new_state == GHOST_VULNERABLE:
                # Reverse direction when becoming vulnerable
                self._reverse_direction()
    
    def _set_scatter_target(self):
        """Set scatter mode target (corners of the maze)."""
        # Each ghost targets a different corner
        corners = [
            (1, 1),           # Top-left
            (self.maze.width-2, 1),     # Top-right
            (1, self.maze.height-2),    # Bottom-left
            (self.maze.width-2, self.maze.height-2)  # Bottom-right
        ]
        
        corner_index = self.ghost_id % len(corners)
        self.target_grid_x, self.target_grid_y = corners[corner_index]
    
    def _update_ai_target(self, pacman_position):
        """Update AI target based on current state and Pacman position."""
        if self.state == GHOST_CHASE and pacman_position:
            # Target Pacman's current position
            self.target_grid_x, self.target_grid_y = pacman_position
        elif self.state == GHOST_VULNERABLE:
            # Try to avoid Pacman by targeting opposite corner
            if pacman_position:
                pacman_x, pacman_y = pacman_position
                # Target the corner farthest from Pacman
                self.target_grid_x = self.maze.width - 1 - pacman_x
                self.target_grid_y = self.maze.height - 1 - pacman_y
                
                # Clamp to valid positions
                self.target_grid_x = max(1, min(self.maze.width-2, self.target_grid_x))
                self.target_grid_y = max(1, min(self.maze.height-2, self.target_grid_y))
        # GHOST_SCATTER target is set in _set_scatter_target()
    
    def _handle_movement(self):
        """Handle ghost movement with AI pathfinding."""
        # Check if we need to choose a new direction
        if not self.moving and self.direction_change_timer >= self.min_direction_change_interval:
            new_direction = self._choose_best_direction()
            if new_direction:
                self.current_direction = new_direction
                self.direction_change_timer = 0.0
                self._set_new_target()
        
        # Continue moving in current direction
        elif not self.moving and self.current_direction:
            if self._can_move_in_direction(self.current_direction):
                self._set_new_target()
            else:
                # Hit a wall, choose new direction immediately
                self.direction_change_timer = self.min_direction_change_interval
        
        # Move towards target position
        if self.moving:
            self._move_towards_target()
    
    def _choose_best_direction(self):
        """Choose the best direction based on AI state and target."""
        if self.state == GHOST_VULNERABLE:
            # Random movement when vulnerable to be less predictable
            return self._get_random_valid_direction()
        else:
            # Use pathfinding toward target
            return self._get_direction_toward_target()
    
    def _get_direction_toward_target(self):
        """Get direction that moves closest to the target."""
        possible_directions = []
        
        # Check all four directions
        for direction in [UP, DOWN, LEFT, RIGHT]:
            if self._can_move_in_direction(direction):
                # Don't reverse direction unless it's the only option
                if direction != self._get_opposite_direction(self.current_direction):
                    possible_directions.append(direction)
        
        # If no forward directions available, allow reversing
        if not possible_directions:
            for direction in [UP, DOWN, LEFT, RIGHT]:
                if self._can_move_in_direction(direction):
                    possible_directions.append(direction)
        
        if not possible_directions:
            return None
        
        # Choose direction that minimizes distance to target
        best_direction = None
        best_distance = float('inf')
        
        for direction in possible_directions:
            new_x = self.grid_x + direction[0]
            new_y = self.grid_y + direction[1]
            
            # Handle screen wrapping for distance calculation
            wrapped_pos = self.maze.handle_screen_wrapping(new_x, new_y)
            if wrapped_pos:
                new_x, new_y = wrapped_pos
                
                # Calculate distance to target
                dx = new_x - self.target_grid_x
                dy = new_y - self.target_grid_y
                distance = dx * dx + dy * dy
                
                if distance < best_distance:
                    best_distance = distance
                    best_direction = direction
        
        return best_direction
    
    def _get_random_valid_direction(self):
        """Get a random valid direction (avoiding walls)."""
        valid_directions = []
        
        for direction in [UP, DOWN, LEFT, RIGHT]:
            if self._can_move_in_direction(direction):
                valid_directions.append(direction)
        
        if valid_directions:
            return random.choice(valid_directions)
        return None
    
    def _get_random_direction(self):
        """Get a completely random direction."""
        return random.choice([UP, DOWN, LEFT, RIGHT])
    
    def _get_opposite_direction(self, direction):
        """Get the opposite of the given direction."""
        if direction == UP:
            return DOWN
        elif direction == DOWN:
            return UP
        elif direction == LEFT:
            return RIGHT
        elif direction == RIGHT:
            return LEFT
        return None
    
    def _reverse_direction(self):
        """Reverse the current direction."""
        if self.current_direction:
            self.current_direction = self._get_opposite_direction(self.current_direction)
    
    def _can_move_in_direction(self, direction):
        """Check if ghost can move in the given direction."""
        new_pos = self.maze.get_valid_move_position(
            self.grid_x, self.grid_y, direction
        )
        return new_pos is not None
    
    def _set_new_target(self):
        """Set a new target position for smooth movement."""
        if not self.current_direction:
            return
        
        new_pos = self.maze.get_valid_move_position(
            self.grid_x, self.grid_y, self.current_direction
        )
        
        if new_pos:
            # Update grid position
            self.grid_x, self.grid_y = new_pos
            
            # Set world target position
            self.target_x, self.target_y = self.maze.grid_to_world(
                self.grid_x, self.grid_y
            )
            
            self.moving = True
    
    def _move_towards_target(self):
        """Move ghost towards the target position."""
        # Calculate distance to target
        dx = self.target_x - self.world_x
        dy = self.target_y - self.world_y
        distance = (dx * dx + dy * dy) ** 0.5
        
        # Check if we've reached the target
        if distance <= self.move_speed:
            self.world_x = self.target_x
            self.world_y = self.target_y
            self.moving = False
        else:
            # Move towards target
            if distance > 0:
                self.world_x += (dx / distance) * self.move_speed
                self.world_y += (dy / distance) * self.move_speed
    
    def _update_animation(self, pacman_position=None):
        """Update ghost animation frames and visual effects."""
        self.animation_timer += 1/60.0  # Assuming 60 FPS
        
        if self.animation_timer >= self.animation_speed:
            self.animation_frame = (self.animation_frame + 1) % 8  # 8 frame animation
            self.animation_timer = 0
        
        # Update floating bob animation
        self.body_bob_offset = math.sin(self.animation_frame * 0.5) * 2
        
        # Update eye direction based on movement or target
        if self.current_direction:
            self.eye_direction = self.current_direction
        elif pacman_position and self.state == GHOST_CHASE:
            # Look toward Pacman when chasing
            pacman_x, pacman_y = pacman_position
            if pacman_x > self.grid_x:
                self.eye_direction = RIGHT
            elif pacman_x < self.grid_x:
                self.eye_direction = LEFT
            elif pacman_y > self.grid_y:
                self.eye_direction = DOWN
            elif pacman_y < self.grid_y:
                self.eye_direction = UP
    
    def _update_actor_position(self):
        """Update the Actor's position for rendering."""
        if self.actor:
            # Add floating animation to actor position
            bob_y = self.world_y + self.body_bob_offset
            self.actor.center = (self.world_x, bob_y)
    
    def reset_to_spawn(self):
        """Reset ghost to spawn position."""
        self.grid_x, self.grid_y = self.spawn_x, self.spawn_y
        self.world_x, self.world_y = self.maze.grid_to_world(self.grid_x, self.grid_y)
        self.target_x = self.world_x
        self.target_y = self.world_y
        self.current_direction = self._get_random_direction()
        self.moving = False
        self.state = GHOST_SCATTER
        self.state_timer = 0.0
        self.direction_change_timer = 0.0
        self._set_scatter_target()
        self._update_actor_position()
    
    def get_position(self):
        """Get current grid position."""
        return (self.grid_x, self.grid_y)
    
    def get_world_position(self):
        """Get current world position."""
        return (self.world_x, self.world_y)
    
    def get_state(self):
        """Get current AI state."""
        return self.state
    
    def is_vulnerable(self):
        """Check if ghost is in vulnerable state."""
        return self.state == GHOST_VULNERABLE
    
    def draw(self, screen, shake_x=0, shake_y=0):
        """Draw ghost with state-based appearance."""
        if self.actor:
            try:
                # Update sprite based on state
                if self.state == GHOST_VULNERABLE:
                    self.actor.image = 'ghost_vulnerable'
                else:
                    ghost_sprite = f'ghost_{self.ghost_id}' if self.ghost_id < 4 else 'ghost_0'
                    self.actor.image = ghost_sprite
                
                # Update actor position with shake offset
                original_center = self.actor.center
                self.actor.center = (original_center[0] + shake_x, original_center[1] + shake_y)
                self.actor.draw()
                self.actor.center = original_center  # Restore original position
                return
            except:
                pass
        
        # Fallback rendering
        self._draw_fallback_ghost(screen, shake_x, shake_y)
    
    def _draw_fallback_ghost(self, screen, shake_x=0, shake_y=0):
        """Draw ghost using enhanced colored shapes with animations."""
        radius = TILE_SIZE // 2 - 2
        center_x = int(self.world_x + shake_x)
        center_y = int(self.world_y + self.body_bob_offset + shake_y)  # Add floating animation
        
        # Choose color based on state and ghost ID
        if self.state == GHOST_VULNERABLE:
            # Flash between blue and white when vulnerable
            flash_timer = self.state_timer * 8  # Fast flashing
            if self.state_timer > self.vulnerable_duration - 3.0:
                # Flash faster when vulnerability is about to end
                flash_timer = self.state_timer * 16
            
            if int(flash_timer) % 2 == 0:
                ghost_color = VULNERABLE_GHOST_COLOR
            else:
                ghost_color = (255, 255, 255)  # White
        else:
            # Normal ghost colors with slight brightness variation for animation
            base_color = GHOST_COLORS[self.ghost_id % len(GHOST_COLORS)]
            brightness_variation = int(10 * math.sin(self.animation_frame * 0.8))
            ghost_color = tuple(max(0, min(255, c + brightness_variation)) for c in base_color)
        
        # Draw main body with wavy bottom edge
        self._draw_ghost_body(screen, center_x, center_y, radius, ghost_color)
        
        # Draw animated eyes
        self._draw_ghost_eyes(screen, center_x, center_y, radius)
        
        # Add state-specific visual effects
        if self.state == GHOST_VULNERABLE:
            self._draw_vulnerable_effects(screen, center_x, center_y, radius)
    
    def _draw_ghost_body(self, screen, center_x, center_y, radius, color):
        """Draw ghost body with wavy bottom edge."""
        # Draw main circular body
        screen.draw.filled_circle((center_x, center_y), radius, color)
        
        # Draw wavy bottom edge for classic ghost look
        wave_height = 4
        wave_width = 6
        bottom_y = center_y + radius
        
        # Create wavy bottom using small rectangles
        for x in range(center_x - radius, center_x + radius, wave_width):
            wave_offset = int(wave_height * math.sin((x + self.animation_frame * 2) * 0.5))
            rect_height = radius + wave_offset
            
            # Draw rectangle from center to bottom with wave
            from pygame import Rect
            screen.draw.filled_rect(
                Rect(x, center_y - radius, wave_width, rect_height),
                color
            )
    
    def _draw_ghost_eyes(self, screen, center_x, center_y, radius):
        """Draw animated ghost eyes that look in movement direction."""
        eye_size = 4
        pupil_size = 2
        eye_offset_x = radius // 3
        eye_offset_y = radius // 3
        
        # Calculate pupil offset based on eye direction
        pupil_offset_x = 0
        pupil_offset_y = 0
        
        if self.eye_direction == LEFT:
            pupil_offset_x = -1
        elif self.eye_direction == RIGHT:
            pupil_offset_x = 1
        elif self.eye_direction == UP:
            pupil_offset_y = -1
        elif self.eye_direction == DOWN:
            pupil_offset_y = 1
        
        # Left eye
        left_eye_x = center_x - eye_offset_x
        left_eye_y = center_y - eye_offset_y
        
        screen.draw.filled_circle((left_eye_x, left_eye_y), eye_size, (255, 255, 255))
        screen.draw.filled_circle(
            (left_eye_x + pupil_offset_x, left_eye_y + pupil_offset_y), 
            pupil_size, (0, 0, 0)
        )
        
        # Right eye
        right_eye_x = center_x + eye_offset_x
        right_eye_y = center_y - eye_offset_y
        
        screen.draw.filled_circle((right_eye_x, right_eye_y), eye_size, (255, 255, 255))
        screen.draw.filled_circle(
            (right_eye_x + pupil_offset_x, right_eye_y + pupil_offset_y), 
            pupil_size, (0, 0, 0)
        )
    
    def _draw_vulnerable_effects(self, screen, center_x, center_y, radius):
        """Draw special effects when ghost is vulnerable."""
        # Draw scared mouth
        mouth_y = center_y + radius // 3
        mouth_width = radius // 2
        
        # Zigzag mouth to show fear
        mouth_points = []
        for i in range(5):
            x = center_x - mouth_width//2 + (i * mouth_width//4)
            y = mouth_y + (2 if i % 2 == 0 else -2)
            mouth_points.append((x, y))
        
        if len(mouth_points) >= 2:
            for i in range(len(mouth_points) - 1):
                screen.draw.line(mouth_points[i], mouth_points[i + 1], (0, 0, 0))
        
        # Add trembling effect when vulnerability is about to end
        if self.state_timer > self.vulnerable_duration - 3.0:
            tremor = int(2 * math.sin(self.animation_frame * 2))
            # This tremor effect is already included in the body bob offset


class GhostManager:
    """Manages multiple ghosts and their collective behavior."""
    
    def __init__(self, maze, num_ghosts=4):
        """Initialize ghost manager with specified number of ghosts."""
        self.maze = maze
        self.ghosts = []
        
        # Get ghost spawn positions
        _, ghost_spawns = maze.get_spawn_positions()
        
        # Create ghosts
        for i in range(num_ghosts):
            spawn_pos = ghost_spawns[i] if i < len(ghost_spawns) else None
            ghost = Ghost(maze, ghost_id=i, spawn_position=spawn_pos)
            self.ghosts.append(ghost)
    
    def update(self, pacman_position=None):
        """Update all ghosts."""
        for ghost in self.ghosts:
            ghost.update(pacman_position)
    
    def set_all_vulnerable(self):
        """Set all ghosts to vulnerable state."""
        for ghost in self.ghosts:
            ghost.set_state(GHOST_VULNERABLE)
    
    def reset_all_ghosts(self):
        """Reset all ghosts to spawn positions."""
        for ghost in self.ghosts:
            ghost.reset_to_spawn()
    
    def check_collision_with_pacman(self, pacman_position):
        """Check if any ghost collides with Pacman."""
        pacman_x, pacman_y = pacman_position
        
        for ghost in self.ghosts:
            ghost_x, ghost_y = ghost.get_position()
            
            # Check if positions match (same grid cell)
            if ghost_x == pacman_x and ghost_y == pacman_y:
                return ghost
        
        return None
    
    def get_ghosts(self):
        """Get list of all ghosts."""
        return self.ghosts
    
    def draw(self, screen, shake_x=0, shake_y=0):
        """Draw all ghosts."""
        for ghost in self.ghosts:
            ghost.draw(screen, shake_x, shake_y)