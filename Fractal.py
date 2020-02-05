import sys, pygame, colorsys
import numpy as np
from time import perf_counter as time
import json


# Function definitions
def mandel(x, bound=3, maxiter=100):
    """Calculates if a given number is in the mandelbrot set"""
    c = 0
    for i in range(maxiter):
        c = c**2 + x
        if abs(c) > bound:
            return i

def julia(x, bound=3, maxiter=100):
    """Calculates if a given number is in the julia set"""
    for i in range(maxiter):
        x = x**2 - 0.6 + 0.4j
        if abs(x) > bound:
            return i

def reformat(color):
    """Reformat the color from [0, 1] to [0, 255]"""
    return int(round(color[0] * 255)), \
           int(round(color[1] * 255)), \
           int(round(color[2] * 255))

def get_color(n, max_n):
    """Get the RGB color ([0, 255]) for a given hue value and maximum brightness/saturation"""
    if n == None:
        return (0, 0, 0)
    else:
        n = int(n**0.8)
        return reformat(colorsys.hsv_to_rgb((n%int(max_n**0.8))/int(max_n**0.8), 1, 1))

def calc_pixels(size, x_coords, y_coords):
    """Calculates the color value for each pixel and returns the array"""
    width, height = size
    pixels = np.zeros(size + (3,))
    for i in range(width):
        x = x_coords[i]
        for j, y in enumerate(y_coords):
            c = x + y*1j
            #n = julia(c, bound=2, maxiter=100)
            n = mandel(c, bound=2, maxiter=100)
            c = get_color(n, 100)
            pixels[i, j, :] = c
    return pixels

# start programm
pygame.init()

# define window size
ratio = 3, 2
base = 100
size = width, height = ratio[0]*base, ratio[1]*base
screen = pygame.display.set_mode(size)

# set window title
pygame.display.set_caption("Fractal")

# calculate x and y coordinates for each pixel
base_coords = 0.7
x_lim = x_min, x_max = -ratio[0]*base_coords, ratio[0]*base_coords
y_lim = y_min, y_max = -ratio[1]*base_coords, ratio[1]*base_coords
x_coords = np.linspace(x_min, x_max, width, False)
y_coords = np.linspace(y_min, y_max, height, False)

# initial button states
calc = False
mouse_down = False
mouse_pos_old = (0, 0)

# draw loop
while True:
    # set fps
    pygame.time.delay(100)

    # get events happened in the last frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # get klicked mouse buttons
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # initiate translation
            if event.button == 1:
                mouse_pos_old = event.pos
                mouse_down = True

            # zoom in action
            elif event.button == 4:
                x_lim = np.array(x_lim)
                y_lim = np.array(y_lim)

                m_pos = event.pos
                x_lim -= x_coords[m_pos[0]]
                y_lim -= y_coords[m_pos[1]]

                x_lim *= 0.5
                y_lim *= 0.5

                x_lim += x_coords[m_pos[0]]
                y_lim += y_coords[m_pos[1]]

                x_coords = np.linspace(x_lim[0], x_lim[1], width, False)
                y_coords = np.linspace(y_lim[0], y_lim[1], height, False)

                calc = False

            # zoom out action
            elif event.button == 5:
                x_lim = np.array(x_lim)
                y_lim = np.array(y_lim)

                m_pos = event.pos
                x_lim -= x_coords[m_pos[0]]
                y_lim -= y_coords[m_pos[1]]

                x_lim *= 2
                y_lim *= 2

                x_lim += x_coords[m_pos[0]]
                y_lim += y_coords[m_pos[1]]

                x_coords = np.linspace(x_lim[0], x_lim[1], width, False)
                y_coords = np.linspace(y_lim[0], y_lim[1], height, False)

                calc = False

        # perform translation
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_pos_new = event.pos
                dx = x_coords[mouse_pos_new[0]] - x_coords[mouse_pos_old[0]]
                dy = y_coords[mouse_pos_new[1]] - y_coords[mouse_pos_old[1]]

                x_lim -= dx

                y_lim -= dy

                x_coords = np.linspace(x_lim[0], x_lim[1], width, False)
                y_coords = np.linspace(y_lim[0], y_lim[1], height, False)

                calc = False
                mouse_down = False

        # get klicked keys
        elif event.type == pygame.KEYDOWN:

            # perform save
            if event.unicode == "s":
                json_data = {"x_lim": list(x_lim), "y_lim": list(y_lim)}
                with open("save.json", "w+") as file:
                    json.dump(json_data, file)

            # perform load
            elif event.unicode == "l":
                try:
                    with open("save.json", "r") as file:
                        json_data = json.load(file)
                except Exception:
                    pass
                else:
                    x_lim = json_data["x_lim"]
                    y_lim = json_data["y_lim"]

                    x_coords = np.linspace(x_lim[0], x_lim[1], width, False)
                    y_coords = np.linspace(y_lim[0], y_lim[1], height, False)

                    calc = False

    # push calculated image to the window/surface
    if not calc:
        pixels = calc_pixels(size, x_coords, y_coords)
        pygame.surfarray.blit_array(screen, pixels)
        pygame.image.save(screen, "Fractal.PNG")
        calc = True

    # show image on the screen
    pygame.display.update()
