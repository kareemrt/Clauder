from setuptools import setup, find_packages

setup(
    name="fractalscope",
    version="1.0.0",
    description="Terminal fractal explorer with PNG export",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="FractalScope",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24",
    ],
    extras_require={
        "image": ["Pillow>=9.0"],
    },
    entry_points={
        "console_scripts": [
            "fractalscope=fractalscope.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Multimedia :: Graphics",
    ],
)
