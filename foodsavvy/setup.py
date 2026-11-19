from setuptools import setup, find_packages

setup(
    name="foodsavvy",
    version="1.0.0",
    description="Intelligent food waste reduction CLI",
    author="FoodSavvy Contributors",
    python_requires=">=3.10",
    packages=find_packages(),
    package_data={"foodsavvy": ["../data/*.json"]},
    include_package_data=True,
    install_requires=[
        "click>=8.1",
        "rich>=13.0",
    ],
    entry_points={
        "console_scripts": [
            "foodsavvy=foodsavvy.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
)
