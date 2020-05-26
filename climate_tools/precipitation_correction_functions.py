from general_variables import MONTHS_SUMMER, MONTHS_WINTER, RICHTER_VALUES, WETTINGLOSS_VALS


def prec_correction_method1(precipitation,
                            month,
                            windspeed_1m,
                            temperature_air,
                            temperature_min):

    # Wind correction of precipitation
    if temperature_air < -27:
        wind_factor = 1 + (0.550 * windspeed_1m ** 1.40)
    elif temperature_air >= - 27 and temperature_air < -8:
        wind_factor = 1 + (0.280 * windspeed_1m ** 1.30)
    elif temperature_air >= - 8 and temperature_air < temperature_min:
        wind_factor = 1 + (0.150 * windspeed_1m ** 1.15)
    elif temperature_air >= temperature_min:
        wind_factor = min(1 + (0.015 * windspeed_1m ** 1.00),
                          1.12)

    # Wetting correction of precipitation
    for key in WETTINGLOSS_VALS:
        lower_limit, upper_limit = key
        if lower_limit <= precipitation <= upper_limit:
            if 5 <= month <= 10:
                wettingloss_value = WETTINGLOSS_VALS[key][0]
            else:
                wettingloss_value = WETTINGLOSS_VALS[key][1]
            break

    precipitation_corrected = (precipitation * wind_factor) - wettingloss_value

    return precipitation_corrected


def prec_correction_method2(precipitation,
                            month,
                            temperature_air,
                            horizon_shielding):
    if temperature_air > 3:
        if month in MONTHS_SUMMER:
            precipitation_type = 'RAIN_SUMMER'
        elif month in MONTHS_WINTER:
            precipitation_type = 'RAIN_WINTER'
    elif -0.7 <= temperature_air <= 3:
        precipitation_type = 'SLEET'
    elif temperature_air < -0.7:
        precipitation_type = 'SNOW'

    epsilon, b_values = RICHTER_VALUES[precipitation_type]

    b = b_values[horizon_shielding]

    precipitation_corrected = precipitation + b * precipitation ** epsilon

    return precipitation_corrected


def prec_areal_correction(precipitation,
                          correction_factor):
    return precipitation * correction_factor


def prec_height_correction_boundary(cor_val_absolute,
                                    cor_val_relative):
    cor_type_boundary = cor_val_absolute / cor_val_relative

    return cor_type_boundary


def prec_height_correction(precipitation_lower,
                           height_higher_station,
                           height_lower_station,
                           cor_boundary,
                           cor_val_absolute,
                           cor_val_relative):
    if precipitation_lower < cor_boundary:
        precipitation_higher = precipitation_lower + cor_val_absolute * \
            (height_higher_station - height_lower_station) / 100
    else:
        precipitation_higher = precipitation_lower * \
            (1 + cor_val_relative * (height_higher_station - height_lower_station) / 100)

    return precipitation_higher


if __name__ == "__main__":

    print(prec_correction_method1(precipitation=100,
                                  month=5,
                                  windspeed_1m=1,
                                  temperature_air=5,
                                  temperature_min=2))

    print(prec_correction_method2(precipitation=100,
                                  month=5,
                                  temperature_air=5,
                                  horizon_shielding='9.5D'))
