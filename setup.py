from setuptools import setup, find_packages

setup(
    name="socials_data",
    version="0.1.0",
    description="A unified library to store and access datasets of public figures for LLM training.",
    author="Jules",
    packages=find_packages(),
    install_requires=[
        "click",
        "datasets",
        "pandas",
        "tqdm",
        "openai",
        "langchain-text-splitters"
    ],
    entry_points={
        "console_scripts": [
            "socials-data=socials_data.cli:main",
        ],
    },
)
