from setuptools import setup, find_packages

setup(
    name="socials-data",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "datasets",
        "pandas",
        "tqdm",
        "openai",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "socials-data=socials_data.cli:main",
        ],
    },
)
