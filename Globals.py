
class Globs:
    RUNNING = True

    # Window Sizes
    MONITOR_SIZE = None
    WINDOW_SIZE = [800, 600]
    FULLSCREEN = False
    SCALED = False

    # Options
    PAUSED = True
    DEBUG_VISUALS = False
    DEBUG_TEXT = False

    # Framerate
    FPS = 60
    dt = 1

    # Game Constants
    GRAVITY = 50
    GRAVITY_MAX = 20

    TILE_SIZE = 50


def Set_FPS(dt):
    Globs.dt = dt
    Globs.GRAVITY = 50 * Globs.dt


# Colors
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

orange = (255, 150, 0)
purple = (200, 0, 200)

sky = (33, 64, 100)
sky_B = (33, 70, 110)
nightSky = (0, 20, 50)
nightSky_B = (0, 25, 55)
portal_A = (200, 0, 200, 50)
portal_B = (150, 0, 250, 50)
