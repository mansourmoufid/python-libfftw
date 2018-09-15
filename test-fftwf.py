#!/usr/bin/env python

import functools
import numpy

import libfftw.fftwf
numpy.fft = libfftw.fftwf.FFT()


def test_fft():
    array = functools.partial(numpy.array, dtype=numpy.complex64)
    inputs = [
        array([1.0+0.0j, 4.0+0.0j, 2.0+0.0j, 3.0+0.0j]),
        array([5.0+0.0j, 4.0+0.0j, 7.0+0.0j, 6.0+0.0j]),
    ]
    outputs = [
        array([10.0+0.0j, -1.0-1.0j, -4.0+0.0j, -1.0+1.0j]),
        array([22.0+0.0j, -2.0+2.0j,  2.0+0.0j, -2.0-2.0j]),
    ]
    for x, Y in zip(inputs, outputs):
        X = numpy.fft.fft(x)
        assert numpy.all(numpy.abs(X - Y) < 1e-5)
        y = numpy.fft.ifft(X)
        assert numpy.all(numpy.abs(x - y) < 1e-5)


def test_rfft():
    array = functools.partial(numpy.array, dtype=numpy.complex64)
    inputs = [
        numpy.array([1.0, 2.0, 3.0, 4.0], dtype=numpy.float32),
        numpy.array([2.0, 3.0, 4.0, 1.0], dtype=numpy.float32),
    ]
    outputs = [
        array([10.0+0.j, -2.0+2.0j, -2.0+0.j,  0.0+0.0j]),
        array([10.0+0.j, -2.0-2.0j,  2.0+0.j,  0.0+0.0j]),
    ]
    for x, Y in zip(inputs, outputs):
        X = numpy.fft.rfft(x)
        assert numpy.all(numpy.abs(X - Y) < 1e-5)


if __name__ == '__main__':
    test_fft()
    test_rfft()
