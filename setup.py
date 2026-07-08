from setuptools import setup, find_packages

setup(
    name="pulsar-git",
    version="1.0.0",
    description="Git Repository Heartbeat Visualizer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Pulsar Contributors",
    url="https://github.com/kareemrt/clauder",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pulsar=pulsar.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    keywords="git visualization cli dashboard heartbeat commits",
)
