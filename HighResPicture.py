import json, imageio, colorsys
import numpy as np
from numba import jit

@jit
def mandel(x, bound=3, maxiter=100):
    """Calculates if a given number is in the mandelbrot set"""
    c = 0
    for i in range(maxiter):
        c = c**2 + x
        if abs(c) > bound:
            return i

@jit
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
    pixels = np.zeros(size[::-1] + (3,), dtype=np.uint8)
    for i in range(width):
        x = x_coords[i]
        for j, y in enumerate(y_coords):
            c = x + y*1j
            #n = julia(c, bound=2, maxiter=100)
            n = mandel(c, bound=2, maxiter=1000)
            c = get_color(n, 100)
            pixels[j, i, :] = c
        if i%100 == 0:
            print(str(int(i*100/width)) + "% abgeschlossen!")
    return pixels

# start programm/get fractal coordinates
try:
    with open("save.json", "r") as file:
        json_data = json.load(file)
except Exception:
    print("No save.json found!")
    print("Open Fractal.py and press 's' to save the Fractal location!")
else:
    x_lim = json_data["x_lim"]
    y_lim = json_data["y_lim"]

    # get desired width
    while True:
        width = input("Width: ")
        try:
            width = int(width)
        except Exception:
            continue
        else:
            break

    # get desired height
    while True:
        height = input("Height: ")
        try:
            height = int(height)
        except Exception:
            continue
        else:
            break

    size = width, height

    x_coords = np.linspace(x_lim[0], x_lim[1], width, False)
    y_coords = np.linspace(y_lim[0], y_lim[1], height, False)

    pixels = calc_pixels(size, x_coords, y_coords)

    imageio.imwrite("Fractal%dx%d.PNG" %size, pixels)

    print("Finished!")
