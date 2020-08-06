"""A setuptools based setup module."""

from os import path
from setuptools import setup, find_packages
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='elt-tools-aio',
    version='1.0.0',
    description='Async Tools for Monitoring and Troubleshooting ELT arrangements',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dewaldabrie/elt_tools_aio',
    author='Dewald Abrie',
    author_email='dewaldabrie@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='SQLAlchemy GCP Google BigQuery SQL ETL ELT RDBMS asycio monitoring fix',
    packages=find_packages(),
    install_requires=['SQLAlchemy-aio',
                      'PyBigQuery',
                      'PyMySQL',
                      'psycopg2',
                      'sqlalchemy-redshift',
                      ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
        'env': ['python-dotenv']
    },
    project_urls={
        'Bug Reports': 'https://github.com/dewaldabrie/elt_tools_aio/issues',
        'Source': 'https://github.com/dewaldabrie/elt_tools_aio',
    },
)
