from numpy import Inf

SOLAR_CONST = 1367.0
GRAVITY = 9.81
GAS_CONSTANT = 287.0
HEAT_CAPACITY_WATER = 4186.8
MELTING_HEAT_WATER = 334000

GLOB_RAD_DAILY_PAR_a = 0.24
GLOB_RAD_DAILY_PAR_b_summer = 0.55
GLOB_RAD_DAILY_PAR_b_winter = 0.50
GLOB_RAD_DAILY_PAR_c = 0.15

GLOB_RAD_HOURLY_PAR_a = 0.19
GLOB_RAD_HOURLY_PAR_b = 0.45

MONTHS_SUMMER = [5, 6, 7, 8, 9, 10]
MONTHS_WINTER = [1, 2, 3, 4, 11, 12]

RICHTER_VALUES = {'RAIN_SUMMER': [0.38, {'2D': 0.345, '5D': 0.310, '9.5D': 0.280, '16D': 0.245}],
                  'RAIN_WINTER': [0.46, {'2D': 0.340, '5D': 0.280, '9.5D': 0.240, '16D': 0.190}],
                  'SLEET': [0.55, {'2D': 0.535, '5D': 0.390, '9.5D': 0.305, '16D': 0.185}],
                  'SNOW': [0.82, {'2D': 0.720, '5D': 0.510, '9.5D': 0.330, '16D': 0.210}]}

WETTINGLOSS_VALS = {(0, 0): (0, 0),
                    (0.1, 0.1): (0.07, 0.04),
                    (0.2, 0.2): (0.11, 0.06),
                    (0.3, 0.3): (0.13, 0.07),
                    (0.4, 0.4): (0.15, 0.08),
                    (0.5, 0.5): (0.16, 0.09),
                    (0.6, 0.8): (0.18, 0.10),
                    (0.9, 1.2): (0.20, 0.12),
                    (1.3, 1.7): (0.24, 0.14),
                    (1.8, 2.4): (0.27, 0.16),
                    (2.5, 3.4): (0.31, 0.18),
                    (3.5, 4.4): (0.34, 0.20),
                    (4.5, 6.0): (0.36, 0.22),
                    (6.1, 8.9): (0.41, 0.26),
                    (9.0, Inf): (0.47, 0.30)}

LAI_TYPICAL = {
    "SEALED": {"JAN": 10, "FEB": 10, "MAR": 10, "APR": 10, "MAY": 10, "JUN": 10, "JUL": 10, "AUG": 10, "SEP": 10, "OCT": 10, "NOV": 10, "DEC": 10},

    "ACRE": {"JAN": 0.3, "FEB": 0.3, "MAR": 1.0, "APR": 2.3, "MAY": 3.7, "JUN": 3.8, "JUL": 0.3, "AUG": 3.5, "SEP": 2.4, "OCT": 1.2, "NOV": 0.3, "DEC": 0.3},

    "WINEGROWING": {"JAN": 1.0, "FEB": 1.0, "MAR": 1.0, "APR": 1.5, "MAY": 2.0, "JUN": 3.5, "JUL": 4.0, "AUG": 4.0, "SEP": 4.0, "OCT": 1.5, "NOV": 1.0, "DEC": 1.0},

    "INTENSE_ORCHARDING": {"JAN": 2.0, "FEB": 2.0, "MAR": 2.0, "APR": 2.0, "MAY": 3.0, "JUN": 3.5, "JUL": 4.0, "AUG": 4.0, "SEP": 4.0, "OCT": 2.5, "NOV": 2.0, "DEC": 2.0},

    "FALLOW": {"JAN": 2.0, "FEB": 2.0, "MAR": 3.0, "APR": 4.0, "MAY": 5.0, "JUN": 5.0, "JUL": 5.0, "AUG": 5.0, "SEP": 5.0, "OCT": 3.0, "NOV": 2.5, "DEC": 2.0},

    "UNVEGETATED_UNSEALED": {"JAN": 0.0, "FEB": 0.0, "MAR": 0.0, "APR": 0.0, "MAY": 0.0, "JUN": 0.0, "JUL": 0.0, "AUG": 0.0, "SEP": 0.0, "OCT": 0.0, "NOV": 0.0, "DEC": 0.0},

    "INTENSIVE_GRASSLAND": {"JAN": 2.0, "FEB": 2.0, "MAR": 2.0, "APR": 3.0, "MAY": 3.5, "JUN": 4.0, "JUL": 4.0, "AUG": 4.0, "SEP": 3.5, "OCT": 3.0, "NOV": 2.5, "DEC": 2.0},

    "WETLANDS": {"JAN": 2.0, "FEB": 2.0, "MAR": 3.0, "APR": 4.0, "MAY": 5.0, "JUN": 5.0, "JUL": 5.0, "AUG": 5.0, "SEP": 5.0, "OCT": 3.0, "NOV": 2.5, "DEC": 2.0},

    "EXTENSIVE_GRASSLAND": {"JAN": 2.0, "FEB": 2.0, "MAR": 2.0, "APR": 3.0, "MAY": 3.5, "JUN": 4.0, "JUL": 4.0, "AUG": 4.0, "SEP": 3.5, "OCT": 3.0, "NOV": 2.5, "DEC": 2.0},

    "ARBORED": {"JAN": 2.0, "FEB": 2.0, "MAR": 3.0, "APR": 4.5, "MAY": 5.5, "JUN": 5.5, "JUL": 5.5, "AUG": 5.5, "SEP": 5.5, "OCT": 4.0, "NOV": 2.5, "DEC": 2.0},

    "CONIFER_FOREST": {"JAN": 11, "FEB": 11, "MAR": 11, "APR": 11, "MAY": 11, "JUN": 11, "JUL": 11, "AUG": 11, "SEP": 11, "OCT": 11, "NOV": 11, "DEC": 11},

    "BROADLEAF_FOREST": {"JAN": 0.5, "FEB": 0.5, "MAR": 1.5, "APR": 4.0, "MAY": 7.0, "JUN": 11, "JUL": 12, "AUG": 12, "SEP": 11, "OCT": 8.0, "NOV": 1.5, "DEC": 0.5},

    "MIXED_FOREST": {"JAN": 3.0, "FEB": 3.0, "MAR": 4.0, "APR": 6.0, "MAY": 8.0, "JUN": 11, "JUL": 11.5, "AUG": 11.5, "SEP": 11, "OCT": 9.0, "NOV": 4.0, "DEC": 3.0},

    "WATER": {"JAN": 0.0, "FEB": 0.0, "MAR": 0.0, "APR": 0.0, "MAY": 0.0, "JUN": 0.0, "JUL": 0.0, "AUG": 0.0, "SEP": 0.0, "OCT": 0.0, "NOV": 0.0, "DEC": 0.0}
}
