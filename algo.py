import numpy as np
from numba import njit

def naive_median(arr, i=None):
    if arr.size == 0:
        return 0
    if i is None:
        i = int(np.ceil(arr.size/2)-1)
    return np.sort(arr, kind='mergesort')[i]


def recurse_median(arr, i=None, sep=5):
    if arr.size == 0:
        return 0
    if i is None:
        i = int(np.ceil(arr.size/2)-1)
    if arr.size <= sep:
        return np.sort(arr, kind='mergesort')[i]

    part_ind = np.arange(sep, arr.size, sep)
    sublists = np.split(arr, part_ind)
    medians = np.array([recurse_median(sublist, sep=sep)
                        for sublist in sublists])

    pivot = recurse_median(medians, sep=sep)
    ref_pivot = np.nonzero(arr == pivot)[0][0]
    arr = np.delete(arr, ref_pivot)

    ind_pivot = np.nonzero(arr <= pivot)[0].size
    if i < ind_pivot:
        sub = arr[arr <= pivot]
        return recurse_median(sub, i, sep=sep)
    elif i > ind_pivot:
        sub = arr[arr > pivot]
        return recurse_median(sub, i-1-ind_pivot, sep=sep)
    else:
        return pivot


@njit('i1(i1[:], optional(i4))')
def c_naive_median(arr, i=None):
    if arr.size == 0:
        return 0

    if i is None:
        s = int(np.ceil(arr.size/2)-1)
    else:
        s = int(i)
    return np.sort(arr)[s]


@njit('i1(i1[:], optional(i4), optional(i4))')
def c_recurse_median(arr, i=None, sep=5):
    if arr.size == 0:
        return 0

    if i is None:
        s = int(np.ceil(arr.size/2)-1)
    else:
        s = int(i)

    if arr.size <= sep:
        return np.sort(arr)[s]

    part_ind = np.arange(sep, arr.size, sep)
    sublists = np.split(arr, part_ind)
    medians = np.array([c_recurse_median(sublist, i=None, sep=sep)
                                         for sublist in sublists])

    pivot = c_recurse_median(medians, i=None, sep=sep)
    ref_pivot = np.nonzero(arr == pivot)[0][0]
    arr = np.delete(arr, ref_pivot)
    
    ind_pivot = np.nonzero(arr <= pivot)[0].size
    if s < ind_pivot:
        sub = arr[arr <= pivot]
        return c_recurse_median(sub, i=s, sep=sep)
    elif s > ind_pivot:
        sub = arr[arr > pivot]
        return c_recurse_median(sub, i=s-1-ind_pivot, sep=sep)
    else:
        return int(pivot)
