#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lunar calendar calculations using ephem library
"""

import ephem
from datetime import datetime, timedelta


MOON_PHASES = {
    'new': '🌑 Luna Nuova',
    'waxing_crescent': '🌒 Luna Crescente',
    'first_quarter': '🌓 Primo Quarto',
    'waxing_gibbous': '🌔 Gibbosa Crescente',
    'full': '🌕 Luna Piena',
    'waning_gibbous': '🌖 Gibbosa Calante',
    'last_quarter': '🌗 Ultimo Quarto',
    'waning_crescent': '🌘 Luna Calante'
}


def get_moon_phase(date):
    """
    Calculate moon phase for a given date

    Args:
        date: datetime object

    Returns:
        dict: Moon phase information
    """
    moon = ephem.Moon(date)

    # Calculate illumination (0-100%)
    illumination = moon.phase

    # Determine phase name based on illumination and whether waxing or waning
    phase_name = _get_phase_name(date, illumination)

    # Get next phase dates
    next_phases = _get_next_phases(date)

    return {
        'phase': phase_name,
        'phase_italian': MOON_PHASES.get(phase_name, 'Luna'),
        'illumination': round(illumination, 1),
        'age': _get_moon_age(date),
        'next_new': next_phases['new_moon'],
        'next_full': next_phases['full_moon'],
        'next_first_quarter': next_phases['first_quarter'],
        'next_last_quarter': next_phases['last_quarter']
    }


def _get_phase_name(date, illumination):
    """Determine the phase name based on illumination and position"""
    # Calculate previous and next new moon to determine if waxing or waning
    prev_new = ephem.previous_new_moon(date)
    next_new = ephem.next_new_moon(date)
    prev_full = ephem.previous_full_moon(date)

    is_waxing = prev_new > prev_full

    if illumination < 1:
        return 'new'
    elif illumination < 48 and is_waxing:
        return 'waxing_crescent'
    elif 48 <= illumination < 52 and is_waxing:
        return 'first_quarter'
    elif illumination < 98 and is_waxing:
        return 'waxing_gibbous'
    elif illumination >= 98:
        return 'full'
    elif illumination > 52 and not is_waxing:
        return 'waning_gibbous'
    elif 48 <= illumination <= 52 and not is_waxing:
        return 'last_quarter'
    else:
        return 'waning_crescent'


def _get_moon_age(date):
    """Calculate moon age in days (0-29.53)"""
    prev_new = ephem.previous_new_moon(date)
    prev_new_datetime = ephem.Date(prev_new).datetime()
    age = (date - prev_new_datetime).days
    return age


def _get_next_phases(date):
    """Get dates of next moon phases"""
    next_new = ephem.next_new_moon(date)
    next_full = ephem.next_full_moon(date)
    next_first = ephem.next_first_quarter_moon(date)
    next_last = ephem.next_last_quarter_moon(date)

    return {
        'new_moon': ephem.Date(next_new).datetime(),
        'full_moon': ephem.Date(next_full).datetime(),
        'first_quarter': ephem.Date(next_first).datetime(),
        'last_quarter': ephem.Date(next_last).datetime()
    }


def get_moon_calendar_for_month(year, month):
    """
    Get all moon phases for a specific month

    Args:
        year: int
        month: int

    Returns:
        list: List of phase changes in the month
    """
    from calendar import monthrange

    start_date = datetime(year, month, 1)
    _, last_day = monthrange(year, month)
    end_date = datetime(year, month, last_day, 23, 59, 59)

    phases = []

    # Find all phase changes in the month
    current = start_date

    # New moons
    try:
        nm = ephem.next_new_moon(current - timedelta(days=1))
        while True:
            nm_date = ephem.Date(nm).datetime()
            if nm_date > end_date:
                break
            if nm_date >= start_date:
                phases.append({
                    'date': nm_date,
                    'phase': 'new',
                    'name': '🌑 Luna Nuova'
                })
            nm = ephem.next_new_moon(nm)
    except:
        pass

    # Full moons
    try:
        fm = ephem.next_full_moon(current - timedelta(days=1))
        while True:
            fm_date = ephem.Date(fm).datetime()
            if fm_date > end_date:
                break
            if fm_date >= start_date:
                phases.append({
                    'date': fm_date,
                    'phase': 'full',
                    'name': '🌕 Luna Piena'
                })
            fm = ephem.next_full_moon(fm)
    except:
        pass

    # First quarter
    try:
        fq = ephem.next_first_quarter_moon(current - timedelta(days=1))
        while True:
            fq_date = ephem.Date(fq).datetime()
            if fq_date > end_date:
                break
            if fq_date >= start_date:
                phases.append({
                    'date': fq_date,
                    'phase': 'first_quarter',
                    'name': '🌓 Primo Quarto'
                })
            fq = ephem.next_first_quarter_moon(fq)
    except:
        pass

    # Last quarter
    try:
        lq = ephem.next_last_quarter_moon(current - timedelta(days=1))
        while True:
            lq_date = ephem.Date(lq).datetime()
            if lq_date > end_date:
                break
            if lq_date >= start_date:
                phases.append({
                    'date': lq_date,
                    'phase': 'last_quarter',
                    'name': '🌗 Ultimo Quarto'
                })
            lq = ephem.next_last_quarter_moon(lq)
    except:
        pass

    # Sort by date
    phases.sort(key=lambda x: x['date'])

    return phases
