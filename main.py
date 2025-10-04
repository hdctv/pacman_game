#!/usr/bin/env python3
"""
Pacman Game - Main Entry Point
Built with pygamezero
"""

import pgzrun
import random
import math
from constants import *
from maze import Maze
from entities.pacman import Pacman
from entities.collectibles import CollectibleManager
from entities.ghost import GhostManager
from ui import UIManager
from audio import PygameZeroAudioManager

class ParticleEffect:
    """Simple particle effect for visual feedback."""
    
    def __init__(self, x, y, color, effect_type="dot"):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.color = color
        self.effect_type = effect_type
        self.timer = 0.0
        self.duration = 0.5  # seconds
        
        # Different effects have different behaviors
        if effect_type == "dot":
            self.velocity_x = random.uniform(-20, 20)
            self.velocity_y = random.uniform(-30, -10)
            self.size = 3
        elif effect_type == "power_pellet":
            self.velocity_x = random.uniform(-40, 40)
            self.velocity_y = random.uniform(-50, -20)
            self.size = 5
            self.duration = 1.0
        elif effect_type == "ghost_eaten":
            self.velocity_x = random.uniform(-30, 30)
            self.velocity_y = random.uniform(-40, -15)
            self.size = 4
            self.duration = 0.8
        elif effect_type == "score_popup":
            self.velocity_x = 0
            self.velocity_y = -30
            self.size = 6
            self.duration = 1.5
            self.text = str(color)  # For score popups, color contains the score value
            self.color = (255, 255, 0)  # Yellow for score
    
    def update(self):
        """Update particle position and lifetime."""
        self.timer += 1/60.0  # Assuming 60 FPS
        
        # Update position
        self.x += self.velocity_x * (1/60.0)
        self.y += self.velocity_y * (1/60.0)
        
        # Apply gravity for some effects
        if self.effect_type in ["dot", "power_pellet", "ghost_eaten"]:
            self.velocity_y += 100 * (1/60.0)  # Gravity
        
        # Fade out over time
        return self.timer < self.duration
    
    def draw(self, screen, shake_offset_x=0, shake_offset_y=0):
        """Draw the particle effect."""
        if self.effect_type == "score_popup":
            # Draw text for score popup
            alpha = 1.0 - (self.timer / self.duration)
            if alpha > 0:
                # Calculate color with fade
                fade_color = tuple(int(c * alpha) for c in self.color)
                screen.draw.text(
                    f"+{self.text}",
                    center=(int(self.x + shake_offset_x), int(self.y + shake_offset_y)),
                    fontsize=14,
                    color=fade_color
                )
        else:
            # Draw particle as circle
            alpha = 1.0 - (self.timer / self.duration)
            if alpha > 0:
                # Calculate size and color with fade
                current_size = int(self.size * alpha)
                fade_color = tuple(int(c * alpha) for c in self.color)
                
                if current_size > 0:
                    screen.draw.filled_circle(
                        (int(self.x + shake_offset_x), int(self.y + shake_offset_y)),
                        current_size,
                        fade_color
                    )

def add_particle_effect(x, y, color, effect_type="dot"):
    """Add a new particle effect to the global list."""
    global particle_effects
    particle_effects.append(ParticleEffect(x, y, color, effect_type))

def add_screen_shake(intensity, duration=0.3):
    """Add screen shake effect."""
    global screen_shake_timer, screen_shake_intensity
    screen_shake_timer = duration
    screen_shake_intensity = intensity

class GameStateManager:
    """Manages game state transitions and timing."""
    
    def __init__(self):
        self.state_timers = {
            PLAYING: 0.0,
            GAME_OVER: 0.0,
            VICTORY: 0.0,
            PAUSED: 0.0
        }
        self.previous_state = None
        self.state_change_callbacks = {}
    
    def update_state_timer(self, current_state):
        """Update the timer for the current state."""
        self.state_timers[current_state] += 1/60.0
    
    def change_state(self, new_state):
        """Change game state and handle transitions."""
        global game_state
        if new_state != game_state:
            self.previous_state = game_state
            game_state = new_state
            self.state_timers[new_state] = 0.0
            
            # Execute state change callback if exists
            if new_state in self.state_change_callbacks:
                self.state_change_callbacks[new_state]()
    
    def get_state_time(self, state):
        """Get how long we've been in a specific state."""
        return self.state_timers.get(state, 0.0)
    
    def register_state_callback(self, state, callback):
        """Register a callback for when entering a specific state."""
        self.state_change_callbacks[state] = callback

# Initialize game state manager
game_state_manager = GameStateManager()

def optimize_collision_detection():
    """Optimize collision detection by using spatial partitioning."""
    # This could be expanded to use a spatial grid for better performance
    # For now, we'll just ensure we're not doing unnecessary checks
    pass

