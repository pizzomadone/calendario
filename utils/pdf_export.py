#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF export functionality for Italian Calendar
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import calendar
from datetime import datetime
import sqlite3
from database import DB_PATH
from io import BytesIO


def generate_month_pdf(year, month):
    """
    Generate PDF calendar for a specific month

    Args:
        year: int
        month: int

    Returns:
        BytesIO: PDF file in memory
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           topMargin=2*cm, bottomMargin=2*cm,
                           leftMargin=2*cm, rightMargin=2*cm)

    # Container for PDF elements
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2563eb'),
        alignment=TA_CENTER,
        spaceAfter=30,
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    # Italian month names
    italian_months = ['', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
                     'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']

    # Title
    title = Paragraph(f"<b>{italian_months[month]} {year}</b>", title_style)
    elements.append(title)

    subtitle = Paragraph("Calendario Italiano", subtitle_style)
    elements.append(subtitle)
    elements.append(Spacer(1, 1*cm))

    # Create calendar grid
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)

    # Get data from database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get saints for this month
    saints_data = {}
    saints = cursor.execute('SELECT day, name FROM saints WHERE month = ?', (month,)).fetchall()
    for saint in saints:
        day = saint['day']
        if day not in saints_data:
            saints_data[day] = []
        saints_data[day].append(saint['name'])

    # Get holidays
    holidays_data = {}
    holidays = cursor.execute(
        'SELECT day, name, is_national FROM holidays WHERE month = ? AND (year IS NULL OR year = ?)',
        (month, year)
    ).fetchall()
    for holiday in holidays:
        day = holiday['day']
        holidays_data[day] = holiday['name']

    conn.close()

    # Calendar table data
    table_data = []

    # Header row with day names
    header_row = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom']
    table_data.append(header_row)

    # Data rows
    for week in month_days:
        row = []
        for day in week:
            if day == 0:
                row.append('')
            else:
                cell_content = f"{day}\n"

                # Add saint if present
                if day in saints_data:
                    saint_names = saints_data[day]
                    cell_content += f"{saint_names[0][:15]}...\n" if len(saint_names[0]) > 15 else f"{saint_names[0]}\n"

                # Add holiday if present
                if day in holidays_data:
                    cell_content += f"🎉 {holidays_data[day][:12]}..."

                row.append(cell_content.strip())
        table_data.append(row)

    # Create table
    table = Table(table_data, colWidths=[2.5*cm]*7, rowHeights=[1*cm] + [2.5*cm]*len(month_days))

    # Table style
    table_style = TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        # Data cells
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),

        # Weekend columns (Saturday and Sunday)
        ('BACKGROUND', (5, 1), (5, -1), colors.HexColor('#fef3c7')),
        ('BACKGROUND', (6, 1), (6, -1), colors.HexColor('#fef3c7')),
    ])

    table.setStyle(table_style)
    elements.append(table)

    # Add saints list
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph("<b>Santi del Mese</b>", styles['Heading2']))
    elements.append(Spacer(1, 0.5*cm))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    saints = cursor.execute(
        'SELECT day, name, short_story FROM saints WHERE month = ? ORDER BY day',
        (month,)
    ).fetchall()

    for saint in saints:
        saint_text = f"<b>{saint['day']} {italian_months[month]}</b> - {saint['name']}: {saint['short_story'][:150]}..."
        elements.append(Paragraph(saint_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*cm))

    conn.close()

    # Build PDF
    doc.build(elements)

    # Get PDF from buffer
    buffer.seek(0)
    return buffer


def generate_year_pdf(year):
    """
    Generate PDF calendar for entire year

    Args:
        year: int

    Returns:
        BytesIO: PDF file in memory
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           topMargin=1.5*cm, bottomMargin=1.5*cm,
                           leftMargin=1.5*cm, rightMargin=1.5*cm)

    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#2563eb'),
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    # Title page
    title = Paragraph(f"<b>Calendario {year}</b>", title_style)
    elements.append(Spacer(1, 3*cm))
    elements.append(title)
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph("Calendario Italiano Completo", styles['Heading2']))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(f"con Santi, Festività e Fasi Lunari", styles['Normal']))
    elements.append(PageBreak())

    italian_months = ['', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
                     'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']

    # Generate a page for each month
    for month in range(1, 13):
        # Month title
        month_title = Paragraph(f"<b>{italian_months[month]}</b>", styles['Heading1'])
        elements.append(month_title)
        elements.append(Spacer(1, 0.5*cm))

        # Calendar grid for month
        cal = calendar.Calendar()
        month_days = cal.monthdayscalendar(year, month)

        table_data = [['L', 'M', 'M', 'G', 'V', 'S', 'D']]

        for week in month_days:
            row = []
            for day in week:
                row.append(str(day) if day != 0 else '')
            table_data.append(row)

        table = Table(table_data, colWidths=[2*cm]*7)
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ])
        table.setStyle(table_style)
        elements.append(table)

        # Add holidays for this month
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        holidays = cursor.execute(
            'SELECT day, name FROM holidays WHERE month = ? AND (year IS NULL OR year = ?)',
            (month, year)
        ).fetchall()
        conn.close()

        if holidays:
            elements.append(Spacer(1, 0.5*cm))
            elements.append(Paragraph("<b>Festività:</b>", styles['Heading3']))
            for holiday in holidays:
                elements.append(Paragraph(f"• {holiday[0]} - {holiday[1]}", styles['Normal']))

        # Page break after each month (except last)
        if month < 12:
            elements.append(PageBreak())

    # Build PDF
    doc.build(elements)

    buffer.seek(0)
    return buffer


