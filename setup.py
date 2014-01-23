# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.0b3.dev0'
description = "Improved syndication for Plone sites providing Atom, iTunes, \
NewsML 1, RSS 1.0 and RSS 2.0 feeds."
long_description = (
    open("README.rst").read() + "\n" +
    open("CONTRIBUTORS.rst").read() + "\n" +
    open("CHANGES.rst").read()
)

setup(name='collective.syndication',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Intended Audience :: End Users/Desktop",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Office/Business :: News/Diary",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='plone atom itunes rss syndication newsml rdf',
      author='Gonzalo Almeida',
      author_email='flecox@ravvit.net',
      url='http://github.com/collective/collective.syndication',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'lxml',
          'plone.app.registry',
          'Products.CMFCore',
          'Products.CMFDefault',
          'Products.CMFPlone>=4.1, <4.3',
          'Products.GenericSetup',
          'setuptools',
          'zope.component',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'plone.app.dexterity',
              'plone.app.testing',
              'plone.browserlayer',
              'plone.dexterity',
              'plone.registry',
              'plone.testing',
              'unittest2',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
