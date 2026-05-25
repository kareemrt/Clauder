from setuptools import setup, find_packages

setup(
    name="fractal-canvas",
    version="1.0.0",
    description="Terminal fractal art generator — Mandelbrot, Julia, Burning Ship, Newton, Tricorn",
    author="Claude",
    python_requires=">=3.8",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "fractal-canvas=fractal_canvas.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Topic :: Artistic Software",
        "License :: OSI Approved :: MIT License",
    ],
)
