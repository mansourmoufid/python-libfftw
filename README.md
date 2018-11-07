LibFFTW is a Python ctypes wrapper for the FFTW library.

LibFFTW supports single-precision, one-dimensional DFTs.


|                 | Single-precision (float) | Double-precision (double) |
| --------------- | ------------------------ | ------------------------- |
| One-dimensional |           Yes            |             No            |
| Two-dimensional |           Soon           |             No            |


## Requirements

LibFFTW requires Python, [NumPy][], and the [FFTW][] library.

[pkg-config][] (or [pkgconf][]) is useful but optional.

To install these on a Debian GNU/Linux system:

    $ sudo apt-get install libfftw3-dev pkg-config python python-numpy

To run unit tests, [pytest][] is required.


## Usage

    import libfftw.fftwf
    import numpy
    numpy.fft = libfftw.fftwf.FFT()

    x = numpy.array([1, 2, 3], dtype=numpy.complex64)
    numpy.fft.fft(x)

    x = numpy.array([4, 5, 6], dtype=numpy.float32)
    numpy.fft.rfft(x)


[FFTW]: <http://www.fftw.org/>
[NumPy]: <http://www.numpy.org/>
[pkg-config]: <https://www.freedesktop.org/wiki/Software/pkg-config/>
[pkgconf]: <http://pkgconf.org/>
[pytest]: <https://pytest.org/>
