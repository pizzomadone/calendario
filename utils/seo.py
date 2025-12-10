#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO utilities for calendar application
"""

import json
from datetime import datetime
from urllib.parse import quote


SITE_NAME = "Calendario Italiano"
SITE_URL = "http://localhost:8080"  # Change in production
SITE_DESCRIPTION = "Calendario completo italiano con santi, fasi lunari, festività comandate, onomastici e eventi storici"


def generate_meta_tags(title, description, url, image=None, keywords=None, date=None):
    """
    Generate HTML meta tags for SEO

    Args:
        title: Page title
        description: Page description
        url: Page URL
        image: Optional image URL
        keywords: Optional comma-separated keywords
        date: Optional datetime object for articles

    Returns:
        str: HTML meta tags
    """
    full_title = f"{title} | {SITE_NAME}"
    full_url = f"{SITE_URL}{url}"

    meta_tags = f'''
    <title>{full_title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords or 'calendario, italia, santi, feste, luna'}">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="{'article' if date else 'website'}">
    <meta property="og:url" content="{full_url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="{SITE_NAME}">
    {f'<meta property="og:image" content="{image}">' if image else ''}
    {f'<meta property="article:published_time" content="{date.isoformat()}">' if date else ''}

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{full_url}">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    {f'<meta name="twitter:image" content="{image}">' if image else ''}

    <!-- Canonical -->
    <link rel="canonical" href="{full_url}">
    '''

    return meta_tags


def generate_breadcrumb_schema(items):
    """
    Generate JSON-LD breadcrumb schema

    Args:
        items: List of tuples (name, url)

    Returns:
        str: JSON-LD script tag
    """
    breadcrumb_list = []
    for idx, (name, url) in enumerate(items, 1):
        breadcrumb_list.append({
            "@type": "ListItem",
            "position": idx,
            "name": name,
            "item": f"{SITE_URL}{url}" if url else None
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": breadcrumb_list
    }

    return f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'


def generate_event_schema(name, start_date, description, location=None):
    """
    Generate JSON-LD event schema for holidays

    Args:
        name: Event name
        start_date: datetime object
        description: Event description
        location: Optional location

    Returns:
        str: JSON-LD script tag
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": name,
        "startDate": start_date.isoformat(),
        "description": description,
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "eventStatus": "https://schema.org/EventScheduled"
    }

    if location:
        schema["location"] = {
            "@type": "Place",
            "name": location,
            "address": {
                "@type": "PostalAddress",
                "addressCountry": "IT"
            }
        }

    return f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'


def generate_article_schema(headline, date_published, description, author="Calendario Italiano"):
    """
    Generate JSON-LD article schema

    Args:
        headline: Article headline
        date_published: datetime object
        description: Article description
        author: Author name

    Returns:
        str: JSON-LD script tag
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "datePublished": date_published.isoformat(),
        "author": {
            "@type": "Organization",
            "name": author
        },
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME
        },
        "description": description
    }

    return f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'


def generate_person_schema(name, description, birth_date=None, death_date=None, job_title=None):
    """
    Generate JSON-LD person schema for saints

    Args:
        name: Saint name
        description: Biography
        birth_date: Optional birth date
        death_date: Optional death date
        job_title: Optional role/title

    Returns:
        str: JSON-LD script tag
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": name,
        "description": description
    }

    if birth_date:
        schema["birthDate"] = birth_date
    if death_date:
        schema["deathDate"] = death_date
    if job_title:
        schema["jobTitle"] = job_title

    return f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'


def slugify(text):
    """
    Convert text to URL-friendly slug

    Args:
        text: Text to slugify

    Returns:
        str: Slugified text
    """
    # Italian-specific character replacements
    replacements = {
        'à': 'a', 'è': 'e', 'é': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
        'À': 'a', 'È': 'e', 'É': 'e', 'Ì': 'i', 'Ò': 'o', 'Ù': 'u',
        "'": '', ' ': '-', '.': '', ',': '', '!': '', '?': ''
    }

    slug = text.lower()
    for old, new in replacements.items():
        slug = slug.replace(old, new)

    # Remove any remaining non-alphanumeric characters except hyphens
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')

    # Remove multiple consecutive hyphens
    while '--' in slug:
        slug = slug.replace('--', '-')

    # Remove leading/trailing hyphens
    slug = slug.strip('-')

    return slug


def generate_sitemap_xml(urls):
    """
    Generate XML sitemap

    Args:
        urls: List of dicts with 'loc', 'lastmod', 'changefreq', 'priority'

    Returns:
        str: XML sitemap
    """
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url_info in urls:
        xml += '  <url>\n'
        xml += f'    <loc>{SITE_URL}{url_info["loc"]}</loc>\n'
        if 'lastmod' in url_info:
            xml += f'    <lastmod>{url_info["lastmod"]}</lastmod>\n'
        if 'changefreq' in url_info:
            xml += f'    <changefreq>{url_info["changefreq"]}</changefreq>\n'
        if 'priority' in url_info:
            xml += f'    <priority>{url_info["priority"]}</priority>\n'
        xml += '  </url>\n'

    xml += '</urlset>'
    return xml


def get_italian_month_name(month_number):
    """Get Italian month name from number"""
    months = [
        '', 'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
        'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'
    ]
    return months[month_number] if 1 <= month_number <= 12 else ''


def get_day_url(year, month, day, slug=None):
    """Generate SEO-friendly URL for a specific day"""
    month_name = get_italian_month_name(month)
    if slug:
        return f"/giorno/{year}/{month:02d}/{day:02d}/{slug}"
    return f"/giorno/{year}/{month:02d}/{day:02d}"


def get_month_url(year, month):
    """Generate SEO-friendly URL for a month"""
    month_name = get_italian_month_name(month)
    return f"/mese/{year}/{month:02d}/{month_name}"


def get_year_url(year):
    """Generate SEO-friendly URL for a year"""
    return f"/anno/{year}"


def get_saint_url(slug):
    """Generate SEO-friendly URL for a saint"""
    return f"/santo/{slug}"
