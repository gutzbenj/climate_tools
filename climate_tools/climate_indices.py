""" According to ETCCDI (Expert Team on Climate Change Detection and Indices)
Link 1: http://etccdi.pacificclimate.org/list_27_indices.shtml
Link 2: http://etccdi.pacificclimate.org/docs/ETCCDMIndicesComparison1.pdf
"""

from typing import Tuple, List, Union, Callable
import operator
from itertools import groupby
import calendar
import numpy as np
import pandas as pd
# from pandas import Series
# from pandas.core.groupby import DataFrameGroupBy, SeriesGroupBy

# TYPING_UNION_AGGREGATION = Union[pd.Series,
#                                  pd.core.groupby.DataFrameGroupBy,
#                                  pd.core.groupby.SeriesGroupBy]

DAY_OF_YEAR_29_FEB = 60


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


def number_of(arr: pd.Series,
              num: float,
              op: Callable[[pd.Series, float], List[bool]]) -> Union[float, int]:
    """Helper function to count numbers in an array according a given threshold and an operator

    Args:
        arr (pandas.Series): value array expected from return of pandas DataFrame groupby
        num (int, float): a number with what the array is compared with to receive a count
        op (operator): the operator that is used to compare the array with the operator

    Returns:
        np.nan or number: the count that results from the comparison

    """
    assert isinstance(arr, pd.Series)
    assert isinstance(num, float)
    assert isinstance(op, (operator.lt, operator.le, operator.eq, operator.ne, operator.ge, operator.gt))

    if not is_valid_year_length(arr):
        return np.nan

    return int(np.sum(op(arr, num)))


def number_of_fd(tmin: pd.Series) -> Union[float, int]:
    """Function for count of frost days (days where minimum temperature lower then 0°C)

    Args:
        tmin (pd.Series): value array of minimum temperature

    Returns:
        np.nan or number: the count of frost days

    """
    if not isinstance(tmin, pd.Series):
        raise TypeError("Error: expecting pandas.Series as array.")

    op = operator.lt
    num = 0.0

    return number_of(tmin, num, op)


def number_of_sd(tmax: pd.Series) -> Union[float, int]:
    """Function for count of summer days (days where maximum temperature greater then 25°C)

    Args:
        tmax (pd.Series): value array of maximum temperature

    Returns:
        np.nan or number: the count of summer days

    """
    if not isinstance(tmax, pd.Series):
        raise TypeError("Error: expecting pandas.Series as array.")

    num = 25.0
    op = operator.gt

    return number_of(tmax, num, op)


def consecutive_fd(tmin: pd.Series) -> Union[float, int]:
    """Function for determining greatest number of consecutive frost days (tmin < 0°C)

    Args:
        tmin (pd.Series): value array of daily minimum temperature

    Returns:
        np.nan or number: the count of icing days

    """
    if not isinstance(tmin, pd.Series):
        raise TypeError("Error: expecting pandas.Series as array.")

    if not is_valid_year_length(tmin):
        return np.nan

    num = 0.0

    values, lengths = rle(operator.lt(tmin, num))

    return int(np.max(np.array(lengths)[np.where(values)]))


def consecutive_sd(tmax: pd.Series) -> Union[float, int]:
    """Function for determining greatest number of consecutive summer days (tmax > 25°C)

    Args:
        tmax (pd.Series): value array of daily minimum temperature

    Returns:
        np.nan or number: the count of icing days

    """
    if not isinstance(tmax, pd.Series):
        raise TypeError("Error: expecting pandas.Series as array.")

    if not is_valid_year_length(tmax):
        return np.nan

    num = 25.0

    values, lengths = rle(operator.gt(tmax, num))

    return int(np.max(np.array(lengths)[np.where(values)]))


def sum_of_hdd(tmean: pd.Series) -> Union[float, int]:
    """Function for determining heating degree days (sum of [17°C - tmean] for all days where tmean < 17°C)

    Args:
        tmean (pd.Series): value array of daily minimum temperature

    Returns:
        np.nan or number: the sum of degree difference

    """
    if not isinstance(tmean, pd.Series):
        raise TypeError("Error: expecting pandas.Series as array.")

    if not is_valid_year_length(tmean):
        return np.nan

    num = 17.0

    return np.sum(num - tmean[operator.lt(tmean, num)]).item()


