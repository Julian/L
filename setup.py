import os

from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    long_description = readme.read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy"
]

setup(
    name="l",
    packages=find_packages(),
    install_requires=["betterpath", "click"],
    setup_requires=["vcversioner"],
    entry_points={"console_scripts": ["l = l.cli:main"]},
    vcversioner={"version_module_paths": ["l/_version.py"]},
    author="Julian Berman",
    author_email="Julian@GrayVines.com",
    classifiers=classifiers,
    description="A project-oriented directory lister",
    license="MIT",
    long_description=long_description,
    url="https://github.com/Julian/L",
)
