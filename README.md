# Tic-Tac-Toe AI

A Python-based AI to play Tic-Tac-Toe against.  
A full documentation of the code and its features can be found in [Documentation.pdf](https://github.com/valentin-s1/tictactoe/blob/main/Documentation.pdf).  
This repository serves as the **submission of the mandatory group project for course "3,793 | Skills: Programming - Introduction Level" taught by Dr. Mario Silic at the University of St. Gallen in the fall semester of 2024.**

## Description

The code features both a graphical and a logical implementation of the well-known game of Tic-Tac-Toe. It is split between [runner.py](https://github.com/valentin-s1/tictactoe/blob/main/runner.py) and [tictactoe.py](https://github.com/valentin-s1/tictactoe/blob/main/tictactoe.py) where the former is responsible for 
 * handling the graphical interface
* running the game 
* and moving the game forward,  
  
while the latter supplies  
* the logical functions required to play 
* and the AI's decision-making algorithm.

The user can choose which symbol to play as (X or O) and X always goes first. 

Furthermore, the AI's decision-making process is based on the [Minimax](https://en.wikipedia.org/wiki/Minimax) algorithm.

## Prerequisites

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [pygame](https://www.pygame.org/).

```bash
pip install pygame
```

Clone this repository onto your local drive with [git](https://git-scm.com/).

```bash
git clone https://github.com/valentin-s1/tictactoe
```

Please note that a version of [Calibri](https://github.com/valentin-s1/tictactoe/blob/main/calibri.ttf) is included to render the text.
## Usage

To run the game, simply navigate to the folder containing the source code and execute [runner.py](https://github.com/valentin-s1/tictactoe/blob/main/runner.py).

``` bash
cd .../tictactoe 
python runner.py
```

Consequently, a game window opens where the user can click the corresponding buttons and tiles to play the game. 
## Authors

Valentin Schnellmann, Marco Broger

