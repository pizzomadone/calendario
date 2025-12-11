#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced search functionality for Italian Calendar
"""

import sqlite3
from database import DB_PATH


def search_all(query, filters=None):
    """
    Search across all content types

    Args:
        query: Search query string
        filters: Dict with optional filters (type, month, region, etc.)

    Returns:
        dict: Search results grouped by type
    """
    if not query or len(query) < 2:
        return {}

    query = query.strip()

    results = {
        'saints': search_saints(query, filters),
        'holidays': search_holidays(query, filters),
        'name_days': search_name_days(query),
        'events': search_events(query, filters),
        'proverbs': search_proverbs(query, filters),
        'recipes': search_recipes(query, filters),
        'tips': search_agricultural_tips(query, filters),
    }

    # Count total results
    results['total'] = sum(len(v) for v in results.values() if isinstance(v, list))

    return results


def search_saints(query, filters=None):
    """Search saints by name, biography, or patronage"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = '''
        SELECT * FROM saints
        WHERE name LIKE ? OR biography LIKE ? OR short_story LIKE ? OR patronage LIKE ?
    '''
    params = [f'%{query}%'] * 4

    if filters and 'month' in filters:
        sql += ' AND month = ?'
        params.append(filters['month'])

    sql += ' ORDER BY month, day LIMIT 50'

    results = cursor.execute(sql, params).fetchall()
    conn.close()

    return [dict(r) for r in results]


def search_holidays(query, filters=None):
    """Search holidays by name or description"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = '''
        SELECT * FROM holidays
        WHERE name LIKE ? OR description LIKE ?
    '''
    params = [f'%{query}%', f'%{query}%']

    if filters:
        if 'month' in filters:
            sql += ' AND month = ?'
            params.append(filters['month'])
        if 'region' in filters:
            sql += ' AND (region = ? OR region IS NULL)'
            params.append(filters['region'])
        if 'is_national' in filters:
            sql += ' AND is_national = ?'
            params.append(filters['is_national'])

    sql += ' ORDER BY month, day LIMIT 50'

    results = cursor.execute(sql, params).fetchall()
    conn.close()

    return [dict(r) for r in results]


def search_name_days(query):
    """Search name days"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = '''
        SELECT * FROM name_days
        WHERE name LIKE ?
        ORDER BY month, day
        LIMIT 50
    '''

    results = cursor.execute(sql, (f'%{query}%',)).fetchall()
    conn.close()

    return [dict(r) for r in results]


def search_events(query, filters=None):
    """Search historical events"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = '''
        SELECT * FROM historical_events
        WHERE title LIKE ? OR description LIKE ?
    '''
    params = [f'%{query}%', f'%{query}%']

    if filters and 'month' in filters:
        sql += ' AND month = ?'
        params.append(filters['month'])

    sql += ' ORDER BY year DESC, month, day LIMIT 50'

    results = cursor.execute(sql, params).fetchall()
    conn.close()

    return [dict(r) for r in results]


def search_proverbs(query, filters=None):
    """Search proverbs and quotes"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = '''
        SELECT * FROM proverbs
        WHERE text LIKE ? OR author LIKE ?
    '''
    params = [f'%{query}%', f'%{query}%']

    if filters:
        if 'month' in filters:
            sql += ' AND (month = ? OR month IS NULL)'
            params.append(filters['month'])
        if 'category' in filters:
            sql += ' AND category = ?'
            params.append(filters['category'])

    sql += ' LIMIT 50'

    results = cursor.execute(sql, params).fetchall()
    conn.close()

    return [dict(r) for r in results]


def search_recipes(query, filters=None):
    """Search recipes"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = '''
        SELECT * FROM recipes
        WHERE title LIKE ? OR description LIKE ? OR ingredients LIKE ?
    '''
    params = [f'%{query}%'] * 3

    if filters:
        if 'season' in filters:
            sql += ' AND season = ?'
            params.append(filters['season'])
        if 'region' in filters:
            sql += ' AND (region = ? OR region IS NULL)'
            params.append(filters['region'])
        if 'difficulty' in filters:
            sql += ' AND difficulty = ?'
            params.append(filters['difficulty'])

    sql += ' LIMIT 50'

    results = cursor.execute(sql, params).fetchall()
    conn.close()

    return [dict(r) for r in results]


def search_agricultural_tips(query, filters=None):
    """Search agricultural tips"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = '''
        SELECT * FROM agricultural_tips
        WHERE title LIKE ? OR description LIKE ?
    '''
    params = [f'%{query}%', f'%{query}%']

    if filters:
        if 'month' in filters:
            sql += ' AND month = ?'
            params.append(filters['month'])
        if 'category' in filters:
            sql += ' AND category = ?'
            params.append(filters['category'])

    sql += ' ORDER BY month LIMIT 50'

    results = cursor.execute(sql, params).fetchall()
    conn.close()

    return [dict(r) for r in results]


def get_suggestions(partial_query):
    """Get search suggestions based on partial query"""
    if not partial_query or len(partial_query) < 2:
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    suggestions = []

    # Saints names
    saints = cursor.execute('''
        SELECT DISTINCT name FROM saints WHERE name LIKE ? LIMIT 5
    ''', (f'%{partial_query}%',)).fetchall()
    suggestions.extend([{'text': s[0], 'type': 'Santo'} for s in saints])

    # Holiday names
    holidays = cursor.execute('''
        SELECT DISTINCT name FROM holidays WHERE name LIKE ? LIMIT 5
    ''', (f'%{partial_query}%',)).fetchall()
    suggestions.extend([{'text': h[0], 'type': 'Festività'} for h in holidays])

    # Name days
    names = cursor.execute('''
        SELECT DISTINCT name FROM name_days WHERE name LIKE ? LIMIT 5
    ''', (f'%{partial_query}%',)).fetchall()
    suggestions.extend([{'text': n[0], 'type': 'Onomastico'} for n in names])

    conn.close()

    return suggestions[:10]
