#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Italian Calendar Web Application
Main Bottle application with routing and controllers
"""

from bottle import Bottle, route, run, static_file, request, response, redirect, jinja2_template as template
from datetime import datetime, timedelta
import sqlite3
import calendar
import os
from jinja2 import Environment, FileSystemLoader

# Import utilities
from utils.lunar import get_moon_phase, get_moon_calendar_for_month
from utils.astronomy import get_sun_info, get_season, get_zodiac_sign, get_day_info
from utils.seo import (generate_meta_tags, generate_breadcrumb_schema, generate_event_schema,
                       generate_article_schema, generate_person_schema, slugify,
                       get_day_url, get_month_url, get_year_url, get_saint_url,
                       get_italian_month_name, generate_sitemap_xml)
from database import DB_PATH


app = Bottle()

# Setup Jinja2
template_path = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = Environment(loader=FileSystemLoader(template_path))

# Add datetime to Jinja2 globals
jinja_env.globals.update({
    'datetime': datetime,
})


# Static files
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    """Serve static files (CSS, JS, images)"""
    return static_file(filepath, root='./static')


# Database helper
def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Routes
@app.route('/')
def home():
    """Home page - today's date"""
    today = datetime.now()
    return redirect(get_day_url(today.year, today.month, today.day))


@app.route('/oggi')
def today():
    """Alternative route for today"""
    today = datetime.now()
    return redirect(get_day_url(today.year, today.month, today.day))


