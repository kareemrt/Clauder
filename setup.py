from setuptools import setup, find_packages

setup(
    name="clauder",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "anthropic>=0.100.0",
        "rich>=15.0.0",
        "gitpython>=3.1.50",
        "click>=8.3.3",
    ],
    entry_points={
        "console_scripts": [
            "clauder=clauder.main:main",
        ],
    },
    python_requires=">=3.9",
)
