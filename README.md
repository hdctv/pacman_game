# Pacman Game

A classic Pacman game implementation built with Python and Pygame Zero, featuring smooth animations, particle effects, and intelligent ghost AI.

## Features

### Core Gameplay
- **Classic Pacman mechanics**: Navigate the maze, collect dots, and avoid ghosts
- **Power pellets**: Temporarily make ghosts vulnerable and earn bonus points
- **Multiple lives system**: Start with 3 lives, lose one when caught by a ghost
- **Score system**: Earn points for dots (10), power pellets (50), and eating ghosts (200)
- **Victory condition**: Collect all dots to win the level

### Visual Polish
- **Smooth animations**: Pacman mouth animation that opens and closes while moving
- **Ghost animations**: Floating ghosts with directional eyes and wavy bottom edges
- **Particle effects**: Visual feedback for collecting items and eating ghosts
- **Screen effects**: Screen shake for dramatic moments and flash effects
- **Enhanced UI**: Score display, lives counter, power mode indicator, and game state screens

### AI and Gameplay
- **Intelligent ghost AI**: Ghosts switch between scatter, chase, and vulnerable modes
- **Pathfinding**: Ghosts use smart pathfinding to navigate toward targets
- **Collision detection**: Precise collision system for smooth gameplay
- **Power mode**: Ghosts become vulnerable and flee when Pacman eats a power pellet
- **Invincibility system**: Brief invincibility after respawning

### Audio System
- **Sound effects**: Audio feedback for all major game events
- **Toggle controls**: Press 'M' to enable/disable sound effects
- **Event-driven audio**: Different sounds for collecting dots, power pellets, eating ghosts, death, and victory

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pacman-game
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install pgzero pygame
   ```

## How to Play

### Running the Game
```bash
cd pacman_game
pgzrun main.py
```

### Controls
- **Arrow Keys**: Move Pacman (Up, Down, Left, Right)
- **ESC**: Pause/Resume game or quit from game over screen
- **M**: Toggle sound effects on/off
- **R**: Restart game (from game over or victory screen)

### Gameplay
1. **Objective**: Collect all dots in the maze while avoiding ghosts
2. **Power Pellets**: Large white dots that make ghosts vulnerable for 10 seconds
3. **Scoring**:
   - Small dots: 10 points each
   - Power pellets: 50 points each
   - Eating vulnerable ghosts: 200 points each
4. **Lives**: You start with 3 lives. Lose a life when caught by a non-vulnerable ghost
5. **Victory**: Collect all dots to complete the level
6. **Game Over**: Lose all lives to end the game

### Ghost Behavior
- **Red Ghost**: Aggressive chaser, directly targets Pacman
- **Pink Ghost**: Ambush behavior, tries to get ahead of Pacman
- **Cyan Ghost**: Patrol behavior, covers maze areas
- **Orange Ghost**: Mixed behavior, switches between chase and scatter

## Project Structure

```
pacman_game/
├── main.py                 # Main game loop and entry point
├── constants.py           # Game constants and configuration
├── maze.py               # Maze generation and collision detection
├── audio.py              # Audio system management
├── ui.py                 # User interface and screen management
├── entities/
│   ├── pacman.py         # Pacman player entity
│   ├── ghost.py          # Ghost AI and behavior
│   └── collectibles.py   # Dots and power pellets
└── assets/
    ├── images/           # Sprite assets (fallback rendering used)
    └── sounds/           # Audio files
```

## Technical Features

### Performance Optimizations
- **Efficient collision detection**: Optimized spatial collision checking
- **Particle system**: Memory-managed particle effects (max 50 particles)
- **State management**: Clean game state transitions and timing
- **FPS monitoring**: Built-in performance metrics (debug mode)

### Code Architecture
- **Entity-component system**: Modular entity design for easy extension
- **State machine**: Proper game state management (Playing, Paused, Game Over, Victory)
- **Event-driven audio**: Centralized audio management system
- **Fallback rendering**: Works without sprite assets using shape-based graphics

## Development

### Built With
- **Python 3.11+**: Core programming language
- **Pygame Zero**: Game development framework
- **Pygame**: Underlying graphics and audio library

### Key Design Patterns
- **State Machine**: Game state management
- **Observer Pattern**: Event-driven audio system
- **Component System**: Modular entity architecture
- **Strategy Pattern**: Different ghost AI behaviors

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Inspired by the classic Pacman arcade game by Namco
- Built using the excellent Pygame Zero framework
- Sound effects and game mechanics based on the original Pacman design

## Troubleshooting

### Common Issues

**Game won't start:**
- Ensure Python 3.7+ is installed
- Install required dependencies: `pip install pgzero pygame`
- Run from the correct directory: `cd pacman_game && pgzrun main.py`

**No sound:**
- Check that your system audio is working
- Press 'M' in-game to toggle sound effects
- Ensure pygame audio system is properly initialized

**Performance issues:**
- The game is optimized for 60 FPS
- Reduce particle effects by modifying `MAX_PARTICLES` in constants.py
- Enable debug mode to monitor performance metrics

**Controls not responding:**
- Ensure the game window has focus
- Check that no other applications are intercepting key events
- Try restarting the game

## Future Enhancements

- Multiple levels with increasing difficulty
- High score persistence
- Additional power-ups and game mechanics
- Sprite-based graphics with custom artwork
- Multiplayer support
- Level editor for custom mazes

---

Enjoy playing Pacman! 🟡👻