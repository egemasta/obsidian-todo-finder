from setuptools import setup, find_packages

setup(
    name="obsidian_todo_finder",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0",
    ],
    entry_points={
        'console_scripts': [
            'obsidian-todo-finder=main:main',
        ],
    },
    author="Serge Decker",
    author_email="serge.decker@gmail.com",
    description="Tool zum Sammeln und Organisieren von ToDo-Einträgen aus einer Obsidian Vault",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/egemasta/obsidian-todo-finder",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)