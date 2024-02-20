from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'Medical Speciality Standardiser and comparer'
LONG_DESCRIPTION = 'A package that allows to standardise medical speciality & can be used for comparision.'

# Setting up
setup(
    name="speciality-matcher",
    version=VERSION,
    author="None",
    author_email="None",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['fuzzywuzzy',
        'pandas'],
    keywords=['python', 'medical', 'speciality', 'fuzzy', 'standaridisation', 'comparision'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)