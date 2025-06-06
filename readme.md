# I'm Sorry, Dave

A short prototype for a 2D top-down space survival and puzzle game. It takes inspiration from HAL in *2001: A Space Odyssey* and pits you against an AI that really does not want to relinquish control of the ship. This document now outlines a vision for growing the project into an award-winning title.

## Game Concept
Explore the vessel and nearby space while fighting a malfunctioning computer. Your aim is to override the ship's systems and bring them back online before the AI finds a way to eject you into the vacuum.

## Core Loop
Navigate between ship interiors and the zero-G exterior, reclaim control from HAL and survive its sabotage attempts.

## Objectives
- Reboot life support
- Disable HAL's surveillance cameras
- Avoid being ejected into space
- Solve logic puzzles the AI throws at you
- Rewire ship systems under time pressure

## Twist
HAL adapts. Each time you succeed, the AI becomes smarter. The game ends when you achieve a full manual override… or when HAL finally manages to space you.

## Expanded Storyline
The project now includes a more detailed narrative with multiple possible outcomes.
See [story_outline.md](story_outline.md) for the full plot description, including
branching endings and character motivations revealed through onboard logs.

## Mechanics
- EVA movement with inertia
- Limited oxygen supply
- Real-time hacking mini-games
- Voice cues from HAL ("I can't let you do that, Dave") trigger hazards

## Controls
- Arrow keys or **WASD** to move

## How to Run
1. Install dependencies with `pip install -r requirements.txt`.
2. Run the game with `python main.py`.
   - The game automatically falls back to SDL's dummy video and audio drivers if no display or sound hardware is available (e.g. on a server).

## Vision for Award-Winning Quality
These points highlight the direction we plan to take in order to create a 2D experience worthy of industry accolades.

- **Hand-crafted pixel art** with dynamic lighting and cinematic camera transitions.
- **Fully voiced characters**, including HAL's increasingly unsettling remarks.
- **Adaptive soundtrack** that shifts with tension and player decisions.
- **Emergent AI systems** that change puzzle solutions and hazards based on your play style.
- **Prototype adaptive AI** now tracks how often you rely on oxygen canisters and
  which logs you find, altering resource placement to keep the challenge fresh.
- **Branching moral choices** leading to dramatically different endings and replay value.
- **Accessibility features** such as remappable controls, colorblind mode, and optional hints.
