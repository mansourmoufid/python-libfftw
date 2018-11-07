#!/usr/bin/env python

import ctypes
import numpy

from . import libfftwf


FFTW_BACKWARD = 1
FFTW_ESTIMATE = 1 << 6
FFTW_FORWARD = -1
FFTW_MEASURE = 0


class FFTWFComplex(ctypes.Structure):
    '''typedef float fftwf_complex[2];'''
    _fields_ = [('r', ctypes.c_float), ('i', ctypes.c_float)]


class FFTWFPlanStructure(ctypes.Structure):
    '''
    struct fftwf_plan_s {
        plan *pln;
        problem *prb;
        int sign;
    };
    '''
    _fields_ = [
        ('pln', ctypes.c_void_p),
        ('prb', ctypes.c_void_p),
        ('sign', ctypes.c_int),
    ]


'''
typedef struct fftwf_plan_s *fftwf_plan;
'''
FFTWFPlan = ctypes.POINTER(FFTWFPlanStructure)


'''
fftwf_plan fftwf_plan_dft_1d(int, fftwf_complex *, fftwf_complex *,
    int, unsigned);
'''
fftwf_plan_dft_1d = libfftwf.fftwf_plan_dft_1d
fftwf_plan_dft_1d.restype = FFTWFPlan
fftwf_plan_dft_1d.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(FFTWFComplex),
    ctypes.POINTER(FFTWFComplex),
    ctypes.c_int,
    ctypes.c_uint,
]

'''
fftwf_plan fftwf_plan_dft_r2c_1d(int, float *, fftwf_complex *, unsigned);
'''
fftwf_plan_dft_r2c_1d = libfftwf.fftwf_plan_dft_r2c_1d
fftwf_plan_dft_r2c_1d.restype = FFTWFPlan
fftwf_plan_dft_r2c_1d.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(FFTWFComplex),
    ctypes.c_uint,
]

'''
fftwf_plan fftwf_plan_dft_c2r_1d(int, fftwf_complex *, float *, unsigned);
'''
fftwf_plan_dft_c2r_1d = libfftwf.fftwf_plan_dft_c2r_1d
fftwf_plan_dft_c2r_1d.restype = FFTWFPlan
fftwf_plan_dft_c2r_1d.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(FFTWFComplex),
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_uint,
]

'''
void fftwf_destroy_plan(fftwf_plan);
'''
fftwf_destroy_plan = libfftwf.fftwf_destroy_plan
fftwf_destroy_plan.restype = None
fftwf_destroy_plan.argtypes = [FFTWFPlan]

'''
void fftwf_execute(const fftwf_plan);
'''
fftwf_execute = libfftwf.fftwf_execute
fftwf_execute.restype = None
fftwf_execute.argtypes = [FFTWFPlan]

'''
void fftwf_execute_dft(const fftwf_plan, fftwf_complex *, fftwf_complex *);
'''
fftwf_execute_dft = libfftwf.fftwf_execute_dft
fftwf_execute_dft.restype = None
fftwf_execute_dft.argtypes = [
    FFTWFPlan,
    ctypes.POINTER(FFTWFComplex),
    ctypes.POINTER(FFTWFComplex),
]

'''
void fftwf_execute_dft_r2c(const fftwf_plan, float *, fftwf_complex *);
'''
fftwf_execute_dft_r2c = libfftwf.fftwf_execute_dft_r2c
fftwf_execute_dft_r2c.restype = None
fftwf_execute_dft_r2c.argtypes = [
    FFTWFPlan,
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(FFTWFComplex),
]

'''
void fftwf_execute_dft_c2r(const fftwf_plan, fftwf_complex *, float *);
'''
fftwf_execute_dft_c2r = libfftwf.fftwf_execute_dft_c2r
fftwf_execute_dft_c2r.restype = None
fftwf_execute_dft_c2r.argtypes = [
    FFTWFPlan,
    ctypes.POINTER(FFTWFComplex),
    ctypes.POINTER(ctypes.c_float),
]


