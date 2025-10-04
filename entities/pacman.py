"""
Pacman player entity with movement and basic functionality.
"""

from constants import *

# Import Actor from pygame zero when available
try:
    from pgzero.actor import Actor
except ImportError:
    # Fallback if pgzero is not available
    Actor = None

class Pacman:
    """Pacman player class with movement and positioning."""
    
    def __init__(self, maze):
        """Initialize Pacman with maze reference and starting position."""
        self.maze = maze
        
        # Get spawn position from maze
        pacman_spawn, _ = maze.get_spawn_positions()
        if pacman_spawn:
            self.grid_x, self.grid_y = pacman_spawn
        else:
            # Fallback position if no spawn point found
            self.grid_x, self.grid_y = 12, 18
        
        # Convert to world coordinates for smooth movement
        self.world_x, self.world_y = self.maze.grid_to_world(self.grid_x, self.grid_y)
        
        # Movement state
        self.current_direction = None
        self.next_direction = None
        self.moving = False
        self.move_speed = 2.0  # pixels per frame
        
        # Target position for smooth movement
        self.target_x = self.world_x
        self.target_y = self.world_y
        
        # Game state
        self.state = PACMAN_NORMAL
        
        # Invincibility system for respawn protection
        self.invincible = False
        self.invincibility_timer = 0.0
        self.invincibility_duration = 3.0  # 3 seconds of invincibility after respawn
        
        # Animation state
        self.facing_direction = RIGHT  # Default facing direction
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.2  # Animation frame duration
        
        # Create Actor for sprite rendering (using pgzero Actor)
        try:
            if Actor:
                self.actor = Actor('pacman', center=(self.world_x, self.world_y))
            else:
                self.actor = None
        except:
            # If sprite loading fails, we'll use fallback rendering
            self.actor = None
        
    def update(self):
        """Update Pacman's position and handle movement."""
        self._handle_smooth_movement()
        self._update_animation()
        self._update_invincibility()
        self._update_actor_position()
    
    def move(self, direction):
        """Attempt to move Pacman in the specified direction."""
        if direction in [UP, DOWN, LEFT, RIGHT]:
            self.next_direction = direction
    
    def _handle_smooth_movement(self):
        """Handle smooth movement between grid positions with collision detection."""
        # Check if we can change direction
        if self.next_direction and self._can_change_direction():
            self.current_direction = self.next_direction
            self.facing_direction = self.next_direction  # Update facing direction
            self.next_direction = None
            self._set_new_target()
        
        # Continue moving in current direction if no obstacles
        elif not self.moving and self.current_direction:
            # Validate movement with collision detection
            if self._validate_movement_with_collision():
                self._set_new_target()
            else:
                # Stop moving if we hit a wall
                self.current_direction = None
        
        # Move towards target position
        if self.moving:
            self._move_towards_target()
    
    def _can_change_direction(self):
        """Check if Pacman can change to the next direction."""
        if not self.next_direction:
            return False
        
        # Only allow direction changes when at grid center
        if self.moving:
            return False
        
        return self._can_move_in_direction(self.next_direction)
    
    def _can_move_in_direction(self, direction):
        """Check if Pacman can move in the given direction."""
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
        """Move Pacman towards the target position."""
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
    
    def _validate_movement_with_collision(self):
        """Validate movement using integrated collision detection."""
        if not self.current_direction:
            return False
        
        # Use maze collision detection system
        return not self.maze.check_wall_collision(
            self.grid_x, self.grid_y, self.current_direction
        )
    
    def _update_animation(self):
        """Update animation frame and sprite direction."""
        # Only animate when moving
        if self.moving or self.current_direction:
            self.animation_timer += 1/60.0  # Assuming 60 FPS
            
            if self.animation_timer >= self.animation_speed:
                self.animation_frame = (self.animation_frame + 1) % 8  # 8 frame animation for smoother mouth movement
                self.animation_timer = 0
        else:
            # Reset to closed mouth when not moving
            self.animation_frame = 0
        
        # Update sprite based on facing direction (if using sprites)
        if self.actor:
            self._update_sprite_direction()
    
    def _update_sprite_direction(self):
        """Update sprite image based on facing direction."""
        # This would normally load different sprite images based on direction
        # For now, we'll just rotate the actor or use different images
        try:
            if self.facing_direction == RIGHT:
                self.actor.image = 'pacman_right'
            elif self.facing_direction == LEFT:
                self.actor.image = 'pacman_left'
            elif self.facing_direction == UP:
                self.actor.image = 'pacman_up'
            elif self.facing_direction == DOWN:
                self.actor.image = 'pacman_down'
        except:
            # If directional sprites don't exist, use default
            pass
    
    def _update_invincibility(self):
        """Update invincibility timer and state."""
        if self.invincible:
            self.invincibility_timer -= 1/60.0  # Assuming 60 FPS
            if self.invincibility_timer <= 0:
                self.invincible = False
                self.invincibility_timer = 0.0
    
    def _update_actor_position(self):
        """Update the Actor's position for rendering."""
        if self.actor:
            self.actor.center = (self.world_x, self.world_y)
    
    def reset_position(self):
        """Reset Pacman to spawn position."""
        pacman_spawn, _ = self.maze.get_spawn_positions()
        if pacman_spawn:
            self.grid_x, self.grid_y = pacman_spawn
        else:
            self.grid_x, self.grid_y = 12, 18
        
        self.world_x, self.world_y = self.maze.grid_to_world(self.grid_x, self.grid_y)
        self.target_x = self.world_x
        self.target_y = self.world_y
        self.current_direction = None
        self.next_direction = None
        self.moving = False
        
        # Reset animation state
        self.facing_direction = RIGHT
        self.animation_frame = 0
        self.animation_timer = 0
        
        # Reset invincibility
        self.invincible = False
        self.invincibility_timer = 0.0
        
        self._update_actor_position()
    
    def get_position(self):
        """Get current grid position."""
        return (self.grid_x, self.grid_y)
    
    def get_world_position(self):
        """Get current world position."""
        return (self.world_x, self.world_y)
    
    def get_facing_direction(self):
        """Get current facing direction."""
        return self.facing_direction
    
    def is_moving(self):
        """Check if Pacman is currently moving."""
        return self.moving
    
    def is_invincible(self):
        """Check if Pacman is currently invincible."""
        return self.invincible
    
    def activate_invincibility(self):
        """Activate invincibility period (used after respawn)."""
        self.invincible = True
        self.invincibility_timer = self.invincibility_duration
    
    def respawn(self):
        """Respawn Pacman at spawn position with invincibility."""
        self.reset_position()
        self.activate_invincibility()
    
    def draw(self, screen, shake_x=0, shake_y=0):
        """Draw Pacman with directional animation."""
        if self.actor:
            try:
                # Update actor position with shake offset
                original_center = self.actor.center
                self.actor.center = (original_center[0] + shake_x, original_center[1] + shake_y)
                self.actor.draw()
                self.actor.center = original_center  # Restore original position
                return
            except:
                pass
        
        # Fallback rendering with directional indication
        self._draw_fallback_pacman(screen, shake_x, shake_y)
    
    def _draw_fallback_pacman(self, screen, shake_x=0, shake_y=0):
        """Draw Pacman using colored shapes with enhanced directional mouth animation."""
        radius = TILE_SIZE // 2 - 2
        center_x = int(self.world_x + shake_x)
        center_y = int(self.world_y + shake_y)
        
        # Change color based on power state and invincibility
        pacman_color = PACMAN_COLOR
        
        # Handle invincibility flashing
        if self.invincible:
            # Flash rapidly when invincible
            flash_timer = self.invincibility_timer * 15  # Fast flashing
            if int(flash_timer) % 2 == 0:
                return  # Don't draw Pacman (invisible phase of flashing)
        
        if self.state == PACMAN_POWERED:
            # Flash between yellow and white when powered
            flash_timer = self.animation_timer * 10  # Faster flashing
            if int(flash_timer) % 2 == 0:
                pacman_color = (255, 255, 255)  # White
        
        # Draw main body
        screen.draw.filled_circle((center_x, center_y), radius, pacman_color)
        
        # Enhanced mouth animation with smoother opening/closing
        mouth_open_ratio = self._get_mouth_open_ratio()
        
        if mouth_open_ratio > 0:  # Only draw mouth when it should be open
            self._draw_animated_mouth(screen, center_x, center_y, radius, mouth_open_ratio)
        
        # Add eyes for more character
        self._draw_pacman_eyes(screen, center_x, center_y, radius)
    
    def _get_mouth_open_ratio(self):
        """Calculate how open the mouth should be based on animation frame."""
        # Create smooth mouth opening/closing animation
        if self.animation_frame < 4:
            # Opening phase (0 to 1)
            return self.animation_frame / 3.0
        else:
            # Closing phase (1 to 0)
            return (8 - self.animation_frame) / 4.0
    
    def _draw_animated_mouth(self, screen, center_x, center_y, radius, open_ratio):
        """Draw animated mouth based on facing direction and open ratio."""
        # Calculate mouth size based on open ratio
        max_mouth_size = radius * 0.6
        mouth_size = int(max_mouth_size * open_ratio)
        
        if mouth_size <= 0:
            return
        
        # Draw mouth using circles (simpler approach that works with pygame zero)
        if self.facing_direction == RIGHT:
            # Mouth facing right
            screen.draw.filled_circle(
                (center_x + radius//2, center_y), mouth_size//2, (0, 0, 0)
            )
        elif self.facing_direction == LEFT:
            # Mouth facing left
            screen.draw.filled_circle(
                (center_x - radius//2, center_y), mouth_size//2, (0, 0, 0)
            )
        elif self.facing_direction == UP:
            # Mouth facing up
            screen.draw.filled_circle(
                (center_x, center_y - radius//2), mouth_size//2, (0, 0, 0)
            )
        elif self.facing_direction == DOWN:
            # Mouth facing down
            screen.draw.filled_circle(
                (center_x, center_y + radius//2), mouth_size//2, (0, 0, 0)
            )
    
    def _draw_pacman_eyes(self, screen, center_x, center_y, radius):
        """Draw simple eyes to give Pacman more character."""
        eye_size = 2
        eye_offset_x = radius // 4
        eye_offset_y = radius // 3
        
        # Only draw eyes if mouth isn't too wide open
        mouth_ratio = self._get_mouth_open_ratio()
        if mouth_ratio < 0.7:  # Don't draw eyes when mouth is wide open
            # Left eye
            screen.draw.filled_circle(
                (center_x - eye_offset_x, center_y - eye_offset_y), 
                eye_size, (0, 0, 0)
            )
            
            # Right eye
            screen.draw.filled_circle(
                (center_x + eye_offset_x, center_y - eye_offset_y), 
                eye_size, (0, 0, 0)
            )