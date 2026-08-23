import pygame

# --- ENGINE & DISPLAY ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 40 

# --- COLORS ---
BG_TOP = (15, 20, 30)
BG_BOTTOM = (40, 35, 60)
PLAYER_COLOR = (40, 200, 150)
PLAYER_DASH_COLOR = (150, 255, 200)
PLATFORM_COLOR = (60, 70, 90)
COIN_COLOR = (255, 215, 0)
ENEMY_RED = (240, 60, 60)
ENEMY_PURPLE = (170, 50, 220)
HAZARD_COLOR = (200, 200, 200)
SPRING_COLOR = (50, 255, 50)
GOAL_COLOR = (100, 200, 255)
TEXT_COLOR = (255, 255, 255)

# --- PHYSICS ---
GRAVITY = 1800
JUMP_STRENGTH = -650
SPRING_STRENGTH = -1200
ACCELERATION = 1600
FRICTION = -9
TERMINAL_VELOCITY = 1000
WALL_SLIDE_SPEED = 120
WALL_JUMP_X = 550
WALL_JUMP_Y = -600
DASH_SPEED = 1600

# --- LEVEL MAPS (10 Levels) ---
LEVEL_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "X                                      X",
    "X                                      X",
    "X                                      X",
    "X                                      X",
    "X                                      X",
    "X                                      X",
    "X                 2                    X",
    "X P     1         X        C       G   X",
    "XXXXX  XXXX     XXXXX      X     XXXXXXX",
    "X                                      X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_2 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "X                                      X",
    "X                           B          X",
    "X               B           B      G   X",
    "X               B   4       B   XXXXXXXX",
    "X       3       B XXXXX     B          X",
    "X P  BBBBBBB    B           B          X",
    "XXXXX           B           B          X",
    "X             XXX         XXX          X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_3 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "X                                      X",
    "X                                      X",
    "X                                      X",
    "X                        6         G   X",
    "X P       5              S       XXXXXXX",
    "XXXXX    XXXX     E     XXX            X",
    "X                XXXX                  X",
    "X^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_4 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "X                                      X",
    "X             B                        X",
    "X             B  L  M         L  G     X",
    "X             X                XXXXX   X",
    "X P                   C                X",
    "XXXXX   E            XXX               X",
    "X     XXXXX                            X",
    "X^^^^^XXXXX^^^^^^^^^^^^^^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_5 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "X                                      X",
    "X                                      X",
    "X                                      X",
    "X                L  M           L      X",
    "X      C     E  X                      X",
    "X P   XXX    C                         X",
    "XXXX        XXX                        X",
    "X                                  G   X",
    "X^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^XXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_6 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                           X",
    "X                                           X",
    "X                                           X",
    "X                    C                      X",
    "X                   XXX      B          G   X",
    "X                            B        XXXXXXX",
    "X                 U          B      X       X",
    "X P              XXX         B              X",
    "XXXXX                        B  X           X",
    "X          S                 BX             X",
    "X^^^^^^^^^^X^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_7 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                       C X            X",
    "X                       C X            X",
    "X                  E    C X            X",
    "X                XXXXXXXXXX            X",
    "X                                      X",
    "X                                      X",
    "X                                      X",
    "X       S                              X",
    "X       X                              X",
    "X                                      X",
    "X                                  G   X",
    "X P                               XXXXXX",
    "XXXXX      S            S              X",
    "X         XXX         XXXXX            X",
    "X^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_8 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "X                                      X",
    "X               B L        M         L X",
    "X               B                      X",
    "X               B       U              X",
    "X P         S   B     XXXXX        C   X",
    "XXXXX      XXX  B                  X   X",
    "X               B        G         X   X",
    "X^^^^^^^^^^^^^^^X^^^^^^XXXXXX^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_9 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "X   B       B       B       B          X",
    "X  BCB     BCB     BCB     BCB     G   X",
    "X   X       X       X       X      X   X",
    "X                                      X",
    "X      U       U       U       U       X",
    "X     XXX     XXX     XXX     XXX      X",
    "X                                      X",
    "X P                                    X",
    "XXXXX                                  X",
    "XXXXX^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_10 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                      X",
    "X                                   G  X",
    "X     L     M    L XX L     M   L XXXXXX",
    "XXXX                                   X",
    "X                                      X",
    "X P           U               U        X",
    "XXXXX        XXX             XXX       X",
    "X      S               S               X",
    "X^^^^^^X^^^^^^^^^^^^^^^X^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5, LEVEL_6, LEVEL_7, LEVEL_8, LEVEL_9, LEVEL_10]

TUTORIAL_MESSAGES = {
    "1": "A/D or Arrows to Move. SPACE/W to Jump. Double Jump in mid-air!",
    "2": "Jump against a wall, then press SPACE to Wall-Jump!",
    "3": "Jump into cracked blocks from below to shatter them!",
    "4": "Hold SHIFT to DASH! Dashing horizontally shatters blocks!",
    "5": "Jump on top of enemies to defeat them and bounce higher!",
    "6": "Springs launch you!"
}