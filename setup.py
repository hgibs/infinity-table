import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Gibson_LED_Driver",
    version="0.1.0",
    author="G. Holland Gibson",
    author_email="arc.mercury3@gmail.com",
    description="A small package to drive individually addressible LED string lights",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hgibs/infinity-table",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['spidev
)
