#Try to use setuptools if present. If not then python_requires,
#install_requires and setup_requires will be ignored
try:
    from setuptools import setup
except:
    from distutils.core import setup


with open("package_description.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pytesimal",
    version="2.0.0",
    description="Model the conductive cooling of planetesimals with temperature-dependent material properties.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="M. Murphy Quinlan, A.M. Walker, P. Selves, L.S.E. Teggin",
    author_email="eememq@leeds.ac.uk",
    url="https://github.com/murphyqm/pytesimal",
    project_urls={
        "Documentation": "https://pytesimal.readthedocs.io/en/latest/",
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
        "Scientific Background:": "https://doi.org/10.1029/2020JE006726",
    },
    packages=["pytesimal"],
    # py_modules=["pytesimal"],
    python_requires=">=3.7",
    install_requires=["numpy", "matplotlib", ],
    setup_requires=["numpy", "matplotlib"],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
    ],
)
