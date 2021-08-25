# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = {"": "src"}

packages = ["plan_a_trip_to_mars", "plan_a_trip_to_mars.misc"]

package_data = {"": ["*"]}

install_requires = [
    "astropy>=4.3.1,<5.0.0",
    "matplotlib>=3.4.3,<4.0.0",
    "numpy>=1.21.2,<2.0.0",
]

entry_points = {
    "console_scripts": ["plan-a-trip-to-mars = plan_a_trip_to_mars.__main__:main"]
}

setup_kwargs = {
    "name": "plan-a-trip-to-mars",
    "version": "0.1.0",
    "description": "",
    "long_description": None,
    "author": "engeir",
    "author_email": "eirroleng@gmail.com",
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "package_dir": package_dir,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.7,<3.11",
}


setup(**setup_kwargs)
