from setuptools import setup, find_packages

setup(
    name="harmoniq",
    version="1.0.0",
    description="Mathematical Music Composer — turn sequences into sound",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Harmoniq Contributors",
    python_requires=">=3.9",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "harmoniq=harmoniq.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)
