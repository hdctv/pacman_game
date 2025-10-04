"""
UI System for Pacman Game
Handles all user interface elements including score, lives, and game state displays.
"""

from constants import *

class UIManager:
    """Manages all UI elements and displays for the game."""
    
    def __init__(self):
        self.font_size_large = 24
        self.font_size_medium = 20
        self.font_size_small = 16
        
        # UI positioning
        self.score_pos = (10, 10)
        self.lives_pos = (10, 40)
        self.power_mode_pos = (10, 70)
        self.dots_remaining_pos = (10, 100)
        
        # High score tracking (could be expanded to save to file)
        self.high_score = 0
        
    def update_high_score(self, current_score):
        """Update high score if current score is higher."""
        if current_score > self.high_score:
            self.high_score = current_score
    
    def draw_game_ui(self, screen, score, lives, power_mode_active, power_mode_timer, remaining_dots, sound_enabled=True):
        """Draw the main game UI elements during gameplay."""
        # Score display with enhanced formatting
        screen.draw.text(
            f"SCORE: {score:,}", 
            topleft=self.score_pos, 
            fontsize=self.font_size_medium, 
            color="white"
        )
        
        # High score display
        if self.high_score > 0:
            screen.draw.text(
                f"HIGH: {self.high_score:,}", 
                topleft=(10, self.score_pos[1] + 25), 
                fontsize=self.font_size_small, 
                color="yellow"
            )
            # Adjust other UI elements down if high score is shown
            lives_y = self.lives_pos[1] + 20
        else:
            lives_y = self.lives_pos[1]
        
        # Lives display with visual representation
        self._draw_lives_display(screen, lives, (10, lives_y))
        
        # Power mode indicator with enhanced visual feedback
        if power_mode_active:
            self._draw_power_mode_indicator(screen, power_mode_timer, (10, lives_y + 30))
            dots_y = lives_y + 60
        else:
            dots_y = lives_y + 30
        
        # Remaining dots counter
        screen.draw.text(
            f"DOTS LEFT: {remaining_dots}", 
            topleft=(10, dots_y), 
            fontsize=self.font_size_small, 
            color="cyan"
        )
        
        # Level indicator (could be expanded for multiple levels)
        screen.draw.text(
            "LEVEL 1", 
            topleft=(SCREEN_WIDTH - 80, 10), 
            fontsize=self.font_size_small, 
            color="white"
        )
        
        # Sound status indicator
        sound_status = "ON" if sound_enabled else "OFF"
        sound_color = "green" if sound_enabled else "red"
        screen.draw.text(
            f"SOUND: {sound_status}", 
            topleft=(SCREEN_WIDTH - 100, 35), 
            fontsize=self.font_size_small, 
            color=sound_color
        )
        
        # Controls hint
        screen.draw.text(
            "ESC: Pause | M: Sound", 
            topleft=(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 25), 
            fontsize=12, 
            color="gray"
        )
    
    def _draw_lives_display(self, screen, lives, pos):
        """Draw lives with both text and visual representation."""
        # Text display
        screen.draw.text(
            f"LIVES: {lives}", 
            topleft=pos, 
            fontsize=self.font_size_medium, 
            color="white"
        )
        
        # Visual representation - small Pacman icons
        for i in range(lives):
            life_x = pos[0] + 80 + (i * 25)
            life_y = pos[1] + 2
            # Draw small Pacman representation as a circle
            screen.draw.filled_circle((life_x, life_y + 8), 8, PACMAN_COLOR)
            # Draw mouth (simple triangle cutout effect with black)
            screen.draw.filled_circle((life_x + 3, life_y + 8), 6, "black")
    
    def _draw_power_mode_indicator(self, screen, power_mode_timer, pos):
        """Draw power mode indicator with dynamic visual effects."""
        # Calculate flash intensity based on remaining time
        if power_mode_timer > 3.0:
            color = "yellow"
            bg_color = None
        else:
            # Flash red when time is running out
            flash_timer = power_mode_timer * 5  # Faster flashing as time runs out
            if int(flash_timer) % 2 == 0:
                color = "red"
                bg_color = "darkred"
            else:
                color = "yellow"
                bg_color = "orange"
        
        # Draw background highlight if flashing
        if bg_color:
            from pygame import Rect
            text_rect = Rect(pos[0] - 5, pos[1] - 2, 200, 22)
            screen.draw.filled_rect(text_rect, bg_color)
        
        # Draw power mode text
        screen.draw.text(
            f"POWER MODE: {power_mode_timer:.1f}s", 
            topleft=pos, 
            fontsize=self.font_size_small, 
            color=color
        )
    
    def draw_game_over_screen(self, screen, final_score):
        """Draw the game over screen with enhanced styling."""
        # Update high score
        self.update_high_score(final_score)
        
        # Dark overlay with transparency effect
        screen.fill((0, 0, 0))
        
        # Main game over text with shadow effect
        shadow_offset = 3
        screen.draw.text(
            "GAME OVER", 
            center=(SCREEN_WIDTH//2 + shadow_offset, SCREEN_HEIGHT//2 - 40 + shadow_offset), 
            fontsize=40, 
            color="darkred"
        )
        screen.draw.text(
            "GAME OVER", 
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40), 
            fontsize=40, 
            color="red"
        )
        
        # Score information
        screen.draw.text(
            f"FINAL SCORE: {final_score:,}", 
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 
            fontsize=24, 
            color="white"
        )
        
        # High score display
        if self.high_score > 0:
            if final_score == self.high_score:
                screen.draw.text(
                    "NEW HIGH SCORE!", 
                    center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30), 
                    fontsize=20, 
                    color="gold"
                )
            else:
                screen.draw.text(
                    f"HIGH SCORE: {self.high_score:,}", 
                    center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30), 
                    fontsize=18, 
                    color="yellow"
                )
        
        # Instructions
        screen.draw.text(
            "Press R to restart", 
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60), 
            fontsize=20, 
            color="yellow"
        )
        screen.draw.text(
            "Press ESC to quit", 
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 90), 
            fontsize=16, 
            color="gray"
        )
    
    def draw_victory_screen(self, screen, final_score):
        """Draw the victory screen with celebration effects."""
        # Update high score
        self.update_high_score(final_score)
        
        # Dark overlay
        screen.fill((0, 0, 0))
        
        # Victory text with shadow effect
        shadow_offset = 3
        screen.draw.text(
            "VICTORY!", 
            center=(SCREEN_WIDTH//2 + shadow_offset, SCREEN_HEIGHT//2 - 40 + shadow_offset), 
            fontsize=40, 
            color="darkgoldenrod"
        )
        screen.draw.text(
            "VICTORY!", 
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40), 
            fontsize=40, 
            color="gold"
        )
        
        # Completion message
        screen.draw.text(
            "All dots collected!", 
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 10), 
            fontsize=20, 
            color="white"
        )
        
        # Score information
        screen.draw.text(
            f"FINAL SCORE: {final_score:,}", 
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20), 
            fontsize=24, 
            color="white"
        )
        
        # High score display
        if self.high_score > 0:
            if final_score == self.high_score:
                screen.draw.text(
                    "NEW HIGH SCORE!", 
                    center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50), 
                    fontsize=20, 
                    color="gold"
                )
            else:
                screen.draw.text(
                    f"HIGH SCORE: {self.high_score:,}", 
                    center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50), 
                    fontsize=18, 
                    color="yellow"
                )
        
        # Instructions
        screen.draw.text(
            "Press R to restart", 
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80), 
            fontsize=20, 
            color="yellow"
        )
        screen.draw.text(
            "Press ESC to quit", 
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 110), 
            fontsize=16, 
            color="gray"
        )
    
    def draw_pause_screen(self, screen, current_score, current_lives):
        """Draw the pause screen with current game state."""
        # Dark overlay
        screen.fill((20, 20, 20))
        
        # Pause text
        screen.draw.text(
            "PAUSED", 
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20), 
            fontsize=40, 
            color="white"
        )
        
        # Current game state
        screen.draw.text(
            f"SCORE: {current_score:,}", 
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20), 
            fontsize=20, 
            color="white"
        )
        screen.draw.text(
            f"LIVES: {current_lives}", 
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50), 
            fontsize=20, 
            color="white"
        )
        
        # Instructions
        screen.draw.text(
            "Press ESC to resume", 
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 90), 
            fontsize=20, 
            color="yellow"
        )
        screen.draw.text(
            "Press R to restart", 
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120), 
            fontsize=16, 
            color="gray"
        )