def update_performance_metrics():
    """Update performance metrics for optimization."""
    global frame_count, last_fps_update, current_fps
    
    frame_count += 1
    current_time = frame_count / 60.0  # Approximate time based on 60 FPS
    
    if current_time - last_fps_update >= 1.0:  # Update every second
        current_fps = frame_count / (current_time - last_fps_update) if last_fps_update > 0 else 60.0
        last_fps_update = current_time
        frame_count = 0

# Global game variables (pygamezero style)
maze = Maze()  # Initialize maze first
pacman = Pacman(maze)  # Initialize Pacman with maze reference
collectible_manager = CollectibleManager(maze)  # Initialize collectibles
ghost_manager = GhostManager(maze, num_ghosts=4)  # Initialize ghosts
ui_manager = UIManager()  # Initialize UI manager
audio_manager = PygameZeroAudioManager()  # Initialize audio manager
score = 0
lives = INITIAL_LIVES
game_state = PLAYING
power_mode_timer = 0.0
power_mode_active = False
screen_flash_timer = 0.0

# Enhanced visual effects
screen_shake_timer = 0.0
screen_shake_intensity = 0.0
particle_effects = []  # List to store particle effects

# Game state management
game_start_timer = 0.0
level_complete_timer = 0.0
death_animation_timer = 0.0
game_paused_time = 0.0

# Performance optimization
frame_count = 0
last_fps_update = 0.0
current_fps = 60.0

# Screen dimensions for pygamezero
WIDTH = SCREEN_WIDTH
HEIGHT = SCREEN_HEIGHT

def update():
    """Optimized main game update loop - called by pygamezero."""
    global game_state, score, lives, power_mode_timer, power_mode_active, screen_flash_timer
    global screen_shake_timer, screen_shake_intensity, particle_effects
    
    # Update performance metrics
    update_performance_metrics()
    
    # Update game state timer
    game_state_manager.update_state_timer(game_state)
    
    # Update visual effects (always update for smooth transitions)
    _update_visual_effects()
    
    # State-specific updates
    if game_state == PLAYING:
        _update_playing_state()
    elif game_state == GAME_OVER:
        _update_game_over_state()
    elif game_state == VICTORY:
        _update_victory_state()
    elif game_state == PAUSED:
        _update_paused_state()

def _update_playing_state():
    """Update game logic during playing state."""
    global score, lives, power_mode_timer, power_mode_active, screen_flash_timer
    # Update entities (optimized order for better performance)
    pacman.update()
    
    # Only update collectibles if needed (performance optimization)
    collectible_manager.update()
    
    # Update ghosts with Pacman's position for AI
    pacman_position = pacman.get_position()
    ghost_manager.update(pacman_position)
    
    # Optimized collision detection
    _handle_collectible_collisions(pacman_position)
    _handle_ghost_collisions(pacman_position)
    
    # Update power mode
    _update_power_mode()
    
    # Check victory condition
    if collectible_manager.are_all_dots_collected():
        game_state_manager.change_state(VICTORY)
        audio_manager.play_victory()

def _handle_collectible_collisions(pacman_position):
    """Handle collectible collision detection and effects."""
    global score, power_mode_active, power_mode_timer, screen_flash_timer
    
    pacman_grid_x, pacman_grid_y = pacman_position
    collected_points, power_pellet_collected = collectible_manager.check_collision(
        pacman_grid_x, pacman_grid_y
    )
    
    if collected_points > 0:
        score += collected_points
        pacman_world_x, pacman_world_y = pacman.get_world_position()
        
        if collected_points == DOT_POINTS:
            audio_manager.play_dot_collect()
            add_particle_effect(pacman_world_x, pacman_world_y, DOT_COLOR, "dot")
            add_particle_effect(pacman_world_x, pacman_world_y, collected_points, "score_popup")
        elif collected_points == POWER_PELLET_POINTS:
            audio_manager.play_power_pellet()
            add_particle_effect(pacman_world_x, pacman_world_y, POWER_PELLET_COLOR, "power_pellet")
            add_particle_effect(pacman_world_x, pacman_world_y, collected_points, "score_popup")
            add_screen_shake(3, 0.2)
    
    # Handle power pellet activation
    if power_pellet_collected:
        power_mode_active = True
        power_mode_timer = POWER_PELLET_DURATION
        pacman.state = PACMAN_POWERED
        screen_flash_timer = 0.3
        ghost_manager.set_all_vulnerable()

