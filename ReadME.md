# Skyjo Game Simulator

## Overview

This project simulates the card game **Skyjo** for multiple players. It allows you to:
- Play a single game of Skyjo.
- Simulate multiple games (N games).
- Analyze player performance, including:
  - Win distribution
  - Average score per player
  - Score distribution per player

The results are visualized using **matplotlib** for better insights into the performance of each player over multiple games.

## Game Rules Summary

The objective of Skyjo is to minimize the points on your cards by the end of each round. The game continues until a player reaches 100 points or more. The player with the lowest score at the end of the game wins.

Each player starts with a 4x3 grid of cards (12 cards total), and only two cards are revealed at the beginning. Players take turns drawing and replacing cards to lower their score. A special rule applies if three vertical cards are the same, which removes the entire column.

## Features

- **Single Game Simulation**: Simulate one full game of Skyjo.
- **Multiple Game Simulation**: Simulate `N` games to gather statistics on:
  - Win distribution
  - Average score
  - Score distribution for each player
- **Visualization**: Visualize player performance using bar charts and histograms.

## How to Run

1. Install the necessary dependencies:
   ```bash
   pip install matplotlib
