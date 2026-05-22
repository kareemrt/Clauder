from setuptools import setup, find_packages

setup(
    name="fractalforge",
    version="1.0.0",
    description="Terminal fractal art generator with PNG export and zoom sequences",
    author="FractalForge",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21",
        "Pillow>=9.0",
    ],
    entry_points={
        "console_scripts": [
            "fractalforge=fractalforge.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
        "Environment :: Console",
    ],
)
