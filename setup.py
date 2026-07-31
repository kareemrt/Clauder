from setuptools import setup, find_packages

setup(
    name="gitpulse",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["rich>=13.0"],
    entry_points={
        "console_scripts": [
            "gitpulse=gitpulse.cli:main",
        ],
    },
    python_requires=">=3.11",
    author="GitPulse",
    description="Beautiful git repository analytics and visualization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Version Control",
    ],
)
