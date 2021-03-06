#!/usr/bin/env python
import codecs
import os
import re
from setuptools import setup


directory_name = os.path.dirname(__file__)
with codecs.open(os.path.join(directory_name, 'marigoso', '__init__.py'), encoding='utf-8') as fd:
    VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(fd.read()).group(1)

setup(
    name="marigoso",
    description="Functional Testing Tools for end to end testing of web applications and APIs.",
    author="Ernesto D. Luzon Jr.",
    license="MIT license",
    author_email="please_raise_a_bug_in_myrepo@github.com",
    url="https://github.com/ldiary/marigoso",
    version=VERSION,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Software Development :: Testing",
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python',
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'pytest',
        'selenium',
    ],
    packages=["marigoso"],
    entry_points={
    },
    include_package_data=True,
)
