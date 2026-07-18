from setuptools import setup, find_packages

setup(
    name="gitpulse",
    version="1.0.0",
    description="Terminal analytics dashboard for git repositories",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "rich>=13.0.0",
        "click>=8.0.0",
        "colorama>=0.4.0",
    ],
    entry_points={
        "console_scripts": [
            "gitpulse=gitpulse.cli:main",
        ],
    },
)
