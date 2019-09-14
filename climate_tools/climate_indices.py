""" According to ETCCDI (Expert Team on Climate Change Detection and Indices)
Link 1: http://etccdi.pacificclimate.org/list_27_indices.shtml
Link 2: http://etccdi.pacificclimate.org/docs/ETCCDMIndicesComparison1.pdf
"""

from typing import Tuple, List, Union, Callable
import operator
from itertools import groupby
import numpy as np
import pandas as pd
from pandas import Series
from pandas.core.groupby import DataFrameGroupBy, SeriesGroupBy


def is_valid_year_length(arr: pd.Series) -> bool:
    """Basic function to check the consumed array for its length and if it's one of the
    common year lengths (365, 366)

    Args:
        arr (pandas.Series): value array expected from return of pandas DataFrame groupby

    Returns:
        booL: True if one of plausible year lengths, False if not

    """
    if arr.size in [365, 366]:
        return True

    return False


def rle(arr: pd.Series) -> Tuple[List[float], List[int]]:
    """Function for runlength encoding that returns a tuple with the values and their individual runlength
    according to the input array. E.g. an array [0, 0, 1, 1] would return a tuple ([0, 1], [2, 2])

    Args:
        arr (pandas.Series): value array expected from return of pandas DataFrame groupby

    Returns:
        tuple: list of values and list of their respective runlength

    """
    values, lengths = [], []
    for k, g in groupby(arr):
        values.append(k)
        lengths.append(len(list(g)))

    return values, lengths


def number_of(arr: Union[Series, DataFrameGroupBy, SeriesGroupBy],
              num: float,
              op: Callable[[Series, float], List[bool]]) -> Union[float, int]:
    """Helper function to count numbers in an array according a given threshold and an operator

    Args:
        arr (pandas.Series): value array expected from return of pandas DataFrame groupby
        num (int, float): a number with what the array is compared with to receive a count
        op (operator): the operator that is used to compare the array with the operator

    Returns:
        np.nan or number: the count that results from the comparison

    """
    assert isinstance(arr, (Series, DataFrameGroupBy, SeriesGroupBy))
    assert isinstance(num, float)
    assert isinstance(op, (operator.lt, operator.le, operator.eq, operator.ne, operator.ge, operator.gt))

    if not is_valid_year_length(arr):
        return np.nan

    return int(np.sum(op(arr, num)))


def number_of_fd(tmin: Union[Series, DataFrameGroupBy, SeriesGroupBy]) -> Union[float, int]:
    """Function for count of frost days (days where minimum temperature lower then 0°C)

    Args:
        tmin (list): value array of minimum temperature

    Returns:
        np.nan or number: the count of frost days

    """
    assert isinstance(tmin, (Series, DataFrameGroupBy, SeriesGroupBy))

    op = operator.lt
    num = 0.0

    return number_of(tmin, num, op)


def number_of_sd(tmax: Union[Series, DataFrameGroupBy, SeriesGroupBy]) -> Union[float, int]:
    """Function for count of summer days (days where maximum temperature greater then 25°C)

    Args:
        tmax (list): value array of maximum temperature

    Returns:
        np.nan or number: the count of summer days

    """
    assert isinstance(tmax, (Series, DataFrameGroupBy, SeriesGroupBy))

    num = 25.0
    op = operator.gt

    return number_of(tmax, num, op)


def number_of_id(tmax: Union[Series, DataFrameGroupBy, SeriesGroupBy]) -> Union[float, int]:
    """Function for count of icing days (days where maximum temperature smaller then 0°C)

    Args:
        tmax (list): value array of maximum temperature

    Returns:
        np.nan or number: the count of icing days

    """
    assert isinstance(tmax, (Series, DataFrameGroupBy, SeriesGroupBy))

    op = operator.lt
    num = 0.0

    return number_of(tmax, num, op)


def number_of_tn(tmin: Union[Series, DataFrameGroupBy, SeriesGroupBy]) -> Union[float, int]:
    """Function for count of tropical nights (days where minimum temperature greater then 20°C)

    Args:
        tmin (list): value array of minimum temperature

    Returns:
        np.nan or number: the count of icing days

    """
    assert isinstance(tmin, (Series, DataFrameGroupBy, SeriesGroupBy))

    op = operator.gt
    num = 20.0

    return number_of(tmin, num, op)

# 5. Growing season length


def growing_season_length(tmean: Union[Series, DataFrameGroupBy, SeriesGroupBy]) -> Union[float, int]:
    """Function for determining the growing-season-length

    Args:
        tmean (list): value array of daily mean temperature

    Returns:
        np.nan or number: the count of icing days

    """
    assert isinstance(tmean, (Series, DataFrameGroupBy, SeriesGroupBy))

    if not is_valid_year_length(tmean):
        return np.nan

    num = 5.0
    min_length = 6

    # Begin of growing season
    values, lengths = rle(operator.gt(tmean, num))
    values, lengths = np.repeat(values, lengths), np.repeat(lengths, lengths)

    start_arr = np.where(values & operator.ge(lengths, min_length))[0]

    if not start_arr.size > 0:
        return 0

    start = start_arr[0]

    # End of growing season
    if tmean.size == 366:
        jday_1jul = 183

    if tmean.size == 365:
        jday_1jul = 182

    values, lengths = rle(operator.lt(tmean, num))
    values, lengths = np.repeat(values, lengths), np.repeat(lengths, lengths)

    end_arr = np.where(values & operator.ge(lengths, min_length))[0]

    if not end_arr.size > 0:
        return 0

    end = end_arr[np.where(end_arr > jday_1jul)]

    if not end:
        return 0

    gsl = end - start + 1

    return gsl


def rr10(prec: Union[Series, DataFrameGroupBy, SeriesGroupBy]) -> Union[float, int]:
    """Function for count of heavy precipitation (days where rr greater equal 10mm)

    Args:
        prec (list): value array of precipitation

    Returns:
        np.nan or number: the count of icing days

    """
    assert isinstance(prec, (Series, DataFrameGroupBy, SeriesGroupBy))

    op = operator.ge
    num = 10.0

    return number_of(prec, num, op)


def rr20(prec: Union[Series, DataFrameGroupBy, SeriesGroupBy]) -> Union[float, int]:
    """Function for count of heavy precipitation (days where rr greater equal 20mm)

    Args:
        prec (list): value array of precipitation

    Returns:
        np.nan or number: the count of icing days

    """
    assert isinstance(prec, (Series, DataFrameGroupBy, SeriesGroupBy))

    op = operator.ge
    num = 20.0

    return number_of(prec, num, op)


# 8. Number of consecutive dry days


def cdd(prec: Union[Series, DataFrameGroupBy, SeriesGroupBy]) -> Union[float, int]:
    """Function for determining greatest number of consecutive dry days (rr < 1mm)

    Args:
        prec (list): value array of precipitation

    Returns:
        np.nan or number: the count of icing days

    """
    assert isinstance(prec, (Series, DataFrameGroupBy, SeriesGroupBy))

    if not is_valid_year_length(prec):
        return np.nan

    num = 1.0

    values, lengths = rle(operator.lt(prec, num))

    return int(np.max(lengths[np.where(values)]))
