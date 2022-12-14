# -*- coding: utf-8 -*-
import itertools
from typing import Iterable, Iterator, Tuple, Set


def ranges_to_set(lst: Iterable[Tuple[int, int]]) -> Set[int]:
    """
    Convert a list of ranges to a set of numbers::

    >>> ranges = [(1,3), (5,6)]
    >>> sorted(list(ranges_to_set(ranges)))
    [1, 2, 3, 5, 6]

    """
    return set(itertools.chain(*(range(x[0], x[1] + 1) for x in lst)))


def to_ranges(lst: Iterable[int]) -> Iterator[Tuple[int, int]]:
    """
    Convert a list of numbers to a list of ranges::

    >>> numbers = [1,2,3,5,6]
    >>> list(to_ranges(numbers))
    [(1, 3), (5, 6)]

    """
    for a, b in itertools.groupby(enumerate(lst), lambda t: t[1] - t[0]):
        c = list(b)
        yield c[0][1], c[-1][1]
