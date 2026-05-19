from setuptools import setup, find_packages

setup(
    name="fractal-dreams",
    version="1.0.0",
    description="Infinite mathematical beauty, one pixel at a time",
    packages=find_packages(),
    install_requires=["numpy>=1.24", "Pillow>=9.0", "click>=8.0"],
    entry_points={"console_scripts": ["fractal-dreams=fractal_dreams.cli:cli"]},
    python_requires=">=3.10",
)
