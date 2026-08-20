import pygame

# --- ENGINE & DISPLAY ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 40 
BG_COLOR = (25, 25, 35)

# --- COLORS ---
PLAYER_COLOR = (50, 205, 50)
PLATFORM_COLOR = (150, 150, 170)
COIN_COLOR = (255, 215, 0)
ENEMY_COLOR = (220, 50, 50)
HAZARD_COLOR = (200, 100, 0)
GOAL_COLOR = (150, 50, 255)
TEXT_COLOR = (255, 255, 255)

# --- PHYSICS (Scaled for Delta Time in Seconds) ---
GRAVITY = 1800
JUMP_STRENGTH = -700
ACCELERATION = 1500
FRICTION = -8
TERMINAL_VELOCITY = 1000
WALL_SLIDE_SPEED = 200
WALL_JUMP_X = 500
WALL_JUMP_Y = -600

# --- LEVEL PARSER DATA ---
# P = Player Spawn, X = Platform, B = Breakable, M = Moving Platform
# C = Coin, E = Enemy, ^ = Spikes, F = Checkpoint Flag, G = Goal/Level End
LEVEL_MAP = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "X      C   C   C             G         X",
    "X     XXXBXXXBXXX          XXXXX       X",
    "X                      M               X",
    "X                                      X",
    "X P              E            C  ^     X",
    "XXXXX   XXXXXXXXXXXXXXXX   XXXXXXXXXXXXX",
    "X                                      X",
    "X              ^^          E           X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]