def _handle_ghost_collisions(pacman_position):
    """Handle ghost collision detection and effects."""
    global score, lives, power_mode_active, power_mode_timer, screen_flash_timer
    
    if pacman.is_invincible():
        return
    
    collided_ghost = ghost_manager.check_collision_with_pacman(pacman_position)
    if not collided_ghost:
        return
    
    if collided_ghost.is_vulnerable():
        # Ghost eaten
        score += GHOST_POINTS
        ghost_world_x, ghost_world_y = collided_ghost.get_world_position()
        collided_ghost.reset_to_spawn()
        
        # Visual and audio feedback
        screen_flash_timer = 0.2
        add_screen_shake(5, 0.3)
        for _ in range(8):
            add_particle_effect(ghost_world_x, ghost_world_y, VULNERABLE_GHOST_COLOR, "ghost_eaten")
        add_particle_effect(ghost_world_x, ghost_world_y, GHOST_POINTS, "score_popup")
        audio_manager.play_ghost_eat()
    else:
        # Pacman caught
        lives -= 1
        pacman_world_x, pacman_world_y = pacman.get_world_position()
        
        # Visual and audio feedback
        audio_manager.play_pacman_death()
        add_screen_shake(8, 0.5)
        for _ in range(12):
            add_particle_effect(pacman_world_x, pacman_world_y, PACMAN_COLOR, "ghost_eaten")
        
        if lives <= 0:
            game_state_manager.change_state(GAME_OVER)
            audio_manager.play_game_over()
            add_screen_shake(10, 1.0)
        else:
            # Respawn
            pacman.respawn()
            power_mode_active = False
            power_mode_timer = 0.0
            pacman.state = PACMAN_NORMAL
            ghost_manager.reset_all_ghosts()
            screen_flash_timer = 0.5

def _update_power_mode():
    """Update power mode timer and state."""
    global power_mode_active, power_mode_timer, screen_flash_timer
    
    if power_mode_active:
        power_mode_timer -= 1/60.0
        if power_mode_timer <= 0:
            power_mode_active = False
            pacman.state = PACMAN_NORMAL
    
    if screen_flash_timer > 0:
        screen_flash_timer -= 1/60.0

def _update_game_over_state():
    """Update game over state."""
    # Game over state - minimal updates needed
    pass

def _update_victory_state():
    """Update victory state."""
    # Victory state - minimal updates needed
    pass

def _update_paused_state():
    """Update paused state."""
    # Paused state - no game logic updates
    pass

def _update_visual_effects():
    """Update all visual effects including particles and screen shake."""
    global screen_shake_timer, particle_effects, screen_flash_timer
    
    # Update screen shake
    if screen_shake_timer > 0:
        screen_shake_timer -= 1/60.0
        if screen_shake_timer <= 0:
            screen_shake_timer = 0
    
    # Update screen flash
    if screen_flash_timer > 0:
        screen_flash_timer -= 1/60.0
    
    # Update particle effects with memory management
    active_particles = []
    for particle in particle_effects:
        if particle.update():
            active_particles.append(particle)
    
    # Limit particle count for performance (max 50 particles)
    if len(active_particles) > 50:
        active_particles = active_particles[-50:]  # Keep only the newest 50
    
    particle_effects = active_particles

def _get_screen_shake_offset():
    """Calculate screen shake offset based on current shake timer and intensity."""
    if screen_shake_timer <= 0:
        return 0, 0
    
    # Calculate shake intensity that decreases over time
    current_intensity = screen_shake_intensity * (screen_shake_timer / 0.5)  # Assuming max duration of 0.5s
    
    # Generate random offset
    shake_x = random.uniform(-current_intensity, current_intensity)
    shake_y = random.uniform(-current_intensity, current_intensity)
    
    return int(shake_x), int(shake_y)

def draw():
    """Main drawing function - called by pygamezero."""
    screen.clear()
    
    # Get screen shake offset
    shake_x, shake_y = _get_screen_shake_offset()
    
    # Add screen flash effect for power pellet collection
    if screen_flash_timer > 0:
        # Calculate flash intensity (0-255) based on remaining timer
        flash_ratio = min(1.0, screen_flash_timer / 0.3)
        flash_intensity = int(255 * flash_ratio)
        screen.fill((flash_intensity, flash_intensity, flash_intensity))
    
    if game_state == PLAYING:
        # Draw the maze (walls only, collectibles drawn separately) with shake offset
        _draw_maze_walls(screen, shake_x, shake_y)
        
        # Draw collectibles with shake offset
        collectible_manager.draw(screen, shake_x, shake_y)
        
        # Draw Pacman with shake offset
        pacman.draw(screen, shake_x, shake_y)
        
        # Draw ghosts with shake offset
        ghost_manager.draw(screen, shake_x, shake_y)
        
        # Draw particle effects
        _draw_particle_effects(screen, shake_x, shake_y)
        
        # Draw UI elements using UI manager (UI not affected by shake)
        remaining_dots = collectible_manager.get_remaining_dots()
        ui_manager.draw_game_ui(screen, score, lives, power_mode_active, power_mode_timer, remaining_dots, audio_manager.is_sound_enabled())
        
        # Draw performance info in debug mode (optional)
        _draw_debug_info(screen)
        
    elif game_state == GAME_OVER:
        # Draw game over screen using UI manager
        ui_manager.draw_game_over_screen(screen, score)
    elif game_state == VICTORY:
        # Draw victory screen using UI manager
        ui_manager.draw_victory_screen(screen, score)
        
    elif game_state == PAUSED:
        # Draw pause screen using UI manager
        ui_manager.draw_pause_screen(screen, score, lives)

