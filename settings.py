# settings.py
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 40 # was 32, looked too small

BG_TOP = (15, 20, 30)
BG_BOTTOM = (40, 35, 60)

# entity colors
PLAYER_COLOR = (40, 200, 150)
PLAYER_DASH_COLOR = (150, 255, 200)
PLATFORM_COLOR = (60, 70, 90)
COIN_COLOR = (255, 215, 0)
ORB_COLOR = (50, 255, 255)
ENEMY_RED = (240, 60, 60)
ENEMY_PURPLE = (170, 50, 220)
ENEMY_FLYER = (50, 200, 220) 
HAZARD_COLOR = (200, 200, 200)
SPRING_COLOR = (50, 255, 50)
GOAL_COLOR = (100, 200, 255)
TEXT_COLOR = (255, 255, 255)

# physics values
GRAVITY = 1800 # 1500 was too floaty
JUMP_STRENGTH = -650
SPRING_STRENGTH = -1200
ACCELERATION = 1600
FRICTION = -9
TERMINAL_VELOCITY = 1000
WALL_SLIDE_SPEED = 120
WALL_JUMP_X = 550
WALL_JUMP_Y = -600
DASH_SPEED = 1600

LEVEL_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                           X",
    "X                                           X",
    "X                                         G X",
    "X                                       XXXXX",
    "X                                           X",
    "X                 2                         X",
    "X P     1         X        C            X   X",
    "XXXXX  XXXX     XXXXX      X          XXX   X",
    "X                                           X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_2 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                              X",
    "X                                  G           X",
    "X                                XXXXXXXX      X",
    "X                                              X",
    "X                4                             X",
    "X              XXXXX  B                        X",
    "X                     B     C                  X",
    "X        3            B   XXXXX   B  C         X",
    "X P   BBBBBB          B           B XXX        X",
    "XXXXX                 B           B            X",
    "X                   XXX         XXX            X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_3 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                              X",
    "X                                              X",
    "X                                              X",
    "X                                              X",
    "X                                              X",
    "X                                              X",
    "X                                              X",
    "X                                              X",
    "X                                         G    X",
    "X                 6                    XXXXXXXXX",
    "X                 O       7                    X",
    "X P       5               S                    X",
    "XXXXX    XXXX           XXXXX                  X",
    "X                                S             X",
    "X                                X             X",
    "X^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^X^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_4 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X              B                                  X",
    "X              B                                  X",
    "X              B                                  X",
    "X              B                                  X",
    "X              B                                  X",
    "X              B                                  X",
    "X              B                                  X",
    "X              B                                  X",
    "X              B                                  X",
    "X              B                                  X",
    "X              B                   S              X",
    "X              B   C              XXX          G  X",
    "X P            B  XXX                        XXXXXX",
    "XXXXX          B          B                       X",
    "X              B          B                       X",
    "X            XXX          B             S         X",
    "X^^^^^^^^^^^^XXX^^^^^^^^^^X^^^^^^^^^^^^XXX^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_5 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                               X",
    "X                                               X",
    "X                                               X",
    "X                                               X",
    "X                                               X",
    "X                  F                   G        X",
    "X                                      X        X",
    "X        C                     C                X",
    "X P     XXX          E        XXX               X",
    "XXXXX               XXXX                        X",
    "X                                               X",
    "X^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_6 = [
    "XXXXXXXXXXXXX",
    "X           X",
    "X           X",
    "X           X",
    "X           X",
    "X           X",
    "X     G     X",
    "X    XXX    X",
    "X           X",
    "X           X",
    "X           X",
    "X        S  X",
    "X        X  X",
    "X           X",
    "X           X",
    "X           X",
    "X           X",
    "X S         X",
    "X X         X",
    "X           X",
    "X           X",
    "X       S   X",
    "X       X   X",
    "X           X",
    "X           X",
    "X   S       X",
    "X   X       X",
    "X P         X",
    "XXXXX       X",
    "XXXXXXXXXXXXX",
]

