"""
Audio System for Pacman Game
Handles all sound effects and audio feedback using pygame.
"""

import pygame
import os

class PygameZeroAudioManager:
    """Audio manager that actually plays sounds."""
    
    def __init__(self):
        self.sounds_enabled = True
        self.sounds = {}
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            print("Audio system initialized")
        except pygame.error as e:
            print(f"Could not initialize audio: {e}")
            self.sounds_enabled = False
            return
        
        # Try to load sound files, create fallback sounds if files don't exist
        self._load_or_create_sounds()
    
    def _load_or_create_sounds(self):
        """Load sound files or create simple beep sounds as fallback."""
        sound_files = {
            'dot_collect': 'dot_collect.wav',
            'power_pellet': 'power_pellet.wav',
            'ghost_eat': 'ghost_eat.wav',
            'pacman_death': 'pacman_death.wav',
            'game_start': 'game_start.wav',
            'victory': 'victory.wav',
            'game_over': 'game_over.wav'
        }
        
        sounds_dir = 'assets/sounds'
        
        for sound_name, filename in sound_files.items():
            sound_path = os.path.join(sounds_dir, filename)
            
            if os.path.exists(sound_path):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                    print(f"Loaded sound: {filename}")
                except pygame.error:
                    self.sounds[sound_name] = self._create_beep_sound(sound_name)
            else:
                # Create a simple beep sound as fallback
                self.sounds[sound_name] = self._create_beep_sound(sound_name)
    
    def _create_beep_sound(self, sound_name):
        """Create a simple beep sound for the given sound type."""
        try:
            import numpy as np
            
            # Different frequencies for different sound types
            frequency_map = {
                'dot_collect': 800,      # High pitch for dots
                'power_pellet': 400,     # Lower pitch for power pellets  
                'ghost_eat': 1200,       # Very high pitch for eating ghosts
                'pacman_death': 200,     # Low pitch for death
                'game_start': 600,       # Medium pitch for game start
                'victory': 1000,         # High pitch for victory
                'game_over': 150         # Very low pitch for game over
            }
            
            frequency = frequency_map.get(sound_name, 500)
            duration = 0.15  # 150ms duration
            sample_rate = 22050
            
            # Generate sine wave
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave = np.sin(2 * np.pi * frequency * t)
            
            # Add envelope to avoid clicks
            fade_frames = int(0.01 * sample_rate)  # 10ms fade
            wave[:fade_frames] *= np.linspace(0, 1, fade_frames)
            wave[-fade_frames:] *= np.linspace(1, 0, fade_frames)
            
            # Convert to 16-bit integers and make stereo
            wave = (wave * 32767).astype(np.int16)
            stereo_wave = np.column_stack((wave, wave))
            
            # Ensure the array is C-contiguous
            stereo_wave = np.ascontiguousarray(stereo_wave)
            
            return pygame.sndarray.make_sound(stereo_wave)
            
        except ImportError:
            # Fallback without numpy - create simple square wave
            frequency = frequency_map.get(sound_name, 500)
            duration = 0.15
            sample_rate = 22050
            frames = int(duration * sample_rate)
            
            # Simple square wave
            arr = []
            for i in range(frames):
                value = 8000 if (i % (sample_rate // frequency)) < (sample_rate // frequency) // 2 else -8000
                arr.extend([value, value])  # Stereo
            
            return pygame.sndarray.make_sound(pygame.array.array('h', arr))
    
    def play_sound(self, sound_name):
        """Play a sound effect."""
        if not self.sounds_enabled or sound_name not in self.sounds:
            return
        
        try:
            self.sounds[sound_name].play()
        except pygame.error as e:
            print(f"Error playing sound {sound_name}: {e}")
    
    def play_dot_collect(self):
        """Play sound for collecting a dot."""
        self.play_sound('dot_collect')
    
    def play_power_pellet(self):
        """Play sound for collecting a power pellet."""
        self.play_sound('power_pellet')
    
    def play_ghost_eat(self):
        """Play sound for eating a ghost."""
        self.play_sound('ghost_eat')
    
    def play_pacman_death(self):
        """Play sound for Pacman dying."""
        self.play_sound('pacman_death')
    
    def play_game_start(self):
        """Play sound for game starting."""
        self.play_sound('game_start')
    
    def play_victory(self):
        """Play sound for victory."""
        self.play_sound('victory')
    
    def play_game_over(self):
        """Play sound for game over."""
        self.play_sound('game_over')
    
    def toggle_sounds(self):
        """Toggle sound effects on/off."""
        self.sounds_enabled = not self.sounds_enabled
        return self.sounds_enabled
    
    def is_sound_enabled(self):
        """Check if sounds are enabled."""
        return self.sounds_enabled
    
    def set_volume(self, volume):
        """Set volume for all sounds (0.0 to 1.0)."""
        for sound in self.sounds.values():
            sound.set_volume(volume)