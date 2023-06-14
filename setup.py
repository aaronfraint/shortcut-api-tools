from setuptools import find_packages, setup

setup(
    name="shortcut_api_tools",
    packages=find_packages(),
    version="0.0.1",
    description="Tools for working with the Shortcut.com API",
    author="Aaron Fraint",
    license="GPL-3.0",
    entry_points="""
        [console_scripts]
        sc=src.cli:main
    """,
)
