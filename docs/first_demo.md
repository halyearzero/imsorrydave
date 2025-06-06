# First Demo Instructions

This demo showcases the initial prototype of **I'm Sorry, Dave**. You can explore the ship,
collect oxygen, read logs and try a short hacking puzzle. The adaptive AI will
react to some of your actions.

## Setup
1. Install Python 3.11 or newer.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Demo
Start the game with:
```bash
python main.py
```
The game will fall back to SDL's dummy drivers if no display or audio device is
found, so it can also run headless on a server.

## Controls
- **Arrow keys / WASD** – move the astronaut
- **Z** – toggle zero‑G movement
- **E** – interact with terminals or action nodes

Collect logs and oxygen canisters and keep an eye on your oxygen level in the
HUD. If you run out of air the game ends.
