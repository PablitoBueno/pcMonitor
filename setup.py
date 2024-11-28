# setup.py
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        ["monitor_cpu.pyx","monitor_energy.pyx"],language="c++"
    )
)
