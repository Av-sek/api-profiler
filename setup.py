from setuptools import setup, find_packages

setup(
    name="api_profiler",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.0", 
        "diskcache"
    ],
    entry_points={
        "console_scripts": [
            "profile=api_profiler.main:main",
        ],
    },
    author="Your Name",
    description="Django profiling middleware CLI tool",
    url="https://github.com/Av-sek/api_profiler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
    ],
)
