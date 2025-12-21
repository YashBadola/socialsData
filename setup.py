from setuptools import setup, find_packages

setup(
    name="socialsData",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "socials-data=socials_data.cli:cli",
        ],
    },
)
