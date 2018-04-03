from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

about = {}
with open(path.join(here, 'jike', '__init__.py'), encoding='utf-8') as f:
    exec('\n'.join(filter(lambda l: l.startswith('__'), f.readlines())), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    keywords=about['__keywords__'],
    packages=find_packages(exclude=['docs', 'tests']),
    package_dir={
        'jike': 'jike'
    },
    install_requires=[
        'requests>=2.18.0',
        'pillow>=3.4.0',
        'qrcode>=5.3',
    ],
    extras_require={
        'test': ['responses>=0.8.0'],
        'doc': ['nbconvert>=5.3.0']
    },
    tests_require=['responses>=0.8.0'],
    project_urls={
        'Bug Reports': 'https://github.com/Sorosliu1029/Jike-Metro/issues',
        'Say Thanks!': 'http://saythanks.io/to/Sorosliu1029',
        'Source': 'https://github.com/Sorosliu1029/Jike-Metro/',
    },
)
