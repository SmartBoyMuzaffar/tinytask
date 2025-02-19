from setuptools import setup, find_packages

setup(
    name="pytinytask",
    version="3.0",
    author="Smart Boy",
    description="A simple macro recording and replaying tool",
    url="https://github.com/SmartBoyMuzaffar/tinytask",
    long_description=open('README.md').read(),  # Or .rst if you're using reStructuredText
    long_description_content_type='text/markdown',  # Set to 'text/rst' if you're using reStructuredText
    packages=find_packages(),
    install_requires=[
        "customtkinter==5.2.2",
        "darkdetect==0.8.0",
        "keyboard==0.13.5",
        "mouse==0.7.1",
        "packaging==24.2",
        "pillow==11.1.0",
        "setuptools==75.8.0",
        "wheel==0.45.1",
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
    include_package_data=True,
    package_data={'': ['src/*.png']},
)
