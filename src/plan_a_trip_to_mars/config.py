"""Script where we place all constants we will need.

Those values that are not present in the `astropy` library are found at:
    https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
    https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html
    https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html
"""

import astropy.constants as c

# PHYSICAL CONSTANTS

# Gravitational constant
G = c.G.value

# 1 astronomical unit (average distance between Sun and Earth)
AU = c.au.value

# Mass of ...
M_sun = c.M_sun.value
M_earth = c.M_earth.value
M_mars = 0.64171e24
M_moon = 0.07346e24

# Raduis of ...
R_sun = c.R_sun.value
R_earth = c.R_earth.value
R_mars = 3396.2e3
R_moon = 1738.1e3

# Distance to the Sun for ...
D_earth = AU
D_mars = 1.524 * AU

# Mean orbital velocity for ...
V_earth = 29.78e3
V_mars = 24.07e3

# # SIMULATION SPECIFIC
# FPS = 24  # Frames-per-second: speed up the animation
# SIZE = 3 * AU  # The side length of the simulated universe
# TOT_TIME = 5e4
