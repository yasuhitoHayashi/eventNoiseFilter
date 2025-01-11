"""
@author: HAYASHI Yasuhito (dangom_ya)

CopyPolicy: 
    Released under the terms of the LGPLv2.1 or later.
"""

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import pybind11

ext_modules = [
    Extension(
        'filter_events',
        ['filter_events.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=['-O3', '-std=c++11'],
    ),
]

setup(
    name='filter_events',
    version='0.1',
    author='HAYASHI Yasuhito',
    description='A Python module for event filtering implemented in C++ with pybind11',
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
    zip_safe=False,
)