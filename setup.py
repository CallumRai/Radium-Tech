import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Get requirements
with open('requirements.txt') as f:
    required = f.read().splitlines()

# This call to setup() does all the work
setup(
    name="Radium-Tech",
    version="0sim.0.1",
    description="Intuitive backtesting for quantitative trading strategies.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/CallumRai/Radium-Tech",
    author="Callum Rai, Ivan Erlic",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=required,
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