def number_of_id(tmax: pd.Series) -> Union[float, int]:
    """Function for count of icing days (days where maximum temperature smaller then 0°C)

    Args:
        tmax (pd.Series): value array of maximum temperature

    Returns:
        np.nan or number: the count of icing days

    """
    if not isinstance(tmax, pd.Series):
        raise TypeError("Error: expecting pandas.Series as array.")

    op = operator.lt
    num = 0.0

    return number_of(tmax, num, op)


def number_of_tn(tmin: pd.Series) -> Union[float, int]:
    """Function for count of tropical nights (days where minimum temperature greater then 20°C)

    Args:
        tmin (pd.Series): value array of minimum temperature

    Returns:
        np.nan or number: the count of icing days

    """
    if not isinstance(tmin, pd.Series):
        raise TypeError("Error: expecting pandas.Series as array.")

    op = operator.gt
    num = 20.0

    return number_of(tmin, num, op)


def calculate_percentile_threshold(timeseries: pd.DataFrame,
                                   percentile: float,
                                   reference_period: Tuple[int, int],
                                   window: int,
                                   min_percentage: float) -> pd.Series:
    """Function for count of tropical nights (days where minimum temperature greater then 20°C)

    Args:
        timeseries (pd.DataFrame) -
        percentile (float) -
        reference_period (tuple) -
        window (int) -
        min_percentage (float) -

    Returns:
        np.nan or number: the count of icing days

    """

    if not isinstance(timeseries, pd.DataFrame):
        raise TypeError()
    if not isinstance(percentile, float):
        raise TypeError()
    if not isinstance(reference_period, tuple):
        raise TypeError()
    if not len(reference_period) == 2:
        raise ValueError()
    if not (isinstance(reference_period[0], int) and isinstance(reference_period[1], int)):
        raise TypeError()
    if not (reference_period[1] - reference_period[0] + 1) == 30:
        raise ValueError()
    if not isinstance(window, int):
        raise TypeError()
    if not window > 0:
        raise ValueError()
    if not isinstance(min_percentage, float):
        raise TypeError()
    if not 0 <= min_percentage <= 1:
        raise ValueError()

    timeseries = timeseries.copy()
    timeseries.columns = ["DATE", "VALUES"]

    start_date = pd.to_datetime(f"{reference_period[0]}-01-01")
    end_date = pd.to_datetime(f"{reference_period[1]}-12-31")

    date_operations = pd.DataFrame({"DATE": pd.date_range(start_date, end_date)})
    date_operations["LEAPYEAR"] = date_operations["DATE"].dt.year.apply(calendar.isleap)
    date_operations["DAYOFYEAR"] = date_operations["DATE"].dt.dayofyear

    date_operations.loc[date_operations["LEAPYEAR"] &
                        (date_operations["DAYOFYEAR"] >= DAY_OF_YEAR_29_FEB), "DAYOFYEAR"] -= 1

    daterange_extended = pd.date_range(start_date - pd.Timedelta(days=int(window / 2)),
                                       end_date + pd.Timedelta(days=int(window / 2)))

    timeseries = pd.merge(pd.DataFrame({"DATE": daterange_extended}),
                          timeseries)

    timeseries.iloc[:, 1] = timeseries.iloc[:, 1].rolling(window, center=True).mean()

    days_of_year = range(1, 366)

    thresholds = []
    for day_of_year in days_of_year:
        selection_of_timeseries = timeseries.loc[date_operations["DAYOFYEAR"].isin([day_of_year]), "VALUES"]

        percentage_of_values = selection_of_timeseries.agg(lambda x: x.notna().sum() / x.size).item()

        if percentage_of_values < min_percentage:
            thresholds.append(np.nan)
            continue

        thresholds.append(selection_of_timeseries[selection_of_timeseries.notna()].quantile([percentile]).item())

    return pd.Series(thresholds)


