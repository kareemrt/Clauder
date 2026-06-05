from setuptools import setup, find_packages

setup(
    name="fractalscope",
    version="1.0.0",
    description="Terminal fractal renderer — Mandelbrot, Julia, Burning Ship & more",
    author="Clauder",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "fractalscope=fractalscope.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Artistic Software",
    ],
)
