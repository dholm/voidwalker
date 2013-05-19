#!/usr/bin/env python

import os

from distutils.core import setup
from voidwalker import __version__


long_description = open(os.path.join(os.path.dirname(__file__),
                                     'description.rst')).read()

setup(name='voidwalker',
      packages=['voidwalker',
                'voidwalker.framework',
                'voidwalker.framework.interface',
                'voidwalker.framework.patching',
                'voidwalker.framework.platform',
                'voidwalker.framework.system',
                'voidwalker.framework.target',
                'voidwalker.framework.types',
                'voidwalker.framework.utils',
                'voidwalker.backends',
                'voidwalker.backends.gdb',
                'voidwalker.backends.gdb.tools',
                'voidwalker.application',
                'voidwalker.application.commands',
                'voidwalker.application.parameters',
                'voidwalker.application.patching',
                'voidwalker.application.cpus'],
      install_requires=['FlowUI>=0.2.1'],
      version=__version__,
      description='A GDB toolbox for low-level debugging',
      author='David Holm',
      author_email='dholmster@gmail.com',
      url='http://github.com/dholm/voidwalker/',
      download_url=('https://github.com/dholm/voidwalker/archive/v%s.zip' %
                    __version__),
      license='GPLv3',
      keywords=['debugging', 'gdb', 'console', 'terminal'],
      classifiers=[
          'Environment :: Console',
          'Topic :: Software Development',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Programming Language :: Python :: 2.7'],
      long_description=long_description)
