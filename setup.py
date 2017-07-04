
import ast
import os
import re

from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('cpybca/__init__.py', 'rb') as f:
    VERSION = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as page:
    README = page.read()

setup(
    name='Cpybca',
    version=VERSION,
    url='https://github.com/3mp3ri0r/cpybca/',
    license='MIT',
    author='Christoforus Surjoputro',
    author_email='cs_sanmar@yahoo.com',
    description='A python module to access BCA API. In this version, you can check balance, '
                'account statement (history), and transfer fund.',
    long_description=README,
    packages=['cpybca'],
    zip_safe=False,
    platforms='any',
    extras_require={
        'dev': ['nose'],
    },
    python_requires='~=3.3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
