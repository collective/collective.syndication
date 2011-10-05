# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.atomsyndication',
      version=version,
      description="",
      long_description=open(os.path.join("README.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone atom syndication',
      author='Joaquín Rosales',
      author_email='globojorro@gmail.com',
      url='http://github.com/collective/collective.atomsyndication',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'five.grok>=1.2.0',
        ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