def _draw_maze_walls(screen, shake_x=0, shake_y=0):
    """Draw only the maze walls, not the collectibles."""
    for y in range(maze.height):
        for x in range(maze.width):
            tile_type = maze.layout[y][x]
            world_x, world_y = grid_to_world(x, y)
            
            # Only draw walls
            if tile_type == WALL:
                # Use pygame zero's Rect class with shake offset
                from pygame import Rect
                screen.draw.filled_rect(
                    Rect(world_x + shake_x, world_y + shake_y, TILE_SIZE, TILE_SIZE),
                    WALL_COLOR
                )

def _draw_particle_effects(screen, shake_x=0, shake_y=0):
    """Draw all active particle effects."""
    for particle in particle_effects:
        particle.draw(screen, shake_x, shake_y)

def _draw_debug_info(screen):
    """Draw debug information (performance metrics, etc.)."""
    # Only show debug info if there are performance issues or in debug mode
    debug_mode = False  # Set to True for debugging
    
    if debug_mode:
        debug_y = SCREEN_HEIGHT - 80
        
        # FPS counter
        screen.draw.text(
            f"FPS: {current_fps:.1f}",
            topleft=(10, debug_y),
            fontsize=12,
            color="white"
        )
        
        # Particle count
        screen.draw.text(
            f"Particles: {len(particle_effects)}",
            topleft=(10, debug_y + 15),
            fontsize=12,
            color="white"
        )
        
        # Game state info
        screen.draw.text(
            f"State: {game_state} ({game_state_manager.get_state_time(game_state):.1f}s)",
            topleft=(10, debug_y + 30),
            fontsize=12,
            color="white"
        )
        
        # Entity positions (for debugging collision issues)
        pacman_pos = pacman.get_position()
        screen.draw.text(
            f"Pacman: {pacman_pos}",
            topleft=(10, debug_y + 45),
            fontsize=12,
            color="white"
        )

def _restart_game():
    """Restart the game to initial state with optimized reset."""
    global score, lives, power_mode_timer, power_mode_active, screen_flash_timer
    global screen_shake_timer, screen_shake_intensity, particle_effects
    
    # Reset game state using state manager
    game_state_manager.change_state(PLAYING)
    
    # Reset game variables
    score = 0
    lives = INITIAL_LIVES
    power_mode_timer = 0.0
    power_mode_active = False
    screen_flash_timer = 0.0
    
    # Reset visual effects
    screen_shake_timer = 0.0
    screen_shake_intensity = 0.0
    particle_effects.clear()  # Clear all particle effects
    
    # Play game start sound
    audio_manager.play_game_start()
    
    # Reset all game entities efficiently
    pacman.reset_position()
    pacman.state = PACMAN_NORMAL
    pacman.invincible = False
    pacman.invincibility_timer = 0.0
    
    collectible_manager.reset()
    ghost_manager.reset_all_ghosts()
    
    # Reset UI state
    ui_manager.update_high_score(0)  # This will only update if score is higher

def on_key_down(key):
    """Handle keyboard input with improved state management."""
    try:
        if game_state == PLAYING:
            _handle_playing_input(key)
        elif game_state in [GAME_OVER, VICTORY]:
            _handle_end_game_input(key)
        elif game_state == PAUSED:
            _handle_paused_input(key)
    except Exception as e:
        print(f"Error handling input: {e}")
        # Graceful error recovery - don't crash the game

def _handle_playing_input(key):
    """Handle input during playing state."""
    if key == keys.UP:
        pacman.move(UP)
    elif key == keys.DOWN:
        pacman.move(DOWN)
    elif key == keys.LEFT:
        pacman.move(LEFT)
    elif key == keys.RIGHT:
        pacman.move(RIGHT)
    elif key == keys.ESCAPE:
        game_state_manager.change_state(PAUSED)
    elif key == keys.M:
        sound_enabled = audio_manager.toggle_sounds()
        print(f"Sound effects {'enabled' if sound_enabled else 'disabled'}")

def _handle_end_game_input(key):
    """Handle input during game over or victory state."""
    if key == keys.R:
        _restart_game()
    elif key == keys.ESCAPE:
        import sys
        sys.exit()

def _handle_paused_input(key):
    """Handle input during paused state."""
    if key == keys.ESCAPE:
        game_state_manager.change_state(PLAYING)
    elif key == keys.R:
        _restart_game()

if __name__ == "__main__":
    pgzrun.go()