def generate_day_pdf(year, month, day):
    """
    Generate detailed PDF for a specific day

    Args:
        year, month, day: int

    Returns:
        BytesIO: PDF file in memory
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           topMargin=2*cm, bottomMargin=2*cm,
                           leftMargin=2*cm, rightMargin=2*cm)

    elements = []
    styles = getSampleStyleSheet()

    italian_months = ['', 'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
                     'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre']
    italian_days = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica']

    date = datetime(year, month, day)
    day_name = italian_days[date.weekday()]

    # Title
    title = Paragraph(f"<b>{day_name.capitalize()} {day} {italian_months[month]} {year}</b>",
                     styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 1*cm))

    # Get all data
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Saints
    saints = cursor.execute('SELECT * FROM saints WHERE day = ? AND month = ?',
                           (day, month)).fetchall()
    if saints:
        elements.append(Paragraph("<b>🙏 Santo del Giorno</b>", styles['Heading2']))
        elements.append(Spacer(1, 0.3*cm))
        for saint in saints:
            elements.append(Paragraph(f"<b>{saint['name']}</b>", styles['Heading3']))
            elements.append(Paragraph(saint['biography'], styles['Normal']))
            elements.append(Spacer(1, 0.5*cm))

    # Holidays
    holidays = cursor.execute('SELECT * FROM holidays WHERE day = ? AND month = ?',
                             (day, month)).fetchall()
    if holidays:
        elements.append(Paragraph("<b>🎉 Festività</b>", styles['Heading2']))
        elements.append(Spacer(1, 0.3*cm))
        for holiday in holidays:
            elements.append(Paragraph(f"<b>{holiday['name']}</b>", styles['Heading3']))
            elements.append(Paragraph(holiday['description'] or '', styles['Normal']))
            elements.append(Spacer(1, 0.5*cm))

    # Proverbs
    proverbs = cursor.execute('SELECT * FROM proverbs WHERE day = ? AND month = ?',
                             (day, month)).fetchall()
    if proverbs:
        elements.append(Paragraph("<b>💭 Proverbio del Giorno</b>", styles['Heading2']))
        elements.append(Spacer(1, 0.3*cm))
        for proverb in proverbs:
            proverb_text = proverb['text'].replace('"', "'")
            elements.append(Paragraph(f'<i>"{proverb_text}"</i>', styles['Normal']))
            elements.append(Spacer(1, 0.5*cm))

    conn.close()

    # Build PDF
    doc.build(elements)

    buffer.seek(0)
    return buffer
