# ⚔️ Knightfall

A 2D side-scrolling combat game built with Python and Pygame. Take control of a knight and battle endless waves of bandits — block, attack, heal, and see how far you can push your streak.

## 🎮 Gameplay

Face off against increasingly difficult waves of bandits. Each wave brings more enemies with higher health and strength. Survive as long as you can, manage your potions wisely, and try to beat your personal best wave count.

## 🕹️ Controls

| Key | Action |
|-----|--------|
| `A` / `←` | Move left |
| `D` / `→` | Move right |
| `SPACE` | Attack |
| `S` | Block |
| `H` | Heal (uses a potion) |
| `P` | Pause / Resume |
| `R` | Restart (after defeat) |
| `ESC` | Quit |

## ✨ Features

- Wave-based survival combat with scaling difficulty
- Enemy AI that chases, attacks, blocks, retreats, and heals based on health thresholds
- Sprite-based animations (idle, attack, hurt, death) for both the knight and bandits
- Sound effects for attacks, impacts, blocks, and enemy deaths
- Persistent high score tracking (best wave saved locally)

## 🛠️ Requirements

- Python 3.8+
- [Pygame](https://www.pygame.org/)

## 📦 Installation

1. Clone the repository:

   git clone https://github.com/gautham-marihal/knightfall-game.git
   cd knightfall-game

2. Install dependencies:

   pip install pygame

3. Run the game:

   python knightfall_game.py

## 📁 Project Structure

    knightfall-game/
    ├── img/
    │   ├── Background/
    │   ├── Bandit/
    │   │   ├── Idle/
    │   │   ├── Attack/
    │   │   ├── Hurt/
    │   │   └── Death/
    │   ├── Knight/
    │   │   ├── Idle/
    │   │   ├── Attack/
    │   │   ├── Hurt/
    │   │   └── Death/
    │   └── Icons/
    ├── sounds/
    ├── knightfall_game.py
    └── README.md

## 🏆 High Score

Your best wave is automatically saved to `Highestscore.txt` and loaded each time you start the game.

## 📝 License

This project is open source and available for personal and educational use.
