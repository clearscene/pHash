# -*- coding: utf-8 -*-
from setuptools import setup
from glob import glob

setup(name="pHash",
    version="1.0",
    description="Bindings for pHash library ",
    long_description="""
Python Bindings for pHash perceptual comparaison library
    """,

    url="http://packages.python.org/python-phash/",
    download_url="http://github.com/trolldbois/python-phash/tree/master",
    license='MIT',
    classifiers=[
        "Topic :: Multimedia",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
    ],
    keywords=['pHash','libphash'],
    author="Loic Jaquemet",
    author_email="loic.jaquemet+python@gmail.com",
    py_modules = ["pHash"], 
#    extras_require = {
#        'CACHE':  ["python-memcached"],
#    },
    entry_points = {
        'console_scripts': [
            'pHash   = pHash:ph_about',
        ]
    },
    #setup_requires=[
    #    "nose",
    #    "sphinx",
    #],
    #test_suite='nose.collector',
)
