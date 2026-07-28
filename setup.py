from setuptools import setup, find_packages

setup(
    name="chronicle",
    version="1.0.0",
    description="Turn your git history into a beautiful story",
    author="Chronicle",
    packages=find_packages(),
    install_requires=["rich>=13.0", "click>=8.0"],
    entry_points={"console_scripts": ["chronicle=chronicle.cli:main"]},
    python_requires=">=3.10",
)
