"""Script where we place all constants we will need.

Those values that are not present in the `astropy` library are found at:
    https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
    https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html
    https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html
"""


# PHYSICAL CONSTANTS

# Gravitational constant
G = 6.6743e-11  # c.G.value

# 1 astronomical unit (average distance between Sun and Earth)
AU = 1.495978707e11  # c.au.value

# Mass of ...
M_sun = 1.989e30  # c.M_sun.value
M_earth = 5.972e24  # c.M_earth.value
M_mars = 0.64171e24
M_moon = 0.07346e24

# Raduis of ...
R_sun = 6.95700e8  # c.R_sun.value
R_earth = 6.3781e6  # c.R_earth.value
R_mars = 3396.2e3
R_moon = 1738.1e3

# Distance to the Sun from ...
D_earth = AU
D_mars = 1.524 * AU

# Mean orbital velocity for ...
V_earth = 29.78e3
V_mars = 24.07e3
