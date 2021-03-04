#!/usr/bin/env python
import os
import shutil
from distutils.command import clean
from pathlib import Path

from setuptools import find_packages, setup


classifiers = """
Development Status :: 4 - Beta
License :: Public Domain
Environment :: Console
Intended Audience :: Education
Intended Audience :: Developers
Intended Audience :: Information Technology
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Topic :: Utilities
Topic :: Text Processing :: General
"""


def get_version():
    """
    Determine a version string using a file VERSION.txt
    """
    version = '0.0.1'
    if os.path.isfile('VERSION.txt'):
        with open('VERSION.txt', 'r') as f:
            version = f.read().strip()
    return version


def get_readme():
    """
    Open and read the readme. This would be the place to convert to RST, but we no longer have to.
    """
    with open('README.md') as f:
        return f.read()


class PurgeCommand(clean.clean):
    """
    Custom command to purge everything
    """
    description = "purge 'build', 'dist', '*.egg-info' and coverage output"
    patterns = [
        # build paths
        'build', 'dist', '*.egg-info', '*.dist-info',
        # run code paths
        '**/__pycache__',
        # test artifacts
        '.pytest_cache',
        'htmlcov',
        '.coverage',
        'coverage.xml',
        'unit_tests.xml',
    ]

    def existing_paths(self):
        current_dir = Path('.')
        return [
            path
            for pattern in self.patterns
            for path in current_dir.glob(pattern)
            if path.exists()
        ]

    def run(self):
        super().run()
        for path in self.existing_paths():
            if self.dry_run:
                print('would remove {}'.format(path))
            elif path.is_dir():
                shutil.rmtree(str(path))
                print('removed directory {}'.format(path))
            else:
                path.unlink()
                print('removed {}'.format(path))


setup(
    name='pymarcspec',
    version=get_version(),
    description='Search pymarc.Record using a string expression',
    long_description=get_readme(),
    long_description_content_type='text/markdown; charset=UTF-8; variant=CommonMark',
    author='Dan Davis',
    author_email='dan@danizen.net',
    url='https://github.com/danizen/pymarcspec/',
    packages=[pkg for pkg in find_packages() if not pkg.startswith('test')],
    include_package_data=True,
    install_requires=[
        'attrs',
        'lxml',
        'pymarc',
        'tatsu',
    ],
    tests_require=[
        'flake8',
        'pytest',
        'pytest-cov',
    ],
    cmdclass={
        'purge': PurgeCommand,
    },
    entry_points={
        'console_scripts': [
            'pymarcsearch=pymarcspec.search:main',
        ]
    },
    classifiers=list(filter(None, classifiers.split("\n"))),
    test_suite="test",
    python_requires=">=3.6"
)
