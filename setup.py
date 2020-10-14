from distutils.core import setup, find_packages
setup(
  name = 'midimusic',         # How you named your package folder (MyLib)
  #packages = ['midimusic'],   # Chose the same as "name"
  packages=find_packages(),
  version = '0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Automate fetching of midis from MuseNet',   # Give a short description about your library
  author = 'Phil Brockman',                   # Type in your name
  author_email = 'phil.brockman@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/PhilBrockman/musepyt',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/PhilBrockman/musepyt/archive/v4.tar.gz',    # I explain this later on
  keywords = ['MuseNet', 'midi'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'IPython',
          'pretty_midi',
          'numpy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
