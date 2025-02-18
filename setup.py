from setuptools import setup, find_packages

setup(
    name="pytinytask",
    version="1.7",
    author="Smart Boy",
    description="A simple macro recording and replaying tool",
    long_description=open('README.md').read(),  # Or .rst if you're using reStructuredText
    long_description_content_type='text/markdown',  # Set to 'text/rst' if you're using reStructuredText
    packages=find_packages(),
    install_requires=[
        "keyboard",
        "mouse",
        "customtkinter"
    ],
    entry_points={
        'console_scripts': [
            'tiny_task = tinytask:main',
            'tinytask = tinytask:main',
            'tiny-task = tinytask:main',
        ]
    },
    python_requires=">=3.6",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
)
