# 🐦 Flappy Bird Game

A classic Flappy Bird game implementation in Python using Pygame with enhanced features and professional UI.

## Features

✨ **Game Features:**
- Smooth bird physics and controls
- Procedurally generated pipes
- Score tracking with high score persistence
- Sound effects for flapping, scoring, and collisions
- Game over screen with restart options
- Professional UI with large, readable score display

🎮 **Controls:**
- **ENTER** - Start the game
- **SPACE** - Flap (when game is active)
- **R** - Restart after game over
- **Mouse Click** - Click restart button
- **ESC/Close Window** - Quit game

## Installation

### Requirements
- Python 3.7+
- Pygame

### Setup

1. Clone this repository:
```bash
git clone https://github.com/Rajvardhan-Vajpai/Flappy-Bird.git
cd Flappy-Bird
```

2. Install dependencies:
```bash
pip install pygame
```

3. Run the game:
```bash
python Flappy_Bird.py
```

## Game Rules

- Navigate the bird through pipes without colliding
- Gain 1 point each time you successfully pass through a pipe
- Game ends when you hit a pipe or the ground
- Try to beat your high score!

## Project Structure

```
Flappy-Bird/
├── Flappy_Bird.py      # Main game file
├── bird.py             # Bird class
├── pipe.py             # Pipe class
├── assets/
│   ├── bg.png          # Game background
│   ├── ground.png      # Ground sprite
│   ├── birdup.png      # Bird sprite
│   ├── gameover.jpg    # Game over screen
│   ├── font.ttf        # Custom font
│   └── sfx/
│       ├── flap.wav    # Flap sound
│       ├── score.wav   # Score sound
│       └── dead.wav    # Collision sound
└── highscore.txt       # Stores the highest score
```

## Gameplay Tips

- Time your flaps carefully to avoid pipes
- The pipes have gaps you need to navigate through
- Each successful pipe pass earns you a point
- The game speed increases with your score
- Practice makes perfect!

## Sound Settings

- The sound loop stops after game over for a cleaner experience
- Score sound plays with minimal delay after passing a pipe
- Collision sound only plays once on impact

## Code Features

- Object-oriented design with Bird and Pipe classes
- Delta time-based movement for smooth animations
- Professional error handling for asset loading
- Persistent high score storage
- Clean event handling and game loop

## Future Enhancements

- [ ] Difficulty levels
- [ ] Different bird/pipe skins
- [ ] Leaderboard system
- [ ] Mobile touch controls
- [ ] Power-ups

## Author

**Rajvardhan-Vajpai**

## License

This project is open source and available under the MIT License.

## Feedback

If you have suggestions or found a bug, feel free to open an issue or create a pull request!

---

**Enjoy the game! 🎮** Try to beat your high score!
