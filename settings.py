import pygame

# --- ENGINE & DISPLAY ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 40 
BG_TOP = (15, 15, 25)
BG_BOTTOM = (40, 40, 60)

# --- COLORS ---
PLAYER_COLOR = (50, 205, 50)
PLAYER_DASH_COLOR = (100, 255, 100)
PLATFORM_COLOR = (120, 130, 160)
COIN_COLOR = (255, 215, 0)
ENEMY_COLOR = (220, 50, 50)
HAZARD_COLOR = (255, 60, 60)
GOAL_COLOR = (150, 50, 255)
TEXT_COLOR = (255, 255, 255)

# --- PHYSICS ---
GRAVITY = 1800
JUMP_STRENGTH = -650
ACCELERATION = 1500
FRICTION = -8
TERMINAL_VELOCITY = 1000
WALL_SLIDE_SPEED = 150
WALL_JUMP_X = 500
WALL_JUMP_Y = -600

# --- LEVEL MAPS ---
LEVEL_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "X                                      X",
    "X     C   C                  G         X",
    "X    XXX BXX                 X         X",
    "X                                      X",
    "X P              E                     X",
    "XXXXX   XXXXXXXXXXXXXXXX   XXXXXXXXXXXXX",
    "X                                      X",
    "X                                      X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_2 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "X                  C   C     G         X",
    "X   X     M       XXX XXX  XXXXX       X",
    "X                                      X",
    "X                                      X",
    "X P          E        E          ^     X",
    "XXXXX   XXXXXX   XXXXXX   XXXXXXXXXXXXXX",
    "X                         X            X",
    "X             ^^^         X            X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_3 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "X C                       ^C^C^        X",
    "XXXX                     XXXXXXX       X",
    "X                M                     X",
    "X       ^^  X    C      ^ ^            X",
    "X P    XXXXX   E C     XXXXX    C      X",
    "XXXX           XXXXX            X      X",
    "X                               X  G   X",
    "X   E      E      E   ^^^C^^^   X^^X^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_4 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "X       M        C   C                 X",
    "X     XXXXX     XXX XXX     M          X",
    "X                          XXX         X",
    "X           E                   X  G   X",
    "X P        XXXX                 XXXXXXXX",
    "XXXXX                           X      X",
    "X      ^^           ^^^         X      X",
    "X    XXXXXXX      XXXXXXX       X      X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_5 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X   C   C                              X",
    "X  XXX XXX                             X",
    "X               M          M           X",
    "X             XXXXX      XXXXX         X",
    "X     ^                            G   X",
    "X P  XXX   E         E         E  XXX  X",
    "XXXX      XXX       XXX       XXX      X",
    "X          X         X         X       X",
    "X       ^^^^^^^^^^^^^^^^^^^^^^^^^      X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5]