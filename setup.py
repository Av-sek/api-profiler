from setuptools import setup, find_packages

setup(
    name="api_profiler",
    version="0.1.6",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.0", 
        "diskcache"
    ],
    entry_points={
        "console_scripts": [
            "profile=api_profiler.main:entry_point",
        ],
    },
    author="Abhishek Ghorashainee",
    author_email="abhishekghorashainee07@gmail.com",  # Add your email here
    description="Django profiling middleware CLI tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Av-sek/api-profiler",
    project_urls={
        "Source": "https://github.com/Av-sek/api-profiler",
        "Tracker": "https://github.com/Av-sek/api-profiler/issues",
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    license="MIT",
    keywords="django profiler middleware cli development",
)