def fix_timeseries_for_leapyear(timeseries: pd.Series) -> pd.Series:
    """Function for count of tropical nights (days where minimum temperature greater then 20°C)

    Args:
        timeseries (pd.Series) -

    Returns:
        np.nan or number: the count of icing days

    """

    if not isinstance(timeseries, pd.Series):
        raise TypeError("Error: expecting pandas.Series as array.")

    if not is_valid_year_length(timeseries):
        return np.nan

    return pd.concat([timeseries[:DAY_OF_YEAR_29_FEB],
                      timeseries[[DAY_OF_YEAR_29_FEB]].repeat(2),
                      timeseries[(DAY_OF_YEAR_29_FEB + 1):]]).reset_index(drop=True)


def _number_of_thresholds(data: pd.Series,
                          thresholds: pd.Series):
    assert isinstance(data, pd.Series), "Error: 'data' is not of type pandas.Series"
    assert isinstance(thresholds, pd.Series), "Error: 'thresholds' is not of type pandas.Series"

    if not is_valid_year_length(data):
        return np.nan

    if data.size > thresholds.size:
        thresholds = fix_timeseries_for_leapyear(thresholds)

    values, lengths = rle(pd.Series(data.reset_index(drop=True) < thresholds.reset_index(drop=True)))

    _number_of_vals = (np.array(values) & operator.ge(np.array(lengths), 6)).nonzero()[0]

    if not _number_of_vals.any():
        return np.nan

    return np.sum(_number_of_vals)


def number_of_cn(tmin: pd.Series,
                 thresholds: pd.Series) -> Union[float, int]:
    """Function for count of tropical nights (days where minimum temperature greater then 20°C)

    Args:
        tmin (pd.Series): value array of minimum temperature
        thresholds (pd.Series) -

    Returns:
        np.nan or number: the count of icing days

    """

    if not isinstance(tmin, pd.Series):
        raise TypeError("Error: expecting pandas.Series as array.")
    if not isinstance(thresholds, pd.Series):
        raise TypeError("Error: expecting pandas.Series as array.")

    return _number_of_thresholds(tmin, thresholds)


def number_of_cd(tmean):
    # todo implement function for cold days
    pass


def number_of_wn(tmin):
    # todo implement function for warm nights
    pass


def number_of_wd(tmax_or_tmean):
    # todo implement function for warm days
    pass


def growing_season_length(tmean: pd.Series) -> Union[float, int]:
    """Function for determining the growing-season-length

    Args:
        tmean (list): value array of daily mean temperature

    Returns:
        np.nan or number: the count of icing days

    """
    assert isinstance(tmean, pd.Series)

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
    else:  # tmean.size == 365:
        jday_1jul = 182

    values, lengths = rle(operator.lt(tmean, num))
    values, lengths = np.repeat(values, lengths), np.repeat(lengths, lengths)

    end_arr = (values & operator.ge(lengths, min_length)).nonzero()[0]

    if not end_arr.size > 0:
        return 0

    end = end_arr[(end_arr > jday_1jul).nonzero()]

    if not end:
        return 0

    gsl = end - start + 1

    return gsl


def rr10(prec: pd.Series) -> Union[float, int]:
    """Function for count of heavy precipitation (days where rr greater equal 10mm)

    Args:
        prec (list): value array of precipitation

    Returns:
        np.nan or number: the count of icing days

    """
    assert isinstance(prec, pd.Series)

    op = operator.ge
    num = 10.0

    return number_of(prec, num, op)


def rr20(prec: pd.Series) -> Union[float, int]:
    """Function for count of heavy precipitation (days where rr greater equal 20mm)

    Args:
        prec (list): value array of precipitation

    Returns:
        np.nan or number: the count of icing days

    """
    assert isinstance(prec, pd.Series)

    op = operator.ge
    num = 20.0

    return number_of(prec, num, op)


# 8. Number of consecutive dry days


def consecutive_dd(prec: pd.Series) -> Union[float, int]:
    """Function for determining greatest number of consecutive dry days (rr < 1mm)

    Args:
        prec (list): value array of precipitation

    Returns:
        np.nan or number: the count of icing days

    """
    assert isinstance(prec, pd.Series)

    if not is_valid_year_length(prec):
        return np.nan

    num = 1.0

    values, lengths = rle(operator.lt(prec, num))

    return int(np.max(lengths[np.array(values).nonzero()]))
