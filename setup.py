# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import codecs

pwd = os.path.abspath(os.path.dirname(__file__))

about = {}
with codecs.open(os.path.join(pwd, "luascli", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=find_packages(),
    package_dir={"luascli": "luascli"},
    include_package_data=True,
    license=about["__license__"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["Click", "requests", "xmltodict"],
    entry_points="""
        [console_scripts]
        luas=luascli.main:luas
    """,
)
