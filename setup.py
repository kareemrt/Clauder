from setuptools import setup, find_packages

setup(
    name="attractor",
    version="1.0.0",
    description="Strange Attractor Art Engine — generate beautiful chaos-theory imagery",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Attractor Project",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24",
        "matplotlib>=3.7",
    ],
    entry_points={
        "console_scripts": [
            "attractor=attractor.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
