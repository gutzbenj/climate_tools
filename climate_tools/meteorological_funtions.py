from math import exp, cos, acos, tan, sin, radians, log
from math import pi

from general_variables import SOLAR_CONST, GRAVITY, GAS_CONSTANT, HEAT_CAPACITY_WATER, MELTING_HEAT_WATER

from general_variables import GLOB_RAD_DAILY_PAR_a
from general_variables import GLOB_RAD_DAILY_PAR_b_summer
from general_variables import GLOB_RAD_DAILY_PAR_b_winter
from general_variables import GLOB_RAD_DAILY_PAR_c

from general_variables import GLOB_RAD_HOURLY_PAR_a
from general_variables import GLOB_RAD_HOURLY_PAR_b

from general_variables import MONTHS_SUMMER, MONTHS_WINTER


def get_sat_wvp(temperature_air):
    saturated_wvp = 6.1078 * \
        exp((17.08085 * temperature_air) / (234.175 + temperature_air))

    return saturated_wvp


def get_humidity(water_vapor_pressure,
                 temperature_air):
    humidity = water_vapor_pressure / get_sat_wvp(temperature_air)

    return humidity


def get_wvp(temperature_air,
            humidity):
    water_vapor_pressure = get_sat_wvp(temperature_air) * humidity

    return water_vapor_pressure


def get_sun_decl(julian_day):
    sun_decl = 0.41 * cos(2 * pi * (julian_day - 172) / 365)

    return sun_decl


def get_sunrise(julian_day,
                latitude):
    sun_decl = get_sun_decl(julian_day)
    sunrise = 12 / pi * acos(tan(sun_decl) * tan(latitude) +
                             0.0145 / (cos(sun_decl) * cos(latitude)))

    return sunrise


def get_pos_sun_dur(julian_day,
                    latitude):
    sunrise = get_sunrise(julian_day,
                          latitude)

    sunset = 24 - sunrise

    pos_sun_dur = sunset - sunrise

    return pos_sun_dur


def get_sun_rad(julian_day,
                latitude):
    pos_sun_dur = get_pos_sun_dur(julian_day,
                                  latitude)

    sun_decl = get_sun_decl(julian_day)

    sunrise = get_sunrise(julian_day,
                          latitude)

    sunset = 24 - sunrise

    sun_rad = SOLAR_CONST * (pos_sun_dur * sin(sun_decl) * sin(latitude) + 12 / pi * cos(
        sun_decl) * cos(latitude) * (sin(pi * sunrise / 12) - sin(pi * sunset / 12)))

    return sun_rad


def get_glob_rad_daily(julian_day,
                       month,
                       latitude,
                       sun_radiation_direct,
                       sunshine_duration,
                       a=GLOB_RAD_DAILY_PAR_a,
                       b_summer=GLOB_RAD_DAILY_PAR_b_summer,
                       b_winter=GLOB_RAD_DAILY_PAR_b_winter,
                       c=GLOB_RAD_DAILY_PAR_c):
    if month in MONTHS_SUMMER:
        b = b_summer
    elif month in MONTHS_WINTER:
        b = b_winter

    sun_rad = get_sun_rad(julian_day,
                          latitude)

    pos_sun_dur = get_pos_sun_dur(julian_day,
                                  latitude)

    glob_rad_daily = sun_rad * (sun_radiation_direct * (a + b * sunshine_duration /
                                                        pos_sun_dur) + c * (1 - sun_radiation_direct))

    return glob_rad_daily


def get_glob_rad_hourly(julian_day,
                        latitude,
                        sun_radiation_direct,
                        sunshine_duration,
                        a=GLOB_RAD_HOURLY_PAR_a,
                        b=GLOB_RAD_HOURLY_PAR_b):

    sun_rad = get_sun_rad(julian_day,
                          latitude)

    pos_sun_dur = get_pos_sun_dur(julian_day,
                                  latitude)

    glob_rad_hourly = sun_rad * (a + b * sunshine_duration / pos_sun_dur)

    return glob_rad_hourly


def get_air_pressure(p1,
                     h1,
                     h2,
                     T1,
                     T2):

    return exp(-(GRAVITY * (h2 - h1)) / (GAS_CONSTANT * ((T1 + T2) / 2)) + log(p1))


def get_windspeed_height(h1,
                         h2,
                         u1,
                         z0):
    u2 = log(h2 / z0) / log(h1 / z0) * u1

    return u2


def get_evapotranspiration(e_pot,
                           e_izp,
                           e_a):
    e_ai = ((e_pot - e_izp) / e_pot) * e_a + e_izp

    return e_ai


def get_eb_snowpack_dd(prec,
                       t_air,
                       t_boundary,
                       ta,
                       degree_day_factor,
                       also_snowmelt):
    if also_snowmelt:
        t_prec = max(t_air - t_boundary, 0)
        t_ref = t_boundary
    else:
        t_prec = max(t_air, 0)
        t_ref = 0

    hf_prec = (prec * t_prec * HEAT_CAPACITY_WATER) / (ta * 3600)

    # pot_snowmelt_dd = degree_day_factor * (ta / 24) * (t_air - t_ref)

    hf_dd = degree_day_factor * (t_air - t_ref) * \
        MELTING_HEAT_WATER / (24 * 3600)

    return hf_dd + hf_prec


def get_eb_snowpack_knauf(a0,
                          a1,
                          v,
                          t_air):

    hf_sense = (a0 + a1 * v) * t_air

    return hf_ground + hf_prec + hf_sense


if __name__ == "__main__":

    # print(get_glob_rad_daily(180, 6, radians(54), 1, 5))
    # print(get_glob_rad_hourly(180, 6, radians(54), 5))

    print(get_air_pressure(1013.25,
                           0,
                           1000,
                           293.15,
                           273.15))
