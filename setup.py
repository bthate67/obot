# This file is place in the Public Domain.

from setuptools import setup, os

def mods(name):
    res = []
    for p in os.listdir(name):
        if p.endswith(".py"):
           res.append(p[:-3])
    return res

def pmods(name):
    res = []
    for p in os.listdir(name):
        if p.endswith(".py"):
           res.append("%sp[:-3])
    return res
    
def read():
    return open("README.rst", "r").read()

setup(
    name='botlib',
    version='118',
    description="python3 bot library",
    author='Bart Thate',
    author_email='bthate67@gmail.com', 
    url='https://github.com/bthate67/botlib',
    long_description=read(),
    license='Public Domain',
    package_dir={'': 'lib'},
    py_modules=mods("lib"),
    scripts=["bin/bot", "bin/botc", "bin/bots"],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
