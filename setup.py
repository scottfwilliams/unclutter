# -*- coding: utf-8 -*-
"""
    Setup file for unclutter.
"""

from setuptools import setup


setup(
    name="unclutter",
    version="1.0.0",
    packages=["unclutter", "unclutter.command"],
    install_requires=["Click"],
    entry_points={
      "console_scripts": [
          "unclutter = unclutter.entry:cli",
      ]
    }
)
