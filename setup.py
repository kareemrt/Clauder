from setuptools import setup, find_packages

setup(
    name="lumina-cosmic",
    version="1.0.0",
    description="Generative Cosmic Art Engine",
    author="Claude",
    packages=find_packages(),
    install_requires=["numpy>=1.24.0", "Pillow>=10.0.0"],
    entry_points={"console_scripts": ["lumina=lumina.cli:main"]},
    python_requires=">=3.10",
)
