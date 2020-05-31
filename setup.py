import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multilingualcl",
    version="0.0.1",
    author="John Samuel",
    author_email="johnsamuelwrites@example.com",
    description="Building multilingual command line",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnsamuelwrites/MultilingualCL",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL v3.0 or later",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
