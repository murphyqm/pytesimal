from distutils.core import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pytesimal",
    version="0.0.1",
    description="Model the conductive cooling of planetesimals with temperature-dependent material properties.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Maeve Murphy Quinlan",
    author_email="eememq@leeds.ac.uk",
    url="https://github.com/murphyqm/pytesimal",
    project_urls={
        "Documentation": "https://pytesimal.readthedocs.io/en/latest/",
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
        "Scientific Background:": "https://doi.org/10.1029/2020JE006726",
    },
    packages=["pytesimal"],  # trying this, now that cfg file is removed
    # py_modules=["pytesimal"],
    python_requires=">=3.7",
    install_requires=["numpy", "matplotlib",],
    setup_requires=["numpy", "matplotlib"],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Visualization",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
    ],
)
