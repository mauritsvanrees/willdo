from setuptools import setup, find_packages

version = '0.2'

setup(name='willdo',
      version=version,
      description="Will Do List",
      long_description="""Will Do List for Grok, see www.markforster.net\
""",
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[], 
      keywords="willdo todo",
      author="Maurits van Rees",
      author_email="maurits@vanrees.org",
      url="http://maurits.vanrees.org",
      license="GPL",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'grok',
                        # Add extra requirements here
                        ],
      entry_points="""
      # Add entry points here
      """,
      )
