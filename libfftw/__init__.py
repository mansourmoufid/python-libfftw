'''ctypes wrapper for the FFTW library'''

import ctypes
import distutils.sysconfig
import os
import subprocess


__author__ = 'Mansour Moufid'
__copyright__ = 'Copyright 2018, Mansour Moufid'
__license__ = 'ISC'
__version__ = '0.1'
__email__ = 'mansourmoufid@gmail.com'
__status__ = 'Development'

__all__ = [
    'fftwf',
]


libdirs = ['.']
libdir = os.environ.get('FFTW_LIBDIR')
if libdir is not None:
    libdirs.append(libdir)
try:
    output = subprocess.check_output(
        ['pkg-config', '--variable=libdir', 'fftw3f']
    )
    libdir = output.rstrip()
    libdirs.append(libdir)
except:
    pass
libdir = distutils.sysconfig.get_config_var('LIBDIR')
if libdir is not None:
    libdirs.append(libdir)
names = ['libfftw3f.so', 'libfftw3f.dylib', 'libfftw3f-3.dll']
for lib in [os.path.join(dir, name) for dir in libdirs for name in names]:
    if os.path.exists(lib):
        break
libfftwf = ctypes.cdll.LoadLibrary(lib)