def data(x):
    if not isinstance(x, numpy.ndarray):
        raise ValueError
    if x.dtype not in [numpy.float32, numpy.complex64]:
        raise ValueError
    if x.dtype == numpy.float32:
        return ctypes.cast(x.ctypes.data, ctypes.POINTER(ctypes.c_float))
    if x.dtype == numpy.complex64:
        return ctypes.cast(x.ctypes.data, ctypes.POINTER(FFTWFComplex))


class FFT(object):

    dtypes = {
        'c2c': (numpy.complex64, numpy.complex64),
        'r2c': (numpy.float32, numpy.complex64),
        'c2r': (numpy.complex64, numpy.float32),
    }

    def __init__(self):
        self.plans = {}
        self.destroy_plan = fftwf_destroy_plan

    def plan(self, x, X):
        if not isinstance(x, numpy.ndarray):
            raise ValueError
        if not isinstance(X, numpy.ndarray):
            raise ValueError
        if (x.dtype, X.dtype) not in self.dtypes.values():
            raise ValueError
        n = x.size
        flags = FFTW_ESTIMATE
        if (x.dtype, X.dtype) == self.dtypes['r2c']:
            return (
                fftwf_plan_dft_r2c_1d(n, data(x), data(X), flags),
                fftwf_plan_dft_c2r_1d(n, data(X), data(x), flags),
            )
        if (x.dtype, X.dtype) == self.dtypes['c2c']:
            return (
                fftwf_plan_dft_1d(n, data(x), data(X), FFTW_FORWARD, flags),
                fftwf_plan_dft_1d(n, data(x), data(X), FFTW_BACKWARD, flags),
            )

    def fft(self, x):
        X = numpy.zeros(x.size, dtype=numpy.complex64)
        if not (x.dtype, X.dtype) == self.dtypes['c2c']:
            raise ValueError
        if (x.dtype, X.dtype, x.size) not in self.plans:
            self.plans[(x.dtype, X.dtype, x.size)] = self.plan(x, X)
        plan = self.plans[(x.dtype, X.dtype, x.size)][0]
        fftwf_execute_dft(plan, data(x), data(X))
        return X

    def ifft(self, X):
        x = numpy.zeros(X.size, dtype=numpy.complex64)
        if not (X.dtype, x.dtype) == self.dtypes['c2c']:
            raise ValueError
        if (x.dtype, X.dtype, x.size) not in self.plans:
            self.plans[(x.dtype, X.dtype, x.size)] = self.plan(x, X)
        plan = self.plans[(x.dtype, X.dtype, x.size)][1]
        fftwf_execute_dft(plan, data(X), data(x))
        x *= 1.0 / x.size
        return x

    def rfft(self, x):
        X = numpy.zeros(x.size, dtype=numpy.complex64)
        if not (x.dtype, X.dtype) == self.dtypes['r2c']:
            raise ValueError
        if (x.dtype, X.dtype, x.size) not in self.plans:
            self.plans[(x.dtype, X.dtype, x.size)] = self.plan(x, X)
        plan = self.plans[(x.dtype, X.dtype, x.size)][0]
        fftwf_execute_dft_r2c(plan, data(x), data(X))
        return X

    def irfft(self, X, n=None):
        x = numpy.zeros(X.size, dtype=numpy.float32)
        if not (X.dtype, x.dtype) == self.dtypes['c2r']:
            raise ValueError
        if (x.dtype, X.dtype, x.size) not in self.plans:
            self.plans[(x.dtype, X.dtype, x.size)] = self.plan(x, X)
        plan = self.plans[(x.dtype, X.dtype, x.size)][1]
        fftwf_execute_dft_c2r(plan, data(X), data(x))
        x *= 1.0 / x.size
        return x

    def __del__(self):
        for plan in self.plans:
            self.destroy_plan(self.plans[plan][0])
            self.destroy_plan(self.plans[plan][1])
        pass


if __name__ == '__main__':
    pass
