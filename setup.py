from setuptools import setup, find_packages

setup(
    name="nebula-fractal",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24",
        "pillow>=10.0",
        "rich>=13.0",
        "click>=8.1",
    ],
    entry_points={
        "console_scripts": [
            "nebula=nebula.cli:main",
        ],
    },
    python_requires=">=3.10",
)