@app.route('/giorno/<year:int>/<month:int>/<day:int>')
@app.route('/giorno/<year:int>/<month:int>/<day:int>/<slug>')
def show_day(year, month, day, slug=None):
    """Show detailed view of a specific day"""
    try:
        date = datetime(year, month, day)
    except ValueError:
        return template('error', message="Data non valida")

    # Get data from database
    conn = get_db()
    cursor = conn.cursor()

    # Get saint(s) of the day
    saints = cursor.execute('''
        SELECT * FROM saints WHERE day = ? AND month = ?
    ''', (day, month)).fetchall()

    # Get holidays
    holidays = cursor.execute('''
        SELECT * FROM holidays WHERE day = ? AND month = ? AND (year IS NULL OR year = ?)
    ''', (day, month, year)).fetchall()

    # Get name days
    name_days = cursor.execute('''
        SELECT DISTINCT name FROM name_days WHERE day = ? AND month = ?
        ORDER BY name
    ''', (day, month)).fetchall()

    # Get historical events
    events = cursor.execute('''
        SELECT * FROM historical_events WHERE day = ? AND month = ?
        ORDER BY year DESC
    ''', (day, month)).fetchall()

    conn.close()

    # Get astronomical data
    moon = get_moon_phase(date)
    sun = get_sun_info(date)
    season = get_season(date)
    zodiac = get_zodiac_sign(day, month)
    day_info = get_day_info(date)

    # Format date information
    italian_months = ['', 'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
                      'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
    italian_days = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica']

    formatted_date = f"{italian_days[date.weekday()]} {day} {italian_months[month]} {year}"

    # SEO data
    saint_names = ', '.join([s['name'] for s in saints]) if saints else 'Calendario'
    title = f"{day} {italian_months[month].capitalize()} {year}"
    if saints:
        title += f" - {saint_names}"

    description = f"Calendario del {formatted_date}."
    if saints:
        description += f" Santo del giorno: {saint_names}."
    if holidays:
        description += f" Festività: {', '.join([h['name'] for h in holidays])}."
    description += f" Fase lunare: {moon['phase_italian']}. {zodiac['name']}."

    keywords = f"calendario, {day} {italian_months[month]}, {year}, {saint_names}, fasi lunari, onomastici"

    meta_tags = generate_meta_tags(title, description, get_day_url(year, month, day), date=date, keywords=keywords)

    breadcrumb = generate_breadcrumb_schema([
        ('Home', '/'),
        (str(year), get_year_url(year)),
        (italian_months[month].capitalize(), get_month_url(year, month)),
        (str(day), None)
    ])

    # Navigation links
    prev_day = date - timedelta(days=1)
    next_day = date + timedelta(days=1)

    return template('day',
                    date=date,
                    formatted_date=formatted_date,
                    saints=saints,
                    holidays=holidays,
                    name_days=name_days,
                    events=events,
                    moon=moon,
                    sun=sun,
                    season=season,
                    zodiac=zodiac,
                    day_info=day_info,
                    meta_tags=meta_tags,
                    breadcrumb=breadcrumb,
                    prev_day=prev_day,
                    next_day=next_day,
                    year=year,
                    month=month,
                    day=day,
                    italian_month=italian_months[month])


@app.route('/mese/<year:int>/<month:int>')
@app.route('/mese/<year:int>/<month:int>/<month_name>')
def show_month(year, month, month_name=None):
    """Show calendar view of a month"""
    try:
        if not 1 <= month <= 12:
            raise ValueError
    except ValueError:
        return template('error', message="Mese non valido")

    # Get month calendar
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)

    # Get data for the month
    conn = get_db()
    cursor = conn.cursor()

    # Get all saints for this month
    saints_in_month = {}
    saints = cursor.execute('''
        SELECT day, name, slug FROM saints WHERE month = ?
    ''', (month,)).fetchall()
    for saint in saints:
        if saint['day'] not in saints_in_month:
            saints_in_month[saint['day']] = []
        saints_in_month[saint['day']].append({'name': saint['name'], 'slug': saint['slug']})

    # Get all holidays for this month
    holidays_in_month = {}
    holidays = cursor.execute('''
        SELECT day, name, is_national FROM holidays
        WHERE month = ? AND (year IS NULL OR year = ?)
    ''', (month, year)).fetchall()
    for holiday in holidays:
        if holiday['day'] not in holidays_in_month:
            holidays_in_month[holiday['day']] = []
        holidays_in_month[holiday['day']].append({'name': holiday['name'], 'is_national': holiday['is_national']})

    conn.close()

    # Get moon phases for the month
    moon_phases = get_moon_calendar_for_month(year, month)

    # Create moon phase lookup by day
    moon_by_day = {}
    for phase in moon_phases:
        day = phase['date'].day
        if day not in moon_by_day:
            moon_by_day[day] = []
        moon_by_day[day].append(phase)

    # Italian month name
    italian_months = ['', 'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
                      'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
    italian_month = italian_months[month]

    # SEO
    title = f"{italian_month.capitalize()} {year}"
    description = f"Calendario {italian_month} {year} con santi, feste, fasi lunari e onomastici per ogni giorno del mese."
    keywords = f"calendario {italian_month} {year}, santi {italian_month}, feste {italian_month}"

    meta_tags = generate_meta_tags(title, description, get_month_url(year, month), keywords=keywords)

    breadcrumb = generate_breadcrumb_schema([
        ('Home', '/'),
        (str(year), get_year_url(year)),
        (italian_month.capitalize(), None)
    ])

    # Navigation
    if month == 1:
        prev_month = (year - 1, 12)
    else:
        prev_month = (year, month - 1)

    if month == 12:
        next_month = (year + 1, 1)
    else:
        next_month = (year, month + 1)

    return template('month',
                    year=year,
                    month=month,
                    italian_month=italian_month,
                    month_days=month_days,
                    saints_in_month=saints_in_month,
                    holidays_in_month=holidays_in_month,
                    moon_by_day=moon_by_day,
                    moon_phases=moon_phases,
                    meta_tags=meta_tags,
                    breadcrumb=breadcrumb,
                    prev_month=prev_month,
                    next_month=next_month)


@app.route('/anno/<year:int>')
def show_year(year):
    """Show overview of entire year"""
    if year < 1 or year > 9999:
        return template('error', message="Anno non valido")

    # Get all months
    italian_months = ['', 'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
                      'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']

    # Get holidays for the year
    conn = get_db()
    cursor = conn.cursor()

    holidays = cursor.execute('''
        SELECT * FROM holidays
        WHERE year IS NULL OR year = ?
        ORDER BY month, day
    ''', (year,)).fetchall()

    conn.close()

    # Get season information
    season_info = get_season(datetime(year, 6, 1))  # Mid-year reference

    # SEO
    title = f"Calendario {year}"
    description = f"Calendario completo dell'anno {year} con tutti i santi, le festività italiane, le fasi lunari e gli onomastici."
    keywords = f"calendario {year}, festività {year}, santi {year}"

    meta_tags = generate_meta_tags(title, description, get_year_url(year), keywords=keywords)

    breadcrumb = generate_breadcrumb_schema([
        ('Home', '/'),
        (str(year), None)
    ])

    return template('year',
                    year=year,
                    months=list(range(1, 13)),
                    italian_months=italian_months,
                    holidays=holidays,
                    season_info=season_info,
                    meta_tags=meta_tags,
                    breadcrumb=breadcrumb)


@app.route('/santo/<slug>')
def show_saint(slug):
    """Show detailed information about a saint"""
    conn = get_db()
    cursor = conn.cursor()

    saint = cursor.execute('''
        SELECT * FROM saints WHERE slug = ?
    ''', (slug,)).fetchone()

    conn.close()

    if not saint:
        return template('error', message="Santo non trovato")

    # Italian month name
    italian_months = ['', 'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
                      'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']

    # SEO
    title = saint['name']
    description = saint['short_story']
    keywords = f"{saint['name']}, santo, {saint['day']} {italian_months[saint['month']]}, {saint['patronage']}"

    meta_tags = generate_meta_tags(title, description, get_saint_url(slug), keywords=keywords)

    person_schema = generate_person_schema(saint['name'], saint['biography'], job_title="Santo")

    breadcrumb = generate_breadcrumb_schema([
        ('Home', '/'),
        ('Santi', '/santi'),
        (saint['name'], None)
    ])

    return template('saint',
                    saint=saint,
                    italian_month=italian_months[saint['month']],
                    meta_tags=meta_tags,
                    person_schema=person_schema,
                    breadcrumb=breadcrumb)


@app.route('/santi')
def list_saints():
    """List all saints"""
    conn = get_db()
    cursor = conn.cursor()

    saints = cursor.execute('''
        SELECT * FROM saints ORDER BY month, day
    ''', ).fetchall()

    conn.close()

    # Group by month
    italian_months = ['', 'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
                      'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']

    saints_by_month = {}
    for saint in saints:
        month = saint['month']
        if month not in saints_by_month:
            saints_by_month[month] = []
        saints_by_month[month].append(saint)

    # SEO
    title = "Tutti i Santi"
    description = "Elenco completo dei santi del calendario italiano con biografie e storie."
    keywords = "santi, calendario santi, santi italiani, agiografia"

    meta_tags = generate_meta_tags(title, description, '/santi', keywords=keywords)

    breadcrumb = generate_breadcrumb_schema([
        ('Home', '/'),
        ('Santi', None)
    ])

    return template('saints_list',
                    saints_by_month=saints_by_month,
                    italian_months=italian_months,
                    meta_tags=meta_tags,
                    breadcrumb=breadcrumb)


@app.route('/feste')
def list_holidays():
    """List all Italian holidays"""
    conn = get_db()
    cursor = conn.cursor()

    holidays = cursor.execute('''
        SELECT * FROM holidays WHERE year IS NULL ORDER BY month, day
    ''', ).fetchall()

    conn.close()

    italian_months = ['', 'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
                      'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']

    # SEO
    title = "Festività Italiane"
    description = "Elenco completo delle festività comandate e feste nazionali italiane."
    keywords = "festività italiane, feste comandate, giorni festivi, feste nazionali"

    meta_tags = generate_meta_tags(title, description, '/feste', keywords=keywords)

    breadcrumb = generate_breadcrumb_schema([
        ('Home', '/'),
        ('Festività', None)
    ])

    return template('holidays_list',
                    holidays=holidays,
                    italian_months=italian_months,
                    meta_tags=meta_tags,
                    breadcrumb=breadcrumb)


@app.route('/sitemap.xml')
def sitemap():
    """Generate sitemap.xml"""
    urls = []

    # Home
    urls.append({
        'loc': '/',
        'changefreq': 'daily',
        'priority': '1.0'
    })

    # Current year months
    current_year = datetime.now().year
    for year in range(current_year - 1, current_year + 2):
        # Year page
        urls.append({
            'loc': get_year_url(year),
            'changefreq': 'weekly',
            'priority': '0.8'
        })

        # Month pages
        for month in range(1, 13):
            urls.append({
                'loc': get_month_url(year, month),
                'changefreq': 'weekly',
                'priority': '0.7'
            })

    # Saints and holidays lists
    urls.append({
        'loc': '/santi',
        'changefreq': 'monthly',
        'priority': '0.9'
    })

    urls.append({
        'loc': '/feste',
        'changefreq': 'monthly',
        'priority': '0.9'
    })

    # Individual saints
    conn = get_db()
    cursor = conn.cursor()
    saints = cursor.execute('SELECT slug FROM saints').fetchall()
    for saint in saints:
        urls.append({
            'loc': get_saint_url(saint['slug']),
            'changefreq': 'monthly',
            'priority': '0.6'
        })
    conn.close()

    response.content_type = 'application/xml'
    return generate_sitemap_xml(urls)


@app.route('/robots.txt')
def robots():
    """Generate robots.txt"""
    response.content_type = 'text/plain'
    return f"""User-agent: *
Allow: /

Sitemap: {request.urlparts.scheme}://{request.urlparts.netloc}/sitemap.xml
"""


@app.error(404)
def error404(error):
    """404 error page"""
    return template('error', message="Pagina non trovata")


@app.error(500)
def error500(error):
    """500 error page"""
    return template('error', message="Errore del server")


if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists(DB_PATH):
        print("📊 Initializing database...")
        from database import init_db
        init_db()

    print("🚀 Starting Calendario Italiano...")
    print("📅 Open your browser at http://localhost:8080")
    run(app, host='localhost', port=8080, debug=True, reloader=True)
