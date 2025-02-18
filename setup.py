from setuptools import setup, find_packages

setup(
    name="tiny_task",
    version="1.0",
    author="Your Name",
    description="A simple macro recording and replaying tool",
    packages=find_packages(),
    install_requires=[
        "keyboard",
        "mouse",
        "customtkinter"
    ],
    entry_points={
        'console_scripts': [
            'tiny_task = tiny_task:main'
            #'tiny_task = tiny_task:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
