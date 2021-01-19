# -*- coding: utf-8 -*-
"""
    Setup file for unclutter.
    Use setup.cfg to configure your project.
"""

from setuptools import setup, find_packages


setup(
    entry_points={
        'console_scripts': [
            'init_unclutter_db = unclutter.initialize-db:initialize_database',
            # 'init_unclutter_db = unclutter.initialize-db:initialize_database',
            # 'init_unclutter_db = unclutter.initialize-db:initialize_database'
        ],
    },
    name="Unclutter",
    version="0.4",
    packages=find_packages(),
)
