from setuptools import setup, find_packages
import os

version = open('version.txt').read()

long_description = (
    open("README.txt").read()
    + '\n' +
    open(os.path.join("docs", "HISTORY.txt")).read()
    + '\n')

setup(name='vnccollab.common',
      version=version,
      description="VNC Collaboration Common Code",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Jose Dinuncio',
      author_email='jose.dinuncio@vnc.biz',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['vnccollab', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.jquery',
          'five.grok',
          'plone.api',
          'collective.js.jqueryui',
      ],
      extras_require={'test': ['plone.app.testing']},
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      #setup_requires=["PasteScript"],
      #paster_plugins=["templer.localcommands"],
      )
