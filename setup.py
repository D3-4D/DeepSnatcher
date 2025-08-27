from setuptools import setup, find_packages

setup(
    name="DeepSnatcher",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "markdown",
        "beautifulsoup4",
        "fake-useragent",
        "requests",
        "requests-toolbelt"
    ],
    python_requires=">=3.7",
)
