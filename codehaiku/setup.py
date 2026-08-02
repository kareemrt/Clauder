from setuptools import setup, find_packages

setup(
    name="codehaiku",
    version="1.0.0",
    description="Poetry distilled from source code",
    author="Claude",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "codehaiku=codehaiku.cli:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Artistic Software",
    ],
)
