#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Additional routes for new features:
- Search
- PDF Export
- Proverbs
- Recipes
- Agricultural Tips
- Regional Holidays
"""

from bottle import request, response
from datetime import datetime
import sqlite3

from database import DB_PATH
from utils.search import search_all, get_suggestions
from utils.pdf_export import generate_month_pdf, generate_year_pdf, generate_day_pdf
from utils.seo import generate_meta_tags, generate_breadcrumb_schema


def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def setup_extended_routes(app):
    """Add new routes to the app"""

    # SEARCH ROUTES
    @app.route('/cerca')
    @app.route('/search')
    def search_page():
        """Search page"""
        query = request.query.get('q', '').strip()
        filters = {}

        if request.query.get('month'):
            filters['month'] = int(request.query.get('month'))
        if request.query.get('region'):
            filters['region'] = request.query.get('region')

        results = {}
        if query:
            results = search_all(query, filters)

        # SEO
        title = f"Cerca: {query}" if query else "Ricerca"
        description = "Cerca santi, festività, onomastici, ricette e consigli agricoli nel calendario italiano."
        keywords = "cerca, ricerca, calendario, santi, festività"

        meta_tags = generate_meta_tags(title, description, '/cerca', keywords=keywords)

        return app.jinja_env.get_template('search.html').render(
            query=query,
            results=results,
            filters=filters,
            meta_tags=meta_tags,
            datetime=datetime
        )

    @app.route('/api/search/suggestions')
    def search_suggestions():
        """API endpoint for search suggestions"""
        query = request.query.get('q', '').strip()
        suggestions = get_suggestions(query) if query else []

        response.content_type = 'application/json'
        import json
        return json.dumps(suggestions, ensure_ascii=False)

    # PDF EXPORT ROUTES
    @app.route('/pdf/mese/<year:int>/<month:int>')
    def export_month_pdf(year, month):
        """Export month calendar as PDF"""
        try:
            pdf_buffer = generate_month_pdf(year, month)

            italian_months = ['', 'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
                            'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']

            response.content_type = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename="calendario-{italian_months[month]}-{year}.pdf"'

            return pdf_buffer.getvalue()
        except Exception as e:
            return f"Errore nella generazione del PDF: {str(e)}"

    @app.route('/pdf/anno/<year:int>')
    def export_year_pdf(year):
        """Export year calendar as PDF"""
        try:
            pdf_buffer = generate_year_pdf(year)

            response.content_type = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename="calendario-{year}.pdf"'

            return pdf_buffer.getvalue()
        except Exception as e:
            return f"Errore nella generazione del PDF: {str(e)}"

    @app.route('/pdf/giorno/<year:int>/<month:int>/<day:int>')
    def export_day_pdf(year, month, day):
        """Export day details as PDF"""
        try:
            pdf_buffer = generate_day_pdf(year, month, day)

            response.content_type = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename="calendario-{year}-{month:02d}-{day:02d}.pdf"'

            return pdf_buffer.getvalue()
        except Exception as e:
            return f"Errore nella generazione del PDF: {str(e)}"

    # PROVERBS ROUTE
    @app.route('/proverbi')
    def list_proverbs():
        """List all proverbs and quotes"""
        conn = get_db()
        cursor = conn.cursor()

        # Get all proverbs
        proverbs = cursor.execute('''
            SELECT * FROM proverbs ORDER BY month, day, id
        ''').fetchall()

        conn.close()

        # Group by category
        proverbs_by_category = {}
        for proverb in proverbs:
            category = proverb['category'] or 'Altro'
            if category not in proverbs_by_category:
                proverbs_by_category[category] = []
            proverbs_by_category[category].append(proverb)

        # SEO
        title = "Proverbi e Citazioni Italiane"
        description = "Raccolta di proverbi tradizionali italiani, detti popolari e citazioni famose."
        keywords = "proverbi, detti, citazioni, saggezza popolare, tradizioni"

        meta_tags = generate_meta_tags(title, description, '/proverbi', keywords=keywords)

        breadcrumb = generate_breadcrumb_schema([
            ('Home', '/'),
            ('Proverbi', None)
        ])

        return app.jinja_env.get_template('proverbs.html').render(
            proverbs_by_category=proverbs_by_category,
            meta_tags=meta_tags,
            breadcrumb=breadcrumb,
            datetime=datetime
        )

    # RECIPES ROUTE
    @app.route('/ricette')
    def list_recipes():
        """List all seasonal recipes"""
        conn = get_db()
        cursor = conn.cursor()

        season_filter = request.query.get('stagione')

        if season_filter:
            recipes = cursor.execute('''
                SELECT * FROM recipes WHERE season = ? ORDER BY month
            ''', (season_filter,)).fetchall()
        else:
            recipes = cursor.execute('''
                SELECT * FROM recipes ORDER BY season, month
            ''').fetchall()

        conn.close()

        # Group by season
        recipes_by_season = {}
        for recipe in recipes:
            season = recipe['season']
            if season not in recipes_by_season:
                recipes_by_season[season] = []
            recipes_by_season[season].append(recipe)

        # SEO
        title = "Ricette Stagionali Italiane"
        description = "Ricette tradizionali italiane divise per stagione. Scopri i piatti tipici di ogni periodo dell'anno."
        keywords = "ricette, cucina italiana, piatti stagionali, tradizioni culinarie"

        meta_tags = generate_meta_tags(title, description, '/ricette', keywords=keywords)

        breadcrumb = generate_breadcrumb_schema([
            ('Home', '/'),
            ('Ricette', None)
        ])

        return app.jinja_env.get_template('recipes.html').render(
            recipes_by_season=recipes_by_season,
            season_filter=season_filter,
            meta_tags=meta_tags,
            breadcrumb=breadcrumb,
            datetime=datetime
        )

    @app.route('/ricetta/<recipe_id:int>')
    def recipe_detail(recipe_id):
        """Recipe detail page"""
        conn = get_db()
        cursor = conn.cursor()

        recipe = cursor.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()

        conn.close()

        if not recipe:
            return app.jinja_env.get_template('error.html').render(
                message="Ricetta non trovata",
                datetime=datetime
            )

        # SEO
        title = recipe['title']
        description = recipe['description']
        keywords = f"ricetta, {recipe['title']}, cucina italiana, {recipe['season']}"

        meta_tags = generate_meta_tags(title, description, f'/ricetta/{recipe_id}', keywords=keywords)

        breadcrumb = generate_breadcrumb_schema([
            ('Home', '/'),
            ('Ricette', '/ricette'),
            (recipe['title'], None)
        ])

        return app.jinja_env.get_template('recipe_detail.html').render(
            recipe=recipe,
            meta_tags=meta_tags,
            breadcrumb=breadcrumb,
            datetime=datetime
        )

    # AGRICULTURAL TIPS ROUTE
    @app.route('/orto')
    @app.route('/agricoltura')
    def agricultural_calendar():
        """Agricultural calendar with monthly tips"""
        conn = get_db()
        cursor = conn.cursor()

        month_filter = request.query.get('mese')

        if month_filter:
            tips = cursor.execute('''
                SELECT * FROM agricultural_tips WHERE month = ? ORDER BY category
            ''', (int(month_filter),)).fetchall()
        else:
            tips = cursor.execute('''
                SELECT * FROM agricultural_tips ORDER BY month, category
            ''').fetchall()

        conn.close()

        # Group by month
        tips_by_month = {}
        for tip in tips:
            month = tip['month']
            if month not in tips_by_month:
                tips_by_month[month] = []
            tips_by_month[month].append(tip)

        italian_months = ['', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
                         'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']

        # SEO
        title = "Calendario dell'Orto e Agricoltura"
        description = "Consigli mensili per l'orto e l'agricoltura. Scopri cosa seminare, potare e raccogliere ogni mese."
        keywords = "orto, agricoltura, semina, calendario lunare, coltivazione"

        meta_tags = generate_meta_tags(title, description, '/orto', keywords=keywords)

        breadcrumb = generate_breadcrumb_schema([
            ('Home', '/'),
            ('Orto e Agricoltura', None)
        ])

        return app.jinja_env.get_template('agricultural.html').render(
            tips_by_month=tips_by_month,
            italian_months=italian_months,
            month_filter=month_filter,
            meta_tags=meta_tags,
            breadcrumb=breadcrumb,
            datetime=datetime
        )

    # REGIONAL HOLIDAYS ROUTE
    @app.route('/feste/regionali')
    def regional_holidays():
        """List regional Italian holidays"""
        conn = get_db()
        cursor = conn.cursor()

        region_filter = request.query.get('regione')

        if region_filter:
            holidays = cursor.execute('''
                SELECT * FROM holidays WHERE region = ? ORDER BY month, day
            ''', (region_filter,)).fetchall()
        else:
            holidays = cursor.execute('''
                SELECT * FROM holidays WHERE region IS NOT NULL ORDER BY region, month, day
            ''').fetchall()

        # Get list of regions
        regions = cursor.execute('''
            SELECT DISTINCT region FROM holidays WHERE region IS NOT NULL ORDER BY region
        ''').fetchall()

        conn.close()

        # Group by region
        holidays_by_region = {}
        for holiday in holidays:
            region = holiday['region']
            if region not in holidays_by_region:
                holidays_by_region[region] = []
            holidays_by_region[region].append(holiday)

        italian_months = ['', 'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
                         'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']

        # SEO
        title = "Festività Regionali Italiane"
        description = "Feste patronali e celebrazioni regionali italiane. Scopri le tradizioni locali di ogni regione."
        keywords = "feste regionali, patroni, tradizioni locali, sagre, celebrazioni"

        meta_tags = generate_meta_tags(title, description, '/feste/regionali', keywords=keywords)

        breadcrumb = generate_breadcrumb_schema([
            ('Home', '/'),
            ('Festività', '/feste'),
            ('Festività Regionali', None)
        ])

        return app.jinja_env.get_template('regional_holidays.html').render(
            holidays_by_region=holidays_by_region,
            regions=[r['region'] for r in regions],
            region_filter=region_filter,
            italian_months=italian_months,
            meta_tags=meta_tags,
            breadcrumb=breadcrumb,
            datetime=datetime
        )
