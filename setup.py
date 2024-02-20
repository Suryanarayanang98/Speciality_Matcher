from setuptools import setup, find_packages

setup(
    name='speciality-matcher',
    version='1.0.0',
    packages=find_packages(),
    package_data={'data': ['./data/nucc_taxonomy_mapper.csv']},
    include_package_data=True,
    install_requires=[
        'fuzzywuzzy',
        'pandas'
    ],
)