LEVEL_7 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                               X",
    "X                                               X",
    "X                                               X",
    "X                                               X",
    "X                        C                      X",
    "X       L     M        L X L       M          L X",
    "X      X                                        X",
    "X                                               X",
    "X    X                                     G    X",
    "X P                                       XXXXX X",
    "XXXXX                                           X",
    "X^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_8 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                        B               X",
    "X                        B               X",
    "X                C       B               X",
    "X               XXX      B               X",
    "X    XXXXX               B    O          X",
    "X    X                   B               X",
    "X    X                   B               X",
    "X    X         F         B          G    X",
    "X P  X      XXXXXX       B        XXXXX  X",
    "XXXXXX^^^^^^XXXXXX^^^^^^^X               X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXX^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_9 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                              X",
    "X                                              X",
    "X                                              X",
    "X                                              X",
    "X                                              X",
    "X                                        G     X",
    "X                 U          C           X     X",
    "X               XXXXX       XXX                X",
    "X P                               U            X",
    "XXXXX                            XXXX          X",
    "X           E                                  X",
    "X^^^^^^^^^XXXXX^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_10 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                  B                            X",
    "X                  B                            X",
    "X                  B                            X",
    "X                  B                            X",
    "X                  B                            X",
    "X                  B                            X",
    "X                  B                            X",
    "X                  B            F               X",
    "X     F            B                            X",
    "X                  B    O                       X",
    "X                  B         S        G         X",
    "X P      S         B        XXX      XXXX       X",
    "XXXX    XXX        B                            X",
    "X                  B                            X",
    "X^^^^^^^^^^^^^^^^^^X^^^^^^^^^^^^^^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_11 = [
    "XXXXXXXXXXXXXXXXXXXXXX",
    "X                   CX",
    "X                   CX",
    "X           OF      XX",
    "X P                  X",
    "XXXX       ^^^^^^^^^^X",
    "X          XXXXXXXXXXX",
    "X       E            X",
    "XXXXXXXXXXXXXXXXX    X",
    "X                    X",
    "X              E     X",
    "X   XXXXXXXXXXXXXXXXXX",
    "X                    X",
    "X                    X",
    "X       E            X",
    "XXXXXXXXXXXXXXXX     X",
    "X                    X",
    "X       E      E     X",
    "X   XXXXXXXXXXXXXXXXXX",
    "X          F         X",
    "X   G                X",
    "X XXXXXX             X",
    "X^^^^^^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_12 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                                   X",
    "X                                                   X",
    "X                                                   X",
    "X                                                   X",
    "X                                                   X",
    "X             F           F           F             X",
    "X                                                   X",
    "X                                                   X",
    "X       F         F         F       F         F     X",
    "X                                                   X",
    "X                O          O        O              X",
    "X           S         S          S        S       G X",
    "X P        XXX       XXX        XXX      XXX     XXXX",
    "XXXXX                                               X",
    "X^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_13 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                                     X",
    "X                                                     X",
    "X                  F                        F         X",
    "X                                                     X",
    "X                                                     X",
    "X      L     M      L  C L        M            L      X",
    "X P                   XXX                             X",
    "XXXXX                                              G  X",
    "X                                                XXXX X",
    "X^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_14 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                      B                            X",
    "X                      B                            X",
    "X                      B               F            X",
    "X                      B                            X",
    "X            U         B     C                      X",
    "X          XXXXX       B    XXX                     X",
    "X                      B                            X",
    "X                      B                            X",
    "X          F           B               F        G   X",
    "X                      B               E      XXXXX X",
    "X P      E             B              XXX           X",
    "XXXXX   XXXX           B    XXX                     X",
    "X                      B                            X",
    "X^^^^^^^^^^^^^^^^^^^^^^X^^^^^^^^^^^^^^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVEL_15 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X                                X",
    "X                                X",
    "X                                X",
    "X                                X",
    "X                                X",
    "X                                X",
    "X        C           C           X",
    "X       XXX         XXX          X",
    "X              G                 X",
    "X            XXXXX               X",
    "X                                X",
    "X    S                           X",
    "X   XXX                     S    X",
    "X                          XXX   X",
    "X                                X",
    "X       F           F            X",
    "X                                X",
    "X      BBBB       BBBB           X",
    "X                                X",
    "X                                X",
    "X                                X",
    "X                                X",
    "X                       S        X",
    "X                      XXX       X",
    "X                                X",
    "X P     XL     M      L          X",
    "XXXXX                            X",
    "X^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

LEVELS = [
    LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5, 
    LEVEL_6, LEVEL_7, LEVEL_8, LEVEL_9, LEVEL_10,
    LEVEL_11, LEVEL_12, LEVEL_13, LEVEL_14, LEVEL_15
]

TUTORIAL_MESSAGES = {
    "1": "A/D or Arrows to Move. SPACE/W to Jump. Double Jump in mid-air!",
    "2": "Jump against a wall, then press SPACE to Wall-Jump!",
    "3": "Jump into cracked blocks from below to shatter them!",
    "4": "Hold SHIFT to DASH! Dashing horizontally shatters blocks!",
    "5": "Jump on top of enemies to defeat them and bounce higher!",
    "6": "Orbs reset your double jump!",
    "7": "Springs launch you!"
}