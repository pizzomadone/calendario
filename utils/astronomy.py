#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Astronomical calculations for sun and seasonal information
"""

import ephem
from datetime import datetime, timedelta


# Rome coordinates as default (Italy's capital)
DEFAULT_LATITUDE = '41.9028'
DEFAULT_LONGITUDE = '12.4964'


def get_sun_info(date, latitude=DEFAULT_LATITUDE, longitude=DEFAULT_LONGITUDE):
    """
    Calculate sunrise, sunset, and day length for a given date and location

    Args:
        date: datetime object
        latitude: string latitude (default: Rome)
        longitude: string longitude (default: Rome)

    Returns:
        dict: Sun information
    """
    observer = ephem.Observer()
    observer.lat = latitude
    observer.lon = longitude
    observer.date = date

    sun = ephem.Sun()

    # Calculate sunrise and sunset
    try:
        sunrise = observer.next_rising(sun).datetime()
        sunset = observer.next_setting(sun).datetime()

        # Calculate day length
        day_length = sunset - sunrise

        # Calculate solar noon (when sun is highest)
        observer.date = date
        transit = observer.next_transit(sun).datetime()

        # Calculate twilight times
        observer.horizon = '-6'  # Civil twilight
        civil_dawn = observer.previous_rising(sun, use_center=True).datetime()
        civil_dusk = observer.next_setting(sun, use_center=True).datetime()

        observer.horizon = '-12'  # Nautical twilight
        nautical_dawn = observer.previous_rising(sun, use_center=True).datetime()
        nautical_dusk = observer.next_setting(sun, use_center=True).datetime()

        return {
            'sunrise': sunrise,
            'sunset': sunset,
            'day_length': day_length,
            'solar_noon': transit,
            'civil_dawn': civil_dawn,
            'civil_dusk': civil_dusk,
            'nautical_dawn': nautical_dawn,
            'nautical_dusk': nautical_dusk,
            'sunrise_str': sunrise.strftime('%H:%M'),
            'sunset_str': sunset.strftime('%H:%M'),
            'day_length_str': _format_timedelta(day_length)
        }
    except ephem.AlwaysUpError:
        return {
            'sunrise': None,
            'sunset': None,
            'day_length': None,
            'solar_noon': None,
            'message': 'Il sole non tramonta (sole di mezzanotte)'
        }
    except ephem.NeverUpError:
        return {
            'sunrise': None,
            'sunset': None,
            'day_length': None,
            'solar_noon': None,
            'message': 'Il sole non sorge (notte polare)'
        }


def _format_timedelta(td):
    """Format timedelta as HH:MM"""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours}h {minutes}m"


def get_season(date):
    """
    Determine the astronomical season for a given date

    Args:
        date: datetime object

    Returns:
        dict: Season information
    """
    year = date.year

    # Calculate equinoxes and solstices for the year
    spring_equinox = ephem.next_vernal_equinox(str(year - 1)).datetime()
    summer_solstice = ephem.next_summer_solstice(str(year - 1)).datetime()
    autumn_equinox = ephem.next_autumn_equinox(str(year - 1)).datetime()
    winter_solstice = ephem.next_winter_solstice(str(year - 1)).datetime()

    # Determine current season
    if spring_equinox <= date < summer_solstice:
        season = 'spring'
        season_italian = 'Primavera'
        emoji = '🌸'
        next_season = summer_solstice
        next_season_name = 'Estate'
    elif summer_solstice <= date < autumn_equinox:
        season = 'summer'
        season_italian = 'Estate'
        emoji = '☀️'
        next_season = autumn_equinox
        next_season_name = 'Autunno'
    elif autumn_equinox <= date < winter_solstice:
        season = 'autumn'
        season_italian = 'Autunno'
        emoji = '🍂'
        next_season = winter_solstice
        next_season_name = 'Inverno'
    else:
        season = 'winter'
        season_italian = 'Inverno'
        emoji = '❄️'
        # Next spring equinox
        next_season = ephem.next_vernal_equinox(str(year)).datetime()
        next_season_name = 'Primavera'

    return {
        'season': season,
        'season_italian': season_italian,
        'emoji': emoji,
        'next_season_date': next_season,
        'next_season_name': next_season_name,
        'spring_equinox': spring_equinox,
        'summer_solstice': summer_solstice,
        'autumn_equinox': autumn_equinox,
        'winter_solstice': winter_solstice
    }


def get_zodiac_sign(day, month):
    """
    Get the zodiac sign for a given date

    Args:
        day: int
        month: int

    Returns:
        dict: Zodiac information
    """
    zodiac_signs = [
        {'name': 'Capricorno', 'symbol': '♑', 'dates': 'dic 22 - gen 19', 'element': 'Terra'},
        {'name': 'Acquario', 'symbol': '♒', 'dates': 'gen 20 - feb 18', 'element': 'Aria'},
        {'name': 'Pesci', 'symbol': '♓', 'dates': 'feb 19 - mar 20', 'element': 'Acqua'},
        {'name': 'Ariete', 'symbol': '♈', 'dates': 'mar 21 - apr 19', 'element': 'Fuoco'},
        {'name': 'Toro', 'symbol': '♉', 'dates': 'apr 20 - mag 20', 'element': 'Terra'},
        {'name': 'Gemelli', 'symbol': '♊', 'dates': 'mag 21 - giu 20', 'element': 'Aria'},
        {'name': 'Cancro', 'symbol': '♋', 'dates': 'giu 21 - lug 22', 'element': 'Acqua'},
        {'name': 'Leone', 'symbol': '♌', 'dates': 'lug 23 - ago 22', 'element': 'Fuoco'},
        {'name': 'Vergine', 'symbol': '♍', 'dates': 'ago 23 - set 22', 'element': 'Terra'},
        {'name': 'Bilancia', 'symbol': '♎', 'dates': 'set 23 - ott 22', 'element': 'Aria'},
        {'name': 'Scorpione', 'symbol': '♏', 'dates': 'ott 23 - nov 21', 'element': 'Acqua'},
        {'name': 'Sagittario', 'symbol': '♐', 'dates': 'nov 22 - dic 21', 'element': 'Fuoco'},
    ]

    # Determine zodiac based on date
    if (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return zodiac_signs[0]
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return zodiac_signs[1]
    elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
        return zodiac_signs[2]
    elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return zodiac_signs[3]
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return zodiac_signs[4]
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return zodiac_signs[5]
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return zodiac_signs[6]
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return zodiac_signs[7]
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return zodiac_signs[8]
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return zodiac_signs[9]
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return zodiac_signs[10]
    else:  # (month == 11 and day >= 22) or (month == 12 and day <= 21)
        return zodiac_signs[11]


def get_day_info(date):
    """
    Get comprehensive day information including week number, day of year, etc.

    Args:
        date: datetime object

    Returns:
        dict: Day information
    """
    day_of_year = date.timetuple().tm_yday
    week_number = date.isocalendar()[1]
    days_in_year = 366 if _is_leap_year(date.year) else 365
    days_remaining = days_in_year - day_of_year

    # Italian day names
    italian_days = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']
    italian_day = italian_days[date.weekday()]

    return {
        'day_of_year': day_of_year,
        'days_in_year': days_in_year,
        'days_remaining': days_remaining,
        'week_number': week_number,
        'italian_day': italian_day,
        'is_weekend': date.weekday() >= 5,
        'is_leap_year': _is_leap_year(date.year)
    }


def _is_leap_year(year):
    """Check if a year is a leap year"""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
