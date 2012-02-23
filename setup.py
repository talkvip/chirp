#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# -*- mode: python -*-
from setuptools import setup, find_packages
from distutils.extension import Extension
from numpy.distutils.core import setup,Extension
import sys, os
import os.path as op

ext_libs = ['fftw3']
ext_incl = []

if hasattr(os,'uname'):
    system = os.uname()[0]
else:
    system = 'Windows'

if system=='Darwin':
    ext_libs.append('lapack')
    ext_incl.append('/opt/local/include')
elif system=='Linux':
    ext_libs.append('lapack')

# --- Distutils setup and metadata --------------------------------------------

VERSION = '1.1.1'

cls_txt = \
"""
Development Status :: 5 - Production/Stable
Intended Audience :: Science/Research
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Topic :: Scientific/Engineering
Operating System :: Unix
Operating System :: POSIX :: Linux
Operating System :: MacOS :: MacOS X
Natural Language :: English
"""

short_desc = "Analyze and compare bioacoustic recordings"

long_desc = \
"""
Chirp provides a number of related tools for analyzing and comparing
bioacoustic recordings.  It can operate on recordings stored in
standard wave files, with the option of restricting analyses to
specific spectrotemporal regions of the recording.  Regions are
defined with polygons in the time-frequency domain.  The tools consist
of the following programs:

+ chirp :: inspect spectrograms of recordings and define regions
+ cpitch :: determine the pitch of recordings
+ ccompare :: compare libraries of recordings using pitch or spectrograms
"""

_vitterbi = Extension('chirp.pitch._vitterbi',sources=['chirp/pitch/vitterbi.pyf','chirp/pitch/vitterbi.c'])
_dtw = Extension('chirp.compare._dtw',sources=['chirp/compare/dtw.pyf','chirp/compare/dtw.c'],
                 extra_compile_args=['-std=c99'])
_libtfr = Extension('chirp.common._libtfr',sources=['libtfr/libtfr.c','libtfr/tfr.c','libtfr/mtm.c'],
                    libraries=ext_libs, extra_compile_args=['-std=c99'], include_dirs=ext_incl)

setup(
  name = 'chirp',
  version = VERSION,
  description = short_desc,
  long_description = long_desc,
  classifiers = [x for x in cls_txt.split("\n") if x],
  author = 'C Daniel Meliza',
  author_email = '"dan" at the domain "meliza.org"',
  maintainer = 'C Daniel Meliza',
  maintainer_email = '"dan" at the domain "meliza.org"',
  url = 'https://dmeliza.github.com/chirp',
  download_url = 'https://github.com/dmeliza/chirp',
  packages= find_packages(exclude=["*test*"]),
  ext_modules = [_vitterbi,_dtw,_libtfr],
  install_requires=['distribute', 'numpy>=1.3'],
  entry_points = {'console_scripts' : ['cpitch = chirp.pitch.tracker:cpitch',
                                       'cplotpitch = chirp.misc.plotpitch:main',
                                       'ccompare = chirp.compare.ccompare:main'],
                  'gui_scripts' : ['chirp = chirp.gui.chirpgui:main'],
                  'chirp.compare.method' : ['spcc = chirp.compare.spcc:spcc',
                                            'masked_spcc = chirp.compare.masked_spcc:masked_spcc',
                                            'pitch_dtw = chirp.compare.pitch_dtw:pitch_dtw'],
                  'chirp.compare.storage' : ['file = chirp.compare.file_storage:file_storage',
                                             'sqlite = chirp.compare.sqlite_storage:sqlite_storage']},
)


# Variables:
